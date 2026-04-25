import os
import asyncio
import logging
import httpx
from fastapi import FastAPI, Request, Header, HTTPException
from contextlib import asynccontextmanager

# ─── LOGGING ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)

# ─── CONFIG ─────────────────────────────────────────────────────────────────
BOT_TOKEN       = os.environ["BOT_TOKEN"]           # Your bot token from @BotFather
WEBHOOK_SECRET  = os.environ["WEBHOOK_SECRET"]      # Any random strong string you set
DUMP_CHANNEL_ID = int(os.environ["DUMP_CHANNEL_ID"])# e.g. -1001234567890
DELETE_AFTER    = int(os.getenv("DELETE_AFTER", "5"))# seconds before deletion

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ─── MEDIA TYPES TO DELETE ──────────────────────────────────────────────────
# Add or remove types based on what you want auto-deleted
DELETABLE_TYPES = {
    "video", "document", "photo", "audio",
    "voice", "video_note", "animation", "sticker"
}

# ─── FASTAPI APP ─────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Bot started. Waiting for webhook updates...")
    yield
    log.info("Bot shutting down.")

app = FastAPI(lifespan=lifespan)

# ─── HELPERS ─────────────────────────────────────────────────────────────────
async def delete_message(chat_id: int, message_id: int):
    """Delete a message via Telegram API."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{TELEGRAM_API}/deleteMessage",
            json={"chat_id": chat_id, "message_id": message_id},
            timeout=10
        )
    result = resp.json()
    if result.get("ok"):
        log.info(f"✅ Deleted message {message_id} from chat {chat_id}")
    else:
        log.warning(f"⚠️ Failed to delete {message_id}: {result.get('description')}")


async def schedule_delete(chat_id: int, message_id: int, delay: int):
    """Wait `delay` seconds, then delete the message."""
    await asyncio.sleep(delay)
    await delete_message(chat_id, message_id)


def get_message_type(message: dict) -> str | None:
    """Return the media type key present in the message, or None."""
    for t in DELETABLE_TYPES:
        if t in message:
            return t
    return None

# ─── WEBHOOK ENDPOINT ────────────────────────────────────────────────────────
@app.post("/webhook")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(default=None)
):
    # Validate secret token to reject fake requests
    if x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret token")

    update = await request.json()
    log.info(f"📩 Update received: {update.get('update_id')}")

    # Handle channel posts (messages in channels come as "channel_post")
    message = update.get("channel_post") or update.get("message")

    if not message:
        return {"ok": True}  # Not a message update, ignore

    chat_id    = message["chat"]["id"]
    message_id = message["message_id"]

    # Only act on the configured dump channel
    if chat_id != DUMP_CHANNEL_ID:
        log.info(f"Ignoring message from chat {chat_id} (not dump channel)")
        return {"ok": True}

    media_type = get_message_type(message)

    if media_type:
        log.info(
            f"🎬 {media_type.upper()} detected (msg {message_id}) "
            f"— deleting in {DELETE_AFTER}s"
        )
        # Schedule deletion in background, don't block webhook response
        asyncio.create_task(schedule_delete(chat_id, message_id, DELETE_AFTER))
    else:
        log.info(f"ℹ️ Text/unknown message {message_id} — skipping")

    return {"ok": True}


# ─── HEALTH CHECK ────────────────────────────────────────────────────────────
@app.get("/")
async def health():
    return {"status": "running", "bot": "Leech Dump Auto-Delete"}

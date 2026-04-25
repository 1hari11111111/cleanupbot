import os
import asyncio
import logging
import httpx
from typing import Optional
from fastapi import FastAPI, Request, Header, HTTPException
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)

BOT_TOKEN       = os.environ["BOT_TOKEN"]
WEBHOOK_SECRET  = os.environ["WEBHOOK_SECRET"]
DUMP_CHANNEL_ID = int(os.environ["DUMP_CHANNEL_ID"])
DELETE_AFTER    = int(os.getenv("DELETE_AFTER", "5"))

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

DELETABLE_TYPES = {
    "video", "document", "photo", "audio",
    "voice", "video_note", "animation", "sticker"
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info(f"Bot started! Watching channel: {DUMP_CHANNEL_ID}")
    yield

app = FastAPI(lifespan=lifespan)

async def delete_message(chat_id: int, message_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{TELEGRAM_API}/deleteMessage",
            json={"chat_id": chat_id, "message_id": message_id},
            timeout=10
        )
    result = resp.json()
    if result.get("ok"):
        log.info(f"Deleted message {message_id} from chat {chat_id}")
    else:
        log.warning(f"Failed to delete {message_id}: {result.get('description')}")

async def schedule_delete(chat_id: int, message_id: int, delay: int):
    await asyncio.sleep(delay)
    await delete_message(chat_id, message_id)

def get_message_type(message: dict) -> Optional[str]:
    for t in DELETABLE_TYPES:
        if t in message:
            return t
    return None

@app.post("/webhook")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Optional[str] = Header(default=None)
):
    if x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret token")

    update = await request.json()
    log.info(f"Update: {update}")

    message = update.get("channel_post") or update.get("message")
    if not message:
        return {"ok": True}

    chat_id    = message["chat"]["id"]
    message_id = message["message_id"]

    log.info(f"Chat ID received: {chat_id}, expected: {DUMP_CHANNEL_ID}")

    if chat_id != DUMP_CHANNEL_ID:
        log.warning(f"Ignoring chat {chat_id}")
        return {"ok": True}

    media_type = get_message_type(message)
    if media_type:
        log.info(f"{media_type.upper()} detected — deleting in {DELETE_AFTER}s")
        asyncio.create_task(schedule_delete(chat_id, message_id, DELETE_AFTER))
    else:
        log.info(f"Text message — skipping")

    return {"ok": True}

@app.get("/")
async def health():
    return {"status": "running", "watching": DUMP_CHANNEL_ID}

import os
import asyncio
import logging
import httpx
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)

# ─── CONFIG ─────────────────────────────────────────────────────────────────
BOT_TOKEN       = os.environ["BOT_TOKEN"]
DUMP_CHANNEL_ID = int(os.environ["DUMP_CHANNEL_ID"])
DELETE_AFTER    = int(os.getenv("DELETE_AFTER", "5"))

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

DELETABLE_TYPES = {
    "video", "document", "photo", "audio",
    "voice", "video_note", "animation", "sticker"
}

# ─── HELPERS ────────────────────────────────────────────────────────────────
async def delete_message(client: httpx.AsyncClient, chat_id: int, message_id: int):
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
    await asyncio.sleep(delay)
    async with httpx.AsyncClient() as client:
        await delete_message(client, chat_id, message_id)

def get_message_type(message: dict) -> Optional[str]:
    for t in DELETABLE_TYPES:
        if t in message:
            return t
    return None

async def process_message(message: dict):
    chat_id    = message["chat"]["id"]
    message_id = message["message_id"]

    if chat_id != DUMP_CHANNEL_ID:
        return

    media_type = get_message_type(message)
    if media_type:
        log.info(f"🎬 {media_type.upper()} detected (msg {message_id}) — deleting in {DELETE_AFTER}s")
        asyncio.create_task(schedule_delete(chat_id, message_id, DELETE_AFTER))
    else:
        log.info(f"💬 Text message {message_id} — skipping")

# ─── POLLING LOOP ───────────────────────────────────────────────────────────
async def poll():
    offset = 0
    log.info(f"🤖 Bot started in POLLING mode! Watching channel: {DUMP_CHANNEL_ID}")

    # First delete any existing webhook
    async with httpx.AsyncClient() as client:
        await client.post(f"{TELEGRAM_API}/deleteWebhook", json={"drop_pending_updates": True})
        log.info("🔗 Webhook cleared. Polling started...")

    async with httpx.AsyncClient() as client:
        while True:
            try:
                resp = await client.get(
                    f"{TELEGRAM_API}/getUpdates",
                    params={
                        "offset": offset,
                        "timeout": 30,
                        "allowed_updates": ["message", "channel_post"]
                    },
                    timeout=40
                )
                data = resp.json()

                if not data.get("ok"):
                    log.warning(f"Bad response: {data}")
                    await asyncio.sleep(5)
                    continue

                updates = data.get("result", [])

                for update in updates:
                    offset = update["update_id"] + 1
                    message = update.get("channel_post") or update.get("message")
                    if message:
                        await process_message(message)

            except httpx.ReadTimeout:
                # Normal for long polling — just continue
                continue
            except Exception as e:
                log.error(f"❌ Error: {e}")
                await asyncio.sleep(5)

# ─── MAIN ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(poll())

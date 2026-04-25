# 🤖 Leech Dump Auto-Delete Bot

Automatically deletes videos, documents, photos, and other media from a
Telegram channel within seconds of being posted — using a **webhook** approach
(no polling, zero wasted resources).

---

## 🎬 What Gets Deleted

By default, these message types are auto-deleted:

- `video` — MP4, MKV etc.
- `document` — any file
- `photo` — images
- `audio` — music files
- `voice` — voice messages
- `video_note` — round video messages
- `animation` — GIFs
- `sticker` — stickers

To change this, edit `DELETABLE_TYPES` in `bot.py`.

---

## 🔒 Security

- Webhook requests are validated using `WEBHOOK_SECRET` (Telegram sends it as a header)
- Fake/external requests get a `403 Forbidden`
- Bot only acts on `DUMP_CHANNEL_ID`, ignores all other chats

---

## 📋 Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check |
| `/webhook` | POST | Telegram webhook receiver |

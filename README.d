# 🤖 Leech Dump Auto-Delete Bot

> Automatically deletes videos, documents, photos, and other media from a Telegram channel within seconds of being posted — using a **webhook** approach (no polling, zero wasted resources).

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot%20API-26A5E4?logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- ⚡ **Instant deletion** — media removed within seconds of being posted
- 🪝 **Webhook-based** — no polling, no wasted CPU or memory
- 🔒 **Secure** — validates every request using a webhook secret
- 🎯 **Targeted** — only acts on your specified channel, ignores everything else
- 🛠️ **Configurable** — easily control which media types to delete

---

## 🎬 What Gets Deleted

By default, the following message types are auto-deleted:

| Type | Description |
|------|-------------|
| `video` | MP4, MKV, and other video files |
| `document` | Any file/document |
| `photo` | Images |
| `audio` | Music files |
| `voice` | Voice messages |
| `video_note` | Round video messages |
| `animation` | GIFs |
| `sticker` | Stickers |

> To customize, edit the `DELETABLE_TYPES` list in `bot.py`.

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- A public HTTPS URL for the webhook (e.g., from a VPS or Railway/Render)

### 1. Clone the repository

```bash
git clone https://github.com/1hari11111111/cleanupbot.git
cd cleanupbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the root directory:

```env
BOT_TOKEN=your_telegram_bot_token
DUMP_CHANNEL_ID=your_channel_id        # e.g. -1001234567890
WEBHOOK_SECRET=your_random_secret_key  # any strong random string
WEBHOOK_URL=https://yourdomain.com     # your public server URL
PORT=8000
```

### 4. Run the bot

```bash
python bot.py
```

The bot will automatically register the webhook with Telegram on startup.

---

## 🚀 Deployment

### On a VPS (with PM2)

```bash
pip install -r requirements.txt
pm2 start bot.py --interpreter python3 --name cleanupbot
pm2 save && pm2 startup
```

### On Railway / Render

1. Connect your GitHub repo
2. Add environment variables in the dashboard
3. Deploy — the `Procfile` handles the rest automatically

---

## 🔒 Security

- Every incoming webhook request is validated using `WEBHOOK_SECRET`
- Requests missing or with an invalid secret receive a `403 Forbidden` response
- The bot only processes updates from `DUMP_CHANNEL_ID` and silently ignores all other chats

---

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | `GET` | Health check — returns `200 OK` |
| `/webhook` | `POST` | Telegram webhook receiver |

---

## 📦 Dependencies

See [`requirements.txt`](requirements.txt) for the full list. Core libraries include:

- [`python-telegram-bot`](https://python-telegram-bot.org/) or `aiohttp` for webhook handling
- `python-dotenv` for environment variable management

---

## ⚠️ Security Notice

- **Never** commit your `.env` file — it's already in `.gitignore`
- If your `BOT_TOKEN` or `WEBHOOK_SECRET` is ever exposed, regenerate them immediately
- Use a strong, random string for `WEBHOOK_SECRET`

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👤 Author

**1hari11111111**
GitHub: [@1hari11111111](https://github.com/1hari11111111)

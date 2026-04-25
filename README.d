# 🤖 Leech Dump Auto-Delete Bot

Automatically deletes videos, documents, photos, and other media from a
Telegram channel within seconds of being posted — using a **webhook** approach
(no polling, zero wasted resources).

---

## ⚙️ Setup

### 1. Create your bot
- Open Telegram → talk to [@BotFather](https://t.me/BotFather)
- `/newbot` → follow steps → copy the **BOT_TOKEN**

### 2. Add bot to your channel
- Go to your leech dump channel → Settings → Administrators
- Add your bot as admin with **"Delete Messages"** permission
- That's the only permission it needs

### 3. Get your channel ID
- Forward any message from your channel to [@userinfobot](https://t.me/userinfobot)
- It shows the chat ID — it will look like `-1001234567890`

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your values
```

| Variable | Description |
|---|---|
| `BOT_TOKEN` | From @BotFather |
| `WEBHOOK_SECRET` | Any random string (e.g. `openssl rand -hex 32`) |
| `DUMP_CHANNEL_ID` | Your channel ID e.g. `-1001234567890` |
| `DELETE_AFTER` | Seconds before deletion (default: `5`) |
| `WEBHOOK_URL` | Your deployed URL e.g. `https://mangoi.in/webhook` |

---

## 🚀 Deploy on mangoi.in

### Step 1 — Upload files
Upload all project files to your mangoi.in hosting panel.

### Step 2 — Set environment variables
In your hosting panel, add all variables from `.env.example`.

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Start the server
```bash
uvicorn bot:app --host 0.0.0.0 --port 8000
```
Or if mangoi.in uses a Procfile, it runs automatically.

### Step 5 — Register the webhook (run once!)
```bash
# Set env vars first, then:
python setup_webhook.py
```

You should see: `✅ Webhook registered successfully!`

---

## 🧪 Test Locally (optional)

```bash
pip install -r requirements.txt

# Use ngrok for a public HTTPS URL
ngrok http 8000

# In another terminal:
export BOT_TOKEN=...
export WEBHOOK_SECRET=...
export DUMP_CHANNEL_ID=...
export DELETE_AFTER=5
export WEBHOOK_URL=https://YOUR_NGROK_URL/webhook

uvicorn bot:app --reload --port 8000

# Register webhook:
python setup_webhook.py
```

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

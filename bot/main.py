from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

from bot.config import BOT_TOKEN, WEBHOOK_PATH
from bot.handlers import delete_message

app = FastAPI()

# Create bot app
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handler (IMPORTANT: captures channel posts)
application.add_handler(MessageHandler(filters.ALL, delete_message))


@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.start()
    print("Bot started")


@app.on_event("shutdown")
async def on_shutdown():
    await application.stop()
    await application.shutdown()
    print("Bot stopped")


@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}

from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8702676707:AAFd11ZFko6cyt7KAyc9dmlsk3Qgjb8RuKY"
WEBHOOK_PATH = "/webhook"

app = FastAPI()

# Create bot
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Delete handler
async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message

    if not msg:
        return

    try:
        await msg.delete()
        print("Deleted instantly")
    except Exception as e:
        print(f"Error: {e}")

# Add handler (IMPORTANT)
application.add_handler(MessageHandler(filters.ALL, delete_message))


@app.on_event("startup")
async def startup():
    await application.initialize()
    await application.start()
    print("Bot started")


@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}

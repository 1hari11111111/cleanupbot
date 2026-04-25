from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8702676707:AAFd11ZFko6cyt7KAyc9dmlsk3Qgjb8RuKY

app = FastAPI()

# Create bot application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Handler to delete messages
async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if msg:
        try:
            await msg.delete()
            print("Deleted message")
        except Exception as e:
            print(f"Error: {e}")

# Add handler
application.add_handler(MessageHandler(filters.ALL, delete_message))


# Startup event (VERY IMPORTANT)
@app.on_event("startup")
async def startup():
    await application.initialize()
    await application.start()
    print("Bot started")


# ✅ THIS IS YOUR WEBHOOK ROUTE (CRITICAL)
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Webhook received")  # debug

    update = Update.de_json(data, application.bot)
    await application.process_update(update)

    return {"ok": True}

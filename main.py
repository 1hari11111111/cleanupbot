from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8702676707:AAFd11ZFko6cyt7KAyc9dmlsk3Qgjb8RuKY"

app = FastAPI()

application = ApplicationBuilder().token(BOT_TOKEN).build()

async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if msg:
        try:
            await msg.delete()
            print("Deleted")
        except Exception as e:
            print(e)

application.add_handler(MessageHandler(filters.ALL, delete_message))


@app.on_event("startup")
async def startup():
    await application.initialize()
    await application.start()
    print("Bot started")


# ✅ REQUIRED ROUTE
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Webhook hit")

    update = Update.de_json(data, application.bot)
    await application.process_update(update)

    return {"ok": True}

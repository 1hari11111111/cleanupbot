from telegram import Update
from telegram.ext import ContextTypes

async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message

    if not msg:
        return

    try:
        # delete everything (or customize)
        await msg.delete()
        print("Deleted message instantly")
    except Exception as e:
        print(f"Delete error: {e}")

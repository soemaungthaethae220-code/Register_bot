import os
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8927826902:AAEi7UQgdBc4gWRIshDtLjRm6Hych15sAF4"
ADMIN_CHAT_ID = 6395918397

ptb = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    device_id = args[0] if args else "Not Provided"
    
    message = f"New Device Registration:\nUser ID: {user_id}\nDevice ID: {device_id}"
    await update.get_bot().send_message(chat_id=ADMIN_CHAT_ID, text=message)
    await update.message.reply_text("Your Device ID has been registered successfully!")

ptb.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    import requests
    # Webhook ပိတ်ပြီး Polling စနစ်ကို တိုက်ရိုက်စတင်မည်
    requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=true")
    
    print("Starting bot in polling mode...")
    ptb.run_polling(allowed_updates=Update.ALL_TYPES)

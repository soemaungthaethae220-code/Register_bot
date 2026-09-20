import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8927826902:AAEi7UQgdBc4gWRIshDtLjRm6Hych15sAF4"
ADMIN_CHAT_ID = 6395918397

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    device_id = args[0] if args else "Not Provided"
    
    message = f"New Device Registration:\nUser ID: {user_id}\nDevice ID: {device_id}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
    await update.message.reply_text(f"Your Device ID ({device_id}) has been registered successfully!")

if __name__ == '__main__':
    # python-telegram-bot v20.7 အတွက် အတည်ငြိမ်ဆုံး တည်ဆောက်ပုံ
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    print("Bot is starting polling...")
    application.run_polling(drop_pending_updates=True)

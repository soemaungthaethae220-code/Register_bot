import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging သတ်မှတ်ခြင်း
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8927826902:AAEi7UQgdBc4gWRIshDtLjRm6Hych15sAF4"
ADMIN_CHAT_ID = 6395918397

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    device_id = args[0] if args else "Not Provided"
    
    # Admin ဆီသို့ Device ID ပို့မည်
    message = f"New Device Registration:\nUser ID: {user_id}\nDevice ID: {device_id}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
    
    # အသုံးပြုသူထံသို့ ပြန်စာပို့မည်
    await update.message.reply_text(f"Your Device ID ({device_id}) has been registered successfully!")

if __name__ == '__main__':
    # ApplicationBuilder ကို တရားဝင်စနစ်အတိုင်း တည်ဆောက်ခြင်း
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    print("Bot is running with polling...")
    application.run_polling()

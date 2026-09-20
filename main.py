import os
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8927826902:AAEi7UQgdBc4gWRIshDtLjRm6Hych15sAF4"
ADMIN_CHAT_ID = 6395918397

# Telegram Application တည်ဆောက်ခြင်း (Polling အတွက်)
ptb = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    device_id = args[0] if args else "Not Provided"
    
    # Admin ဆီကို Device ID ပို့မည်
    message = f"New Device Registration:\nUser ID: {user_id}\nDevice ID: {device_id}"
    await update.get_bot().send_message(chat_id=ADMIN_CHAT_ID, text=message)
    
    # အသုံးပြုသူ ဆီကို ပြန်စာပို့မည်
    await update.message.reply_text("Your Device ID has been registered successfully!")

ptb.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    # Telegram ရဲ့ အရင် Webhook တွေကို အရင်ရှင်းထုတ်မည်
    import requests
    requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=true")
    
    print("Bot is starting with Polling...")
    # ဖရီးဆာဗာမှာ ဝက်ဘ်ဆာဗာ မလိုတော့ဘဲ တိုက်ရိုက် run မည်
    ptb.run_polling(allowed_updates=Update.ALL_TYPES)

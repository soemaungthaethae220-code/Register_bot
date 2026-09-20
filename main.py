import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8927826902:AAEi7UQgdBc4gWRIshDtLjRm6Hych15sAF4"
ADMIN_CHAT_ID = 6395918397

app = Flask(__name__)
bot = Bot(token=TOKEN)

ptb = Application.builder().token(TOKEN).updater(None).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    device_id = args[0] if args else "Not Provided"
    
    message = f"New Device Registration:\nUser ID: {user_id}\nDevice ID: {device_id}"
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
    await update.message.reply_text("Your Device ID has been registered successfully!")

ptb.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.run(ptb.process_update(update))
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot is running nicely!", 200

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(ptb.initialize())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

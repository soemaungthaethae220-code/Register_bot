import os
import telegram
from flask import Flask, request

TOKEN = "8927826902:AAEi7UQgdBc4gWRIshDtLjRm6Hych15sAF4"
# အစ်ကို့ရဲ့ Chat ID ကို ထည့်ထားပါပြီ
ADMIN_CHAT_ID = "6395918397"  

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    
    if update.message:
        chat_id = update.message.chat.id
        user = update.message.from_user
        
        username = f"@{user.username}" if user.username else user.first_name
        text = update.message.text.strip()
        
        if text.startswith('/start'):
            parts = text.split(' ')
            if len(parts) > 1:
                device_id = parts[1]
                admin_msg = f"🚨 **New Registration Request!**\n\n👤 **User:** {username}\n📱 **Device ID:** `{device_id}`"
                
                try:
                    bot.sendMessage(chat_id=ADMIN_CHAT_ID, text=admin_msg, parse_mode="Markdown")
                except Exception as e:
                    print(f"Error sending to admin: {e}")
                
                bot.sendMessage(chat_id=chat_id, text="ကျေးဇူးတင်ပါတယ်။ သင့်ရဲ့ Device ID ကို Admin ထံ ပို့ပြီးပါပြီ။ အကောင့်ဖွင့်ပေးသည်အထိ ခဏစောင့်ပေးပါ။")
            else:
                bot.sendMessage(chat_id=chat_id, text="ကျေးဇူးပြု၍ App ထဲမှ Register ခလုတ်ကို နှိပ်ပါ။")
                
    return 'ok'

@app.route('/')
def index():
    return 'Bot is running nicely!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


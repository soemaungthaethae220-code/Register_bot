import os
import time
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "8927826902:AAEi7UQgdBc4gWRIshDtLjRm6Hych15sAF4"
ADMIN_CHAT_ID = "6395918397"
CHANNEL_USERNAME = "@YMBA_MOD_SHAIRING"
CHANNEL_LINK = "https://t.me/YMBA_MOD_SHAIRING"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Render Free Tier အတွက် Port ဖွင့်ပေးမည့် mini web server
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active and running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"Web server running on port {port}")
    server.serve_forever()

def send_message(chat_id, text, reply_markup=None, parse_mode=None):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    if parse_mode:
        payload["parse_mode"] = parse_mode
    requests.post(url, json=payload)

def check_user_in_channel(user_id):
    url = f"{BASE_URL}/getChatMember"
    payload = {"chat_id": CHANNEL_USERNAME, "user_id": user_id}
    response = requests.get(url, params=payload)
    data = response.json()
    if data.get("ok"):
        status = data["result"].get("status")
        if status in ["creator", "administrator", "member"]:
            return True
    return False

def main():
    # Web server ကို background မှာ အလုပ်လုပ်ခိုင်းမည် (Port error မတက်အောင်)
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()

    print("Bot started with Free Tier Web Service support...")
    offset = 0
    requests.get(f"{BASE_URL}/deleteWebhook?drop_pending_updates=true")
    
    while True:
        try:
            response = requests.get(f"{BASE_URL}/getUpdates", params={"offset": offset, "timeout": 30})
            data = response.json()
            
            if data.get("ok"):
                for result in data.get("result", []):
                    offset = result["update_id"] + 1
                    
                    message = result.get("message")
                    if message and "text" in message:
                        text = message["text"]
                        user_id = message["from"]["id"]
                        
                        if text.startswith("/start"):
                            if str(user_id) != str(ADMIN_CHAT_ID):
                                is_member = check_user_in_channel(user_id)
                                if not is_member:
                                    warning_text = (
                                        ">⚠️ **ဝင်ရောက်ခွင့် မရှိသေးပါ!**\n\n"
                                        ">🚀 ဒီ Bot ကို အသုံးမပြုမီ ကျွန်ုပ်တို့၏ Channel သို့ ဦးစွာ Join ပေးပါရန် မေတ္တာရပ်ခံအပ်ပါတယ်:"
                                    )
                                    keyboard = {
                                        "inline_keyboard": [
                                            [{"text": "📢 ချန်နယ်သို့ ဝင်မည် (VIEW CHANNEL)", "url": CHANNEL_LINK}]
                                        ]
                                    }
                                    send_message(user_id, warning_text, reply_markup=keyboard, parse_mode="Markdown")
                                    continue
                            
                            parts = text.split(" ")
                            device_id = parts[1] if len(parts) > 1 else "Not Provided"
                            
                            admin_msg = (
                                ">🔔 **စက်ပစ္စည်း အသစ် မှတ်ပုံတင်ခြင်း:**\n"
                                f">👤 အသုံးပြုသူ ID: `{user_id}`\n"
                                f">📱 စက်ပစ္စည်း ID: `{device_id}`"
                            )
                            send_message(ADMIN_CHAT_ID, admin_msg, parse_mode="Markdown")
                            
                            reply_msg = (
                                ">✅ **အောင်မြင်ပါသည်!**\n"
                                f">သင့်ရဲ့ Device ID (`{device_id}`) ကို စနစ်အတွင်း အောင်မြင်စွာ မှတ်ပုံတင်ပြီးပါပြီ။"
                            )
                            send_message(user_id, reply_msg, parse_mode="Markdown")
                            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

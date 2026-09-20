import os
import time
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "8927826902:AAEi7UQgdBc4gWRIshDtLjRm6Hych15sAF4"
ADMIN_CHAT_ID = "6395918397"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

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
    response = requests.post(url, json=payload)
    return response.json()

def main():
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()

    print("Bot started with clean Admin Approval system...")
    offset = 0
    requests.get(f"{BASE_URL}/deleteWebhook?drop_pending_updates=true")
    
    while True:
        try:
            response = requests.get(f"{BASE_URL}/getUpdates", params={"offset": offset, "timeout": 30})
            data = response.json()
            
            if data.get("ok"):
                for result in data.get("result", []):
                    offset = result["update_id"] + 1
                    
                    # 1. Callback Query (Admin က Button နှိပ်တဲ့အခါ)
                    if "callback_query" in result:
                        callback = result["callback_query"]
                        callback_id = callback["id"]
                        cb_data = callback["data"]
                        
                        if cb_data.startswith("approve_"):
                            user_chat_id = cb_data.replace("approve_", "")
                            
                            # User ဆီကို အတည်ပြုပြီးကြောင်း စာပို့မည်
                            success_msg = (
                                ">✅ **အတည်ပြုပြီးပါပြီ!**\n"
                                ">သင့်ရဲ့ Device ID ကို Admin မှ စစ်ဆေးအတည်ပြုပြီးဖြစ်၍ အောင်မြင်စွာ အသုံးပြုနိုင်ပါပြီ။"
                            )
                            send_message(user_chat_id, success_msg, parse_mode="Markdown")
                            
                            # Admin ကို အသိပေးရန်
                            requests.post(f"{BASE_URL}/answerCallbackQuery", json={
                                "callback_query_id": callback_id,
                                "text": "✅ User ကို အတည်ပြုစာ ပို့ပြီးပါပြီ!"
                            })
                        continue

                    # 2. Normal Message (User ဘက်က ပို့လာတဲ့အခါ)
                    message = result.get("message")
                    if message and "text" in message:
                        text = message["text"]
                        user_id = message["from"]["id"]
                        
                        if text.startswith("/start"):
                            parts = text.split(" ")
                            if len(parts) < 2 or not parts[1].strip():
                                missing_msg = (
                                    ">⚠️ **စက်ပစ္စည်း ID လိုအပ်နေပါသည်!**\n\n"
                                    ">❌ ကျေးဇူးပြု၍ Device ID ထည့်သွင်းပြီးမှ ပြန်လည် ပို့ပေးပါ။\n"
                                    ">💡 **ပုံစံမှန်:** `/start [သင့်ရဲ့ Device ID]`"
                                )
                                send_message(user_id, missing_msg, parse_mode="Markdown")
                                continue
                            
                            device_id = parts[1].strip()
                            
                            if len(device_id) < 3:
                                invalid_msg = (
                                    ">⚠️ **Device ID မမှန်ကန်ပါ!**\n\n"
                                    ">❌ ထည့်သွင်းလိုက်သော Device ID မှာ တိုလွန်းနေပါသည် သို့မဟုတ် ပုံစံမမှန်ပါ။"
                                )
                                send_message(user_id, invalid_msg, parse_mode="Markdown")
                                continue
                            
                            # User ကို 24 hours waiting လို့ စာပို့မည်
                            waiting_msg = (
                                ">⏳ **24 Hour Waiting...**\n\n"
                                f">📱 သင်ပေးပို့ထားသော Device ID (`{device_id}`) ကို လက်ခံရရှိပါပြီ။\n"
                                ">🛠️ Admin မှ စစ်ဆေးအတည်ပြုနေပါပြီ၊ ခဏစောင့်ဆိုင်းပေးပါ။"
                            )
                            send_message(user_id, waiting_msg, parse_mode="Markdown")
                            
                            # Admin ဆီသို့ Button နဲ့တကွ ပို့မည်
                            admin_msg = (
                                ">🔔 **Device ID အတည်ပြုရန် တောင်းဆိုမှု:**\n"
                                f">👤 User ID: `{user_id}`\n"
                                f">📱 Device ID: `{device_id}`\n\n"
                                ">အောက်ပါခလုတ်ကိုနှိပ်၍ အတည်ပြုပေးပါ 👇"
                            )
                            keyboard = {
                                "inline_keyboard": [
                                    [
                                        {
                                            "text": "✅ Device ID အတည်ပြုမည်",
                                            "callback_data": f"approve_{user_id}"
                                        }
                                    ]
                                ]
                            }
                            send_message(ADMIN_CHAT_ID, admin_msg, reply_markup=keyboard, parse_mode="Markdown")
                            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

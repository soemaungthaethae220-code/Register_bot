import os
import time
import requests

TOKEN = "8927826902:AAEi7UQgdBc4gWRIshDtLjRm6Hych15sAF4"
ADMIN_CHAT_ID = "6395918397"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def main():
    print("Bot started with direct API polling...")
    offset = 0
    
    # Webhook များကို အရင်ရှင်းထုတ်မည်
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
                            parts = text.split(" ")
                            device_id = parts[1] if len(parts) > 1 else "Not Provided"
                            
                            # Admin ဆီသို့ Device ID ပို့မည်
                            admin_msg = f"New Device Registration:\nUser ID: {user_id}\nDevice ID: {device_id}"
                            send_message(ADMIN_CHAT_ID, admin_msg)
                            
                            # User ထံသို့ အောင်မြင်ကြောင်း ပြန်ပို့မည်
                            reply_msg = f"Your Device ID ({device_id}) has been registered successfully!"
                            send_message(user_id, reply_msg)
                            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

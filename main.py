import os, time, threading, requests
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
BASE = f"https://api.telegram.org/bot{TOKEN}"
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def send(chat_id, text):
    try:
        requests.post(f"{BASE}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except Exception as e:
        print("SEND ERROR:", e, flush=True)

def polling():
    offset = 0
    print("=== BOT POLLING STARTED ===", flush=True)
    while True:
        try:
            r = requests.get(f"{BASE}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=40).json()
            for u in r.get("result", []):
                offset = u["update_id"] + 1
                msg = u.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "")
                if not chat_id: continue
                if text == "/start":
                    send(chat_id, "Hello! Bot is working!")
                elif text == "/signal":
                    send(chat_id, "SIGNAL Pair: USDJPY Action: BUY")
        except Exception as e:
            print("POLLING ERROR:", e, flush=True)
            time.sleep(3)

if __name__ == "__main__":
    print("=== BOT STARTING ===", flush=True)
    print("TOKEN EXISTS:", bool(TOKEN), flush=True)
    threading.Thread(target=polling, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

@'
from flask import Flask, request
import requests
import anthropic
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

def ask_claude(user_text):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system="You are SOLVAIN, a sharp and helpful AI assistant with a cyberpunk personality. Keep replies concise.",
        messages=[{"role": "user", "content": user_text}]
    )
    return message.content[0].text

def send_telegram(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=10.0,
    )

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    logger.info("Incoming: %s", data)

    message = data.get("message") or data.get("edited_message")
    if not message:
        return "ok", 200

    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    if not chat_id or not text:
        return "ok", 200

    try:
        reply = ask_claude(text)
    except Exception as e:
        logger.exception("Claude error: %s", e)
        reply = "Something went wrong. Try again."

    try:
        send_telegram(chat_id, reply)
    except Exception as e:
        logger.exception("Telegram error: %s", e)

    return "ok", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
'@ | Set-Content -Path "app.py"
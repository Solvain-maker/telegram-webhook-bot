from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
ODY_API_URL = os.getenv("ODYSSEUS_API_URL")  # optional: forward to your Odysseus app
ODY_API_TOKEN = os.getenv("ODYSSEUS_API_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    # Basic validation
    message = data.get("message") or data.get("edited_message")
    if not message:
        return "ok", 200

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "")

    # Simple echo reply
    if chat_id and TOKEN:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": f"You said: {text}"},
                timeout=10.0,
            )
        except Exception:
            pass

    # Optional: forward the message to local Odysseus API chat endpoint
    if ODY_API_URL and ODY_API_TOKEN and text:
        try:
            headers = {"Authorization": f"Bearer {ODY_API_TOKEN}", "Content-Type": "application/json"}
            payload = {"message": text, "session": None}
            requests.post(f"{ODY_API_URL}/api/chat", json=payload, headers=headers, timeout=20.0)
        except Exception:
            pass

    return "ok", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

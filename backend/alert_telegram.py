"""
alert_telegram.py
Sends alert messages via Telegram Bot API.

Setup (5 minutes):
1. Open Telegram, search @BotFather
2. Send /newbot, follow prompts, get your bot token
3. Send any message to your new bot
4. Visit https://api.telegram.org/bot<TOKEN>/getUpdates to find your chat_id
5. Put both in backend/.env
"""

import requests
from config import settings


def send_telegram_alert(message: str) -> dict:
    """Send a message to the configured Telegram chat. Returns {success, ...}."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return {"success": False, "error": "Telegram not configured in .env"}

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": f"🛡️ CyberMate Alert\n\n{message}",
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {
            "success": True,
            "message_id": data["result"]["message_id"],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    # Quick standalone test: python alert_telegram.py
    result = send_telegram_alert("Test alert — CyberMate backend is connected.")
    print(result)

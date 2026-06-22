"""
alert_email.py
Sends alert emails via Gmail SMTP. Used as a fallback if Telegram fails.

Setup:
1. Go to Google Account -> Security -> 2-Step Verification -> App Passwords
2. Generate an app password for "Mail"
3. Put GMAIL_ADDRESS and GMAIL_APP_PASSWORD in backend/.env
"""

import smtplib
from email.mime.text import MIMEText
from config import settings


def send_email_alert(message: str, subject: str = "CyberMate Security Alert") -> dict:
    if not settings.GMAIL_ADDRESS or not settings.GMAIL_APP_PASSWORD:
        return {"success": False, "error": "Gmail not configured in .env"}

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = settings.GMAIL_ADDRESS
    msg["To"] = settings.GMAIL_ADDRESS  # sending to yourself for the demo

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(settings.GMAIL_ADDRESS, settings.GMAIL_APP_PASSWORD)
            server.send_message(msg)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    result = send_email_alert("Test alert — CyberMate email backup is working.")
    print(result)

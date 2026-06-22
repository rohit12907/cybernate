"""
config.py
Loads all environment variables from .env file.
Every other backend file imports settings from here.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "cybermate.db")

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    # Gmail SMTP
    GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

    # Agent pipeline (Person 2's server)
    AGENT_API_URL = os.getenv("AGENT_API_URL", "http://localhost:8001")

    # Log files to watch
    LOG_PATHS = os.getenv("LOG_PATHS", "/var/log/auth.log").split(",")


settings = Settings()

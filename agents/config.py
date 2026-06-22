import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8001"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama3-70b-8192")

    ABUSEIPDB_API_KEY: str = os.getenv("ABUSEIPDB_API_KEY", "")
    NVD_API_KEY: str = os.getenv("NVD_API_KEY", "")
    OTX_API_KEY: str = os.getenv("OTX_API_KEY", "")

    BACKEND_API_URL: str = os.getenv("BACKEND_API_URL", "http://localhost:8000")

    MAX_LOG_LENGTH: int = 4096
    REQUEST_TIMEOUT: int = 30
    CONFIDENCE_THRESHOLD: float = 0.6

    @classmethod
    def validate(cls):
        missing = []
        if not cls.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
        if not cls.ABUSEIPDB_API_KEY:
            missing.append("ABUSEIPDB_API_KEY")
        if missing:
            print(f"Warning: Missing API keys: {', '.join(missing)}")
            print("The pipeline will use mock data for missing APIs.")

config = Config()
config.validate()

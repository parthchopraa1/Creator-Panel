import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "CreatorMVP")
    ENV: str = os.getenv("ENV", "dev")
    PORT: int = int(os.getenv("PORT", "8000"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret")
    # Google
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "")
    GOOGLE_SCOPES: str = os.getenv("GOOGLE_SCOPES", "https://www.googleapis.com/auth/youtube.readonly")

settings = Settings()

def get_fernet():
    if not settings.ENCRYPTION_KEY:
        raise RuntimeError("ENCRYPTION_KEY is not set")
    return Fernet(settings.ENCRYPTION_KEY.encode())

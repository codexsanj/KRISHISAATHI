import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "KrishiSaathi Backend"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "krishisaathi_super_secret_jwt_key_sih_hackathon_demo_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Database
    DATABASE_URL: str = "sqlite:///./krishisaathi.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # External APIs
    GEMINI_API_KEY: str = ""
    WEATHER_API_KEY: str = ""
    MARKET_API_KEY: str = ""
    DATA_GOV_IN_API_KEY: str = ""
    FIREBASE_CREDENTIALS_PATH: str = ""

    # Uploads
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

try:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
except Exception:
    pass

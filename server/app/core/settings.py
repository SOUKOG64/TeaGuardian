import os
from pathlib import Path


SERVER_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = SERVER_DIR / "teaguardian.db"


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}",
    )
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "tea-guardian-dev-secret-key-1234567890")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()
DATABASE_URL = settings.DATABASE_URL

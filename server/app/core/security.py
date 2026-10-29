from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from app.core.settings import Settings


settings = Settings()


def _normalize_password(password: str) -> bytes:
    return password.encode("utf-8")[:72]


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(_normalize_password(password), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(_normalize_password(password), password_hash.encode("utf-8"))


def create_token(subject: str, token_type: str) -> str:
    expires_value = settings.ACCESS_TOKEN_EXPIRE_MINUTES if token_type == "access" else settings.REFRESH_TOKEN_EXPIRE_DAYS
    delta = timedelta(minutes=expires_value) if token_type == "access" else timedelta(days=expires_value)
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + delta).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

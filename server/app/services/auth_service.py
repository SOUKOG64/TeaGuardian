from fastapi import HTTPException, status

from app.core.security import create_token, decode_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, name: str, email: str, password: str):
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        password_hash = hash_password(password)
        user = self.user_repository.create(name=name, email=email, password_hash=password_hash)
        return {
            "user": {"id": user.id, "name": user.name, "email": user.email},
            "access_token": create_token(str(user.id), "access"),
            "refresh_token": create_token(str(user.id), "refresh"),
        }

    def login(self, email: str, password: str):
        user = self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return {
            "user": {"id": user.id, "name": user.name, "email": user.email},
            "access_token": create_token(str(user.id), "access"),
            "refresh_token": create_token(str(user.id), "refresh"),
        }

    def refresh(self, refresh_token: str):
        try:
            payload = decode_token(refresh_token)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

        user_id = payload.get("sub")
        user = self.user_repository.get_by_id(int(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return {
            "access_token": create_token(str(user.id), "access"),
            "refresh_token": create_token(str(user.id), "refresh"),
        }

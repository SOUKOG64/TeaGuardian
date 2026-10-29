from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenPair, TokenRefresh, UserLogin, UserRegister
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/register", response_model=TokenPair, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    service = AuthService(UserRepository(db))
    return service.register(payload.name, payload.email, payload.password)


@router.post("/login", response_model=TokenPair)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(UserRepository(db))
    return service.login(payload.email, payload.password)


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: TokenRefresh, db: Session = Depends(get_db)):
    service = AuthService(UserRepository(db))
    return service.refresh(payload.refresh_token)


@router.get("/me")
def me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    user = UserRepository(db).get_by_id(int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {"id": user.id, "name": user.name, "email": user.email}

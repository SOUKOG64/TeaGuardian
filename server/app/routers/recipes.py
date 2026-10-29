from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.repositories.recipe_repository import RecipeRepository
from app.schemas.recipe import RecipeCreate, RecipeRead, RecipeUpdate
from app.services.recipe_service import RecipeService

router = APIRouter(prefix="/api/v1/recipes", tags=["recipes"])
security = HTTPBearer()


def get_user_id_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    try:
        payload = decode_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    return int(payload["sub"])


@router.get("", response_model=list[RecipeRead])
def list_recipes(
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db),
    search: str | None = Query(default=None),
    tea_type_id: int | None = Query(default=None),
):
    service = RecipeService(RecipeRepository(db))
    return service.list_recipes(user_id, search=search, tea_type_id=tea_type_id)


@router.get("/{recipe_id}", response_model=RecipeRead)
def get_recipe(
    recipe_id: int,
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db),
):
    service = RecipeService(RecipeRepository(db))
    return service.get_recipe(user_id, recipe_id)


@router.post("", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
def create_recipe(
    payload: RecipeCreate,
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db),
):
    service = RecipeService(RecipeRepository(db))
    return service.create_recipe(user_id, payload.model_dump())


@router.patch("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: int,
    payload: RecipeUpdate,
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db),
):
    service = RecipeService(RecipeRepository(db))
    return service.update_recipe(user_id, recipe_id, payload.model_dump(exclude_unset=True))


@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db),
):
    service = RecipeService(RecipeRepository(db))
    return service.delete_recipe(user_id, recipe_id)

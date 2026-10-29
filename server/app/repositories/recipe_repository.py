from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Recipe, TeaType


class RecipeRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: int, search: str | None = None, tea_type_id: int | None = None) -> list[Recipe]:
        stmt = select(Recipe).where(Recipe.user_id == user_id)
        if search:
            stmt = stmt.where(Recipe.name.ilike(f"%{search}%"))
        if tea_type_id is not None:
            stmt = stmt.where(Recipe.tea_type_id == tea_type_id)
        return list(self.db.scalars(stmt.order_by(Recipe.id.desc())).all())

    def get_by_id_and_user(self, recipe_id: int, user_id: int) -> Recipe | None:
        return self.db.scalar(
            select(Recipe).where(Recipe.id == recipe_id, Recipe.user_id == user_id)
        )

    def create(self, user_id: int, payload: dict) -> Recipe:
        recipe = Recipe(user_id=user_id, **payload)
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return recipe

    def update(self, recipe: Recipe, payload: dict) -> Recipe:
        for key, value in payload.items():
            if value is not None:
                setattr(recipe, key, value)
        self.db.commit()
        self.db.refresh(recipe)
        return recipe

    def delete(self, recipe: Recipe) -> None:
        self.db.delete(recipe)
        self.db.commit()

    def tea_type_exists(self, tea_type_id: int) -> bool:
        return self.db.get(TeaType, tea_type_id) is not None

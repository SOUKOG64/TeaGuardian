from fastapi import HTTPException, status

from app.repositories.recipe_repository import RecipeRepository


class RecipeService:
    def __init__(self, recipe_repository: RecipeRepository):
        self.recipe_repository = recipe_repository

    def list_recipes(self, user_id: int, search: str | None = None, tea_type_id: int | None = None):
        return self.recipe_repository.list_for_user(user_id, search=search, tea_type_id=tea_type_id)

    def get_recipe(self, user_id: int, recipe_id: int):
        recipe = self.recipe_repository.get_by_id_and_user(recipe_id, user_id)
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        return recipe

    def create_recipe(self, user_id: int, payload: dict):
        if not self.recipe_repository.tea_type_exists(payload["tea_type_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tea type not found")
        return self.recipe_repository.create(user_id, payload)

    def update_recipe(self, user_id: int, recipe_id: int, payload: dict):
        recipe = self.get_recipe(user_id, recipe_id)
        if payload.get("tea_type_id") is not None and not self.recipe_repository.tea_type_exists(payload["tea_type_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tea type not found")
        return self.recipe_repository.update(recipe, payload)

    def delete_recipe(self, user_id: int, recipe_id: int):
        recipe = self.get_recipe(user_id, recipe_id)
        self.recipe_repository.delete(recipe)
        return {"detail": "Recipe deleted"}

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RecipeCreate(BaseModel):
    tea_type_id: int
    name: str = Field(..., min_length=2, max_length=150)
    temperature: int = Field(..., ge=40, le=100)
    notes: Optional[str] = None
    is_private: bool = True


class RecipeUpdate(BaseModel):
    tea_type_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    temperature: Optional[int] = Field(None, ge=40, le=100)
    notes: Optional[str] = None
    is_private: Optional[bool] = None


class RecipeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    tea_type_id: int
    name: str
    temperature: int
    notes: Optional[str]
    is_private: bool

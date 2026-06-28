from typing import Optional
from pydantic import BaseModel, Field


class CategoriesFiltersSchema(BaseModel):
    name_order: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class CreateCategorySchema(BaseModel):
    name: str
    description: str


class UpdateCategorySchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

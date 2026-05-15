from typing import Optional
from pydantic import BaseModel


class CategoriesFiltersSchema(BaseModel):
    name_order: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None


class CreateCategorySchema(BaseModel):
    name: str
    description: str


class UpdateCategorySchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

from pydantic import BaseModel
from typing import Optional


class CategoriesFilters(BaseModel):
    name_order: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None


class CreateCategory(BaseModel):
    name: str
    description: str


class UpdateCategory(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

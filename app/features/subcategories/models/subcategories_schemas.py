from typing import Optional
from pydantic import BaseModel, Field


class SubcategoriesFiltersSchema(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    category_order: Optional[int] = None
    status: Optional[int] = None
    name_order: Optional[str] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class CreateSubcategorySchema(BaseModel):
    category_id: int
    subcategory_name: str


class UpdateSubcategorySchema(BaseModel):
    category_id: Optional[int] = None
    subcategory_name: Optional[str] = None

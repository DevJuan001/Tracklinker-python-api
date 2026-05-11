from typing import Optional
from pydantic import BaseModel


class SubcategoriesFiltersSchema(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    category_order: Optional[int] = None
    status: Optional[int] = None
    name_order: Optional[str] = None


class CreateSubcategorySchema(BaseModel):
    category_id: int
    subcategory_name: str


class UpdateSubcategorySchema(BaseModel):
    category_id: Optional[int] = None
    subcategory_name: Optional[str] = None

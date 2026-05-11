from typing import Optional
from pydantic import BaseModel


class SubcategoriesFiltersSchema(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    category_order: Optional[int] = None
    status: Optional[int] = None
    name_order: Optional[str] = None


class CreateSubcategorySchema(BaseModel):
    subcategory_name: str
    category_id: int


class UpdateSubcategorySchema(BaseModel):
    subcategory_name: str
    category_id: int

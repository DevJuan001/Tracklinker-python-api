from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, Field

from app.utils.safe_types import safe_optional_str, safe_str


class SubcategoriesFiltersSchema(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category_order: Optional[int] = None
    status: Optional[int] = None
    name_order: Optional[Literal["asc", "desc"]] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class CreateSubcategorySchema(BaseModel):
    category_id: int
    subcategory_name: str = safe_str(min_length=3, max_length=356)


class UpdateSubcategorySchema(BaseModel):
    category_id: Optional[int] = None
    subcategory_name: Optional[str] = safe_optional_str(
        min_length=3, max_length=356
    )

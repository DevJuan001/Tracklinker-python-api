from typing import Optional
from pydantic import BaseModel, Field
from app.utils.safe_str import safe_str, safe_optional_str


class CategoriesFiltersSchema(BaseModel):
    name_order: Optional[str] = safe_optional_str(max_length=100)
    start_date: Optional[str] = safe_optional_str(max_length=100)
    end_date: Optional[str] = safe_optional_str(max_length=100)
    status: Optional[int] = None
    search: Optional[str] = safe_optional_str(max_length=100)
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class CreateCategorySchema(BaseModel):
    name: str = safe_str(max_length=100)
    description: str = safe_str(max_length=255)


class UpdateCategorySchema(BaseModel):
    name: Optional[str] = safe_optional_str(max_length=100)
    description: Optional[str] = safe_optional_str(max_length=255)

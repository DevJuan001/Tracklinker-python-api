

from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field

from app.utils.safe_types import safe_optional_str, safe_str


class FilterSuppliersSchema(BaseModel):
    name_order: Optional[Literal["asc", "desc"]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[int] = None
    city: Optional[int] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class CreateSupplierSchema(BaseModel):
    name: str = safe_str(min_length=3, max_length=356)
    city: int
    address: str = safe_str(min_length=3, max_length=356)
    email: EmailStr = safe_str(max_length=254)
    phone: int


class UpdateSupplierSchema(BaseModel):
    name: Optional[str] = safe_optional_str(min_length=3, max_length=356)
    city: Optional[int] = None
    address: Optional[str] = safe_optional_str(min_length=3, max_length=356)
    email: Optional[EmailStr] = safe_optional_str(max_length=254)
    phone: Optional[int] = None

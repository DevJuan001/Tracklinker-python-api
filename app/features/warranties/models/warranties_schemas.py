from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

from app.utils.safe_types import safe_optional_str, safe_str


class WarrantiesFilterSchema(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    city: Optional[int] = None
    status: Optional[int] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class CreateWarrantySchema(BaseModel):
    product_serial: str = safe_str(min_length=3, max_length=356)
    customer: int
    phone: str = safe_str(min_length=3, max_length=356)
    address: str = safe_str(min_length=3, max_length=400)
    description: str = safe_str(min_length=3, max_length=1000)
    link_attachments: str = safe_str(min_length=3, max_length=1000)
    city: int


class UpdateWarrantySchema(BaseModel):
    product_serial: str = safe_str(min_length=3, max_length=356)
    customer: Optional[int] = None
    phone: Optional[str] = safe_optional_str(min_length=3, max_length=356)
    address: Optional[str] = safe_optional_str(min_length=3, max_length=400)
    description: Optional[str] = safe_optional_str(
        min_length=3, max_length=1000
    )
    link_attachments: Optional[str] = safe_optional_str(
        min_length=3, max_length=1000
    )
    city: Optional[int] = None
    status: Optional[int] = None

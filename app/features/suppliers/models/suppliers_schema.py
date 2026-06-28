

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class FilterSuppliersSchema(BaseModel):
    name_order: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None
    city: Optional[int] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class CreateSupplierSchema(BaseModel):
    name: str
    city: int
    address: str
    email: EmailStr
    phone: int


class UpdateSupplierSchema(BaseModel):
    name: Optional[str] = None
    city: Optional[int] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None

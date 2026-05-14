

from typing import Optional
from pydantic import BaseModel, EmailStr


class FilterSuppliersSchema(BaseModel):
    name_order: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None
    city: Optional[int] = None


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

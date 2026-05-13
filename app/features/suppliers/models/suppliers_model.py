from pydantic import BaseModel, EmailStr
from typing import Optional


class Supplier(BaseModel):
    name: str
    city: int
    address: str
    email: EmailStr
    phone: int


class UpdateSupplier(BaseModel):
    name: Optional[str] = None
    city: Optional[int] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None

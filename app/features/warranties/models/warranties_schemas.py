from typing import Optional
from pydantic import BaseModel


class WarrantiesFilterSchema(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    city: Optional[int] = None
    status: Optional[int] = None


class CreateWarrantySchema(BaseModel):
    product_serial: str
    customer: int
    phone: str
    address: str
    description: str
    link_attachments: str
    city: int


class UpdateWarrantySchema(BaseModel):
    product_serial: str
    customer: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    link_attachments: Optional[str] = None
    city: Optional[int] = None
    status: Optional[int] = None

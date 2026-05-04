from pydantic import BaseModel
from typing import Optional


class Warranty(BaseModel):
    id: int
    product_serial: str
    customer: str
    phone: str
    address: str
    description: str
    link_attachments: str
    city: int
    city_name: str
    date: str
    status: int

class WarrantiesFilter(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    city: Optional[int] = None
    status: Optional[int] = None

class CreateWarranty(BaseModel):
    product_serial: str
    customer: str
    phone: str
    address: str
    description: str
    link_attachments: str
    city: int


class WarrantyUpdate(BaseModel):
    product_serial: str
    customer: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    link_attachments: Optional[str] = None
    city: Optional[int] = None
    status: Optional[int] = None

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
    status: Optional[int] = None

class CreateWarranty(BaseModel):
    product_serial: str
    warranty_customer: str
    warranty_phone: str
    warranty_address: str
    warranty_description: str
    warranty_link_attachments: str
    warranty_city: str


class WarrantyUpdate(BaseModel):
    product_serial: str
    warranty_customer: Optional[str] = None
    warranty_phone: Optional[str] = None
    warranty_address: Optional[str] = None
    warranty_description: Optional[str] = None
    warranty_link_attachments: Optional[str] = None
    warranty_city: Optional[str] = None
    warranty_status: Optional[int] = None

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Warranty(BaseModel):
    warranty_incidents_id: Optional[int] = None
    product_serial: str
    warranty_customer: str
    warranty_phone: str
    warranty_address: str
    warranty_description: str
    warranty_link_attachments: str
    warranty_city: str
    warranty_date: Optional[datetime] = None
    warranty_status:  Optional[int] = None


class WarrantyUpdate(BaseModel):
    product_serial: str
    warranty_customer: str
    warranty_phone: str
    warranty_address: str
    warranty_description: str
    warranty_link_attachments: str
    warranty_city: str
    warranty_status: int

from typing import Optional
from pydantic import BaseModel

from app.utils.base_schema import BaseSchema


class WarrantyResponse(BaseModel):
    id: int
    product_serial: str
    customer: str
    created_by: str
    assigned_to: Optional[str] = None
    phone: str
    address: str
    description: str
    link_attachments: str
    city: int
    city_name: str
    date: str
    status: int


class RecentWarrantyResponse(BaseSchema):
    serial: str
    customer: str
    description: str
    date: str
    status: int


class WarrantyByBrandResponse(BaseModel):
    brand: str
    warranties: int


class WarrantyByStatusResponse(BaseModel):
    total_warranties: int
    without_make_warranties: int
    inprocess_warranties: int
    complete_warranties: int


class WarrrantyGrowthResponse(BaseSchema):
    date: str
    warranties: int

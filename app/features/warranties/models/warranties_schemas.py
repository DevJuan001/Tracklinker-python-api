from typing import Optional
from pydantic import BaseModel, Field


class WarrantiesFilterSchema(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    city: Optional[int] = None
    status: Optional[int] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


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

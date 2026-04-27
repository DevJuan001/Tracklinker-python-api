from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Product(BaseModel):
    input_order: int
    subcategory: int
    serial: str
    model: int
    warranty_time: int


class UpdateProduct(BaseModel):
    id: int
    product_details_id: int
    input_order: Optional[int] = None
    subcategory: Optional[int] = None
    serial: Optional[str] = None
    brand: Optional[int] = None
    model: Optional[int] = None
    warranty_time: Optional[datetime] = None
    status: Optional[int] = None

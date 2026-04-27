from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductSerial(BaseModel):
    serial: str
    product_id: int
    input_order: int
    warranty_time: int


class UpdateProductSerial(BaseModel):
    id: int
    serial: Optional[str] = None
    input_order: Optional[int] = None
    warranty_time: Optional[datetime] = None

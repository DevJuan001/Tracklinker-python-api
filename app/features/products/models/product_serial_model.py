from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateProductSerial(BaseModel):
    product_serial: str
    product_id: int
    input_order_id: int
    warranty_time: int


class UpdateProductSerial(BaseModel):
    id: int
    product_serial: Optional[str] = None
    input_order: Optional[int] = None
    warranty_time: Optional[datetime] = None

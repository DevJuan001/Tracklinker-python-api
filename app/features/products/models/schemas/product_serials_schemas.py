from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CreateProductSerialSchema(BaseModel):
    product_serial: str
    product_id: int
    input_order_id: int
    warranty_time: int

class UpdateProductSerialSchema(BaseModel):
    product_id: int
    product_serial: Optional[str] = None
    input_order: Optional[int] = None
    warranty_time: Optional[datetime] = None

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.utils.safe_types import safe_optional_str, safe_str


class CreateProductSerialSchema(BaseModel):
    product_serial: str = safe_str(min_length=3, max_length=356)
    product_id: int
    input_order_id: int
    warranty_time: int


class UpdateProductSerialSchema(BaseModel):
    product_id: int
    product_serial: Optional[str] = safe_optional_str(
        min_length=3, max_length=356
    )
    input_order: Optional[int] = None
    warranty_time: Optional[datetime] = None

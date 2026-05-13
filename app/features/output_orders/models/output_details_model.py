from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class CreateOutputDetails(BaseModel):
    product_serial: str
    output_product_garanty: datetime


class UpdateOutputDetails(BaseModel):
    product_serial: Optional[str] = None
    output_product_garanty: Optional[datetime] = None

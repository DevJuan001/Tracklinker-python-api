from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OutputOrdersFiltersSchema(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None


class CreateOutputOrderSchema(BaseModel):
    product_serials: list[str]
    output_product_garanty: datetime


class UpdateOutputOrderSchema(BaseModel):
    output_order_status: Optional[int] = None
    product_serial: Optional[str] = None
    output_product_garanty: Optional[datetime] = None

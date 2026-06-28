from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OutputOrdersFiltersSchema(BaseModel):
    client_id: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class CreateOutputOrderSchema(BaseModel):
    client_id: int
    product_serials: list[str]
    output_product_garanty: datetime


class UpdateOutputOrderSchema(BaseModel):
    output_order_status: Optional[int] = None
    product_serials: Optional[list[str]] = None
    output_product_garanty: Optional[datetime] = None

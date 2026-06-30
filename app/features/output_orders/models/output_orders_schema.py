from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.utils.safe_str import safe_optional_str


class OutputOrdersFiltersSchema(BaseModel):
    client_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
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

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateOutputOrder(BaseModel):
    product_serial: str
    product_details_id: int
    out_product_garanty: datetime
    product_transformation: str

class OutputOrdersFilters(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None

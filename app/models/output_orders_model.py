from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OutputOrder(BaseModel):
    out_order_id: Optional[int] = None
    out_order_date: Optional[datetime] = None
    product_details_id: int
from pydantic import BaseModel
from typing import Optional

class InputOrder(BaseModel):
    input_order_id: Optional[int] = None
    input_order_bill: str
    supplier_id: int
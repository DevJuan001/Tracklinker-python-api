import datetime
from typing import Optional
from pydantic import BaseModel


class UpdateOutputOrderModel(BaseModel):
    output_order_status: Optional[int] = None

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OutputDetails(BaseModel):
    product_serial: str 
    output_details_id: Optional[int] = None
    out_product_garanty: datetime
    product_transformation: str
   
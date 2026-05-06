from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class OutputOrdersFilters(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None

class OutputOrder(BaseModel):
    output_order_id: int
    output_order_date: str
    output_order_status: int
    output_details_id: int
    product_serial: str
    output_product_garanty: str
    product_transformation: str
    product_model_name:str
    product_model_description: str
    product_brand_name: str

class CreateOutputOrder(BaseModel):
    product_serial: str
    output_product_garanty: datetime
    product_transformation: str


class UpdateOutputOrder(BaseModel):
    output_order_status: Optional[int] = None
    product_serial: Optional[str] = None
    output_product_garanty: Optional[datetime] = None
    product_transformation: Optional[str] = None

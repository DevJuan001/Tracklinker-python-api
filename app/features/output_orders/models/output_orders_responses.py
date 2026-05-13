from datetime import date
from pydantic import BaseModel


class OutputOrderResponse(BaseModel):
    output_order_id: int
    output_order_date: str
    output_order_status: int
    output_details_id: int
    product_serial: str
    output_product_garanty: date
    product_brand_name: str
    product_model_name: str
    product_model_description: str
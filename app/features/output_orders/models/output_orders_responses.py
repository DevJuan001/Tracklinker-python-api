from datetime import date
from pydantic import BaseModel

from app.utils.base_schema import BaseSchema


class OutputOrderProductResponse(BaseModel):
    output_details_id: int
    product_serial: str
    output_product_garanty: str
    product_brand_name: str
    product_model_name: str


class OutputOrderResponse(BaseModel):
    output_order_id: int
    output_order_date: str
    output_order_status: int
    products: list[OutputOrderProductResponse] = []


class RecentOutputOrderResponse(BaseSchema):
    id: int
    serial: str
    brand: str
    model: str
    warranty_time: str
    date: str
    status: int


class OutputOrderByBrandResponse(BaseModel):
    brand: str
    outputs: int


class OutputOrderByStatusResponse(BaseModel):
    total_outputs: int
    recent_outputs: int
    inactive_outputs: int
    active_outputs: int


class OutputOrderGrowthResponse(BaseSchema):
    date: str
    output_orders: int

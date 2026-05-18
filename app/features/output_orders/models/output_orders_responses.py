from datetime import date
from typing import Union
from pydantic import BaseModel

from app.utils.base_schema import BaseSchema


class OutputOrderResponse(BaseModel):
    output_order_id: int
    output_order_date: str
    output_order_status: int
    product_serial: str
    output_product_garanty: date
    product_brand_name: str
    product_model_name: str
    product_model_description: str


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
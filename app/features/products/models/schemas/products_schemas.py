from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.utils.safe_types import safe_list_str, safe_optional_str, safe_str


class ProductsFilterSchema(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    input_order: Optional[int] = None
    category_order: Optional[int] = None
    subcategory_order: Optional[int] = None
    warranty_time: Optional[int] = None
    product_status: Optional[int] = None
    brand: Optional[int] = None
    product_model: Optional[int] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class UpdateProductSchema(BaseModel):
    id: int
    product_details_id: int
    input_order_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    product_serial: Optional[str] = safe_optional_str(
        min_length=3, max_length=356
    )
    brand_id: Optional[int] = None
    model_id: Optional[int] = None
    warranty_time: Optional[datetime] = None
    status: Optional[int] = None


class CreateProductSchema(BaseModel):
    brand_id: int
    input_order_id: int
    subcategory_id: int
    product_serials: list[str] = safe_list_str(
        min_items=1, min_length=3, max_length=256
    )
    model_id: int
    warranty_time: int


class UpdateProductStatusSchema(BaseModel):
    product_id: int
    product_serial: str = safe_str(min_length=3, max_length=256)
    status: int

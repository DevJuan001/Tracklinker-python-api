from datetime import date
from pydantic import BaseModel

from app.utils.base_schema import BaseSchema


class ProductResponse(BaseModel):
    input_order_id: int
    input_date: str
    input_order: str
    category: str
    subcategory_id: int
    subcategory: str
    product_id: int
    supplier: str
    product_serial: str
    model: str
    model_id: int
    description: str
    brand_id: int
    brand: str
    warranty_time: date
    product_details_id: int
    status: int

class ProductStatusResponse(BaseModel):
    id: int


class RecentProductsResponse(BaseModel):
    input_date: str
    serial: str
    model: str
    brand: str
    status: int


class ProductsByStatus(BaseModel):
    recent_products: int
    total_products: int
    warranties_products: int
    sold_products: int


class ProductsGrowthResponse(BaseSchema):
    date: str = None
    products: int


class ProductsByBrandResponse(BaseModel):
    brand: str
    products: int

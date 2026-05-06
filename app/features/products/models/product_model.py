from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class Product(BaseModel):
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
    


class ProductsFilter(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    input_order: Optional[int] = None
    category_order: Optional[int] = None
    subcategory_order: Optional[int] = None
    warranty_time: Optional[int] = None
    product_status: Optional[int] = None
    brand: Optional[int] = None
    product_model: Optional[int] = None


class UpdateProduct(BaseModel):
    id: int
    product_details_id: int
    input_order_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    product_serial: Optional[str] = None
    brand_id: Optional[int] = None
    model_id: Optional[int] = None
    warranty_time: Optional[datetime] = None
    status: Optional[int] = None

class CreateProduct(BaseModel):
    brand_id: int
    input_order_id: int
    subcategory_id: int
    product_serial: str
    model_id: int
    warranty_time: int

class UpdateProductStatus(BaseModel):
    product_id: int
    product_serial: str
    status: int
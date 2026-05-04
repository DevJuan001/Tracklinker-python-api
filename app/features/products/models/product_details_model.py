from pydantic import BaseModel
from typing import Optional


class CreateProductDetails(BaseModel):
    product_details_id: Optional[int] = None
    model: int


class UpdateProductDetails(BaseModel):
    model: int
    product_details_id: int

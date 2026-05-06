from pydantic import BaseModel
from typing import Optional


class CreateProductDetails(BaseModel):
    product_details_id: Optional[int] = None
    model_id: int


class UpdateProductDetails(BaseModel):
    model_id: int
    product_details_id: int

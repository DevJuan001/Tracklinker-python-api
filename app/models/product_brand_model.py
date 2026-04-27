from pydantic import BaseModel
from typing import Optional

class ProductBrand(BaseModel):
    product_brand_id: Optional[int] = None
    product_brand_name: str
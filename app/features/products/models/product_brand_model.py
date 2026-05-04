from pydantic import BaseModel
from typing import Union

class ProductBrand(BaseModel):
    subcategories: Union[dict, int, str]
    id: int
    name: str

class CreateProductBrand(BaseModel):
    name: str
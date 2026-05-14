from typing import Union
from pydantic import BaseModel


class ProductBrandResponse(BaseModel):
    subcategories: Union[dict, int, str]
    id: int
    name: str

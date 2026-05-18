from typing import Optional, Union
from pydantic import BaseModel


class ProductBrandResponse(BaseModel):
    subcategories: Optional[Union[dict, int, str]]
    id: int
    name: str

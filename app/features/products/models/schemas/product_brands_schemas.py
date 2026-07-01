from pydantic import BaseModel

from app.utils.safe_types import safe_str


class CreateProductBrandSchema(BaseModel):
    name: str = safe_str(min_length=3, max_length=356)

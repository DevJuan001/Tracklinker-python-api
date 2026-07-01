from pydantic import BaseModel

from app.utils.safe_types import safe_str


class CreateProductModelSchema(BaseModel):
    brand_id: int
    model: str = safe_str(min_length=3, max_length=356)
    description: str = safe_str(min_length=3)

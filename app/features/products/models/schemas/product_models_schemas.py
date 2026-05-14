from pydantic import BaseModel


class CreateProductModelSchema(BaseModel):
    brand_id: int
    model: str
    description: str

from pydantic import BaseModel


class ProductModel(BaseModel):
    brand: int
    id: int
    model: str


class CreateProductModel(BaseModel):
    brand_id: int
    model: str
    description: str

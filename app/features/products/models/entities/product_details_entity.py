from pydantic import BaseModel


class CreateProductDetailsEntity(BaseModel):
    model_id: int


class UpdateProductDetailsEntity(BaseModel):
    model_id: int
    product_details_id: int
from pydantic import BaseModel


class ProductModelResponse(BaseModel):
    brand: int
    id: int
    model: str

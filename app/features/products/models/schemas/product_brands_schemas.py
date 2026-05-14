from pydantic import BaseModel


class CreateProductBrandSchema(BaseModel):
    name: str
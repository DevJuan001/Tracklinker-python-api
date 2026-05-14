from pydantic import BaseModel


class CreateInputOrderSchema(BaseModel):
    input_order_bill: str
    supplier_id: int

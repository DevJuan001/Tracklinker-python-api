from pydantic import BaseModel

class InputOrder(BaseModel):
    id: int
    bill: str

class CreateInputOrder(BaseModel):
    input_order_bill: str
    supplier_id: int
from pydantic import BaseModel

from app.utils.safe_types import safe_str


class CreateInputOrderSchema(BaseModel):
    input_order_bill: str = safe_str(min_length=3, max_length=256)
    supplier_id: int

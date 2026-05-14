from pydantic import BaseModel


class InputOrderResponse(BaseModel):
    id: int
    bill: str
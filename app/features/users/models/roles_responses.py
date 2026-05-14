from pydantic import BaseModel


class RolResponse(BaseModel):
    id: int
    name: str

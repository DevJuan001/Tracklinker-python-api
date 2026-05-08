from pydantic import BaseModel


class Rol(BaseModel):
    id: int
    name: str

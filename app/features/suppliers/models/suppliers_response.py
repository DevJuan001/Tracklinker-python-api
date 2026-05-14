from pydantic import BaseModel, EmailStr


class SupplierResponse(BaseModel):
    id: int
    name: str
    city_id: int
    city_name: str
    address: str
    email: EmailStr
    phone: str
    status: int
    date: str

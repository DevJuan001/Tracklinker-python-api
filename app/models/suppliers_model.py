from pydantic import BaseModel, EmailStr

class Supplier(BaseModel):
    supplier_name: str
    supplier_city: str
    supplier_address: str
    supplier_email: EmailStr
    supplier_phone: int
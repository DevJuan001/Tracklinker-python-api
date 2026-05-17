from pydantic import BaseModel, EmailStr

from app.utils.base_schema import BaseSchema


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


class RecentSupplierResponse(BaseModel):
    name: str
    city: str
    address: str
    email: str
    phone: str
    date: str
    status: int


class SupplierByBrandResponse(BaseModel):
    brand: str
    suppliers: int


class SupplierByStatusResponse(BaseModel):
    total_suppliers: int
    recent_suppliers: int
    inactive_suppliers: int
    active_suppliers: int


class SupplierGrowthResponse(BaseSchema):
    date: str
    suppliers: int

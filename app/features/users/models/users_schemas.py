from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field

from app.utils.safe_types import safe_optional_str, safe_str


class UsersFiltersSchema(BaseModel):
    role_order: Optional[int] = None
    name_order: Optional[Literal["asc", "desc"]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[int] = None
    city: Optional[int] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class CreateUserSchema(BaseModel):
    role_id: int
    name: str = safe_str(min_length=3, max_length=256)
    first_surname: str = safe_str(min_length=3, max_length=256)
    second_surname: str = safe_str(min_length=3, max_length=256)
    address: str = safe_str(min_length=3, max_length=500)
    city: int
    email: EmailStr = safe_str(max_length=254)
    phone: int


class CreateClientSchema(BaseModel):
    name: str = safe_str(min_length=3, max_length=256)
    first_surname: str = safe_str(min_length=3, max_length=256)
    second_surname: str = safe_str(min_length=3, max_length=256)
    address: str = safe_str(min_length=3, max_length=500)
    city: int
    email: EmailStr = safe_str(max_length=254)
    phone: int


class UpdateUserSchema(BaseModel):
    role_id: Optional[int] = None
    name: Optional[str] = safe_optional_str(min_length=3, max_length=256)
    first_surname: Optional[str] = safe_optional_str(
        min_length=3, max_length=256
    )
    second_surname: Optional[str] = safe_optional_str(
        min_length=3, max_length=256
    )
    address: Optional[str] = safe_optional_str(min_length=3, max_length=500)
    city: Optional[int] = None
    email: Optional[EmailStr] = safe_optional_str(max_length=254)
    phone: Optional[int] = None
    status: Optional[int] = None


class UpdateCurrentUserSchema(BaseModel):
    name: Optional[str] = safe_optional_str(
        min_length=3, max_length=256
    )
    first_surname: Optional[str] = safe_optional_str(
        min_length=3, max_length=256
    )
    second_surname: Optional[str] = safe_optional_str(
        min_length=3, max_length=256
    )
    address: Optional[str] = safe_optional_str(
        min_length=3, max_length=500
    )
    city: Optional[int] = None
    email: Optional[EmailStr] = safe_optional_str(max_length=254)
    phone: Optional[int] = None


class UpdatePasswordSchema(BaseModel):
    old_password: str = safe_str(min_length=8, max_length=254)
    new_password: str = safe_str(min_length=8, max_length=254)
    repeat_password: str = safe_str(min_length=8, max_length=254)

from typing import Optional
from pydantic import BaseModel, EmailStr


class UsersFiltersSchema(BaseModel):
    role_order: Optional[int] = None
    name_order: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None
    city: Optional[int] = None


class CreateUserSchema(BaseModel):
    role_id: int
    name: str
    first_surname: str
    second_surname: str
    address: str
    city: int
    email: EmailStr
    phone: int


class CreateClientSchema(BaseModel):
    name: str
    first_surname: str
    second_surname: str
    address: str
    city: int
    email: EmailStr
    phone: int


class UpdateUserSchema(BaseModel):
    role_id: Optional[int] = None
    name: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    address: Optional[str] = None
    city: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None
    status: Optional[int] = None


class UpdateCurrentUserSchema(BaseModel):
    name: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    address: Optional[str] = None
    city: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None


class UpdatePasswordSchema(BaseModel):
    old_password: str
    new_password: str
    repeat_password: str

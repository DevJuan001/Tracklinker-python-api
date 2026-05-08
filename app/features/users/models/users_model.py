from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    rol_id: int
    rol_name: str
    id: int
    name: str
    first_surname: str
    second_surname: str
    phone: int
    email: EmailStr
    address: str
    city: int
    city_name: str
    date: str
    status:int

class CurrentUser(BaseModel):
    name: str
    first_surname: str
    second_surname: str
    phone: int
    email: EmailStr
    address: str
    city: int

class UsersFilters(BaseModel):
    role_order: Optional[int] = None
    name_order: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None
    city: Optional[int] = None


class CreateUser(BaseModel):
    rol_id: int
    name: str
    first_surname: str
    second_surname: str
    address: str
    city: int
    email: EmailStr
    phone: int


class UpdateUser(BaseModel):
    name: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    address: Optional[str] = None
    city: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None
    status: Optional[int] = None


class UpdateCurrentUser(BaseModel):
    name: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    address: Optional[str] = None
    city: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str
    repeat_password: str

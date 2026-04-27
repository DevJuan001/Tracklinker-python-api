from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    rol_id: int
    id: Optional[int] = None
    name: str
    first_surname: str
    second_surname: str
    address: str
    city: int
    email: EmailStr
    phone: int
    date: Optional[datetime] = None


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
    name: str
    first_surname: str
    second_surname: str
    address: str
    city: int
    email: EmailStr
    phone: int


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str
    repeat_password: str

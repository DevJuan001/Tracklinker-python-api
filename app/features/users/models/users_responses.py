from pydantic import BaseModel, EmailStr

from app.utils.base_schema import BaseSchema


class UserResponse(BaseModel):
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
    status: int


class CurrentUserResponse(BaseModel):
    id: int
    name: str
    first_surname: str
    second_surname: str
    phone: int
    email: EmailStr
    address: str
    city: int


class RecentUserResponse(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: int
    date: str
    status: int


class UsersGrowthResponse(BaseSchema):
    date: str = None
    users: int


class UsersByRolResponse(BaseModel):
    rol: str
    users: int


class UsersByStatusResponse(BaseModel):
    recent_users: int
    active_users: int
    inactive_users: int
    total_users: int

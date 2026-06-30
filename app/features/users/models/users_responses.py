from pydantic import BaseModel, EmailStr

from app.utils.base_schema import BaseSchema


class UserResponse(BaseModel):
    role_id: int
    role_name: str
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


class UserByIdResponse(BaseModel):
    role: str
    id: int
    name: str
    first_surname: str
    second_surname: str
    phone: int
    email: EmailStr
    address: str
    city: int


class UserByEmailResponse(BaseModel):
    rol_name: str
    user_id: int
    user_name: str
    user_first_surname: str
    user_second_surname: str
    user_email: EmailStr
    user_password: str


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


class UsersByRoleResponse(BaseModel):
    role: str
    users: int


class UsersByStatusResponse(BaseModel):
    recent_users: int
    active_users: int
    inactive_users: int
    total_users: int

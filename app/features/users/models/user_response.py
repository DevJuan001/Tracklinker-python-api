from pydantic import BaseModel, EmailStr


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
    status:int

class CurrentUserResponse(BaseModel):
    id: int
    name: str
    first_surname: str
    second_surname: str
    phone: int
    email: EmailStr
    address: str
    city: int

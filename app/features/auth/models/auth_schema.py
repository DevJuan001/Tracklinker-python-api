from pydantic import BaseModel, EmailStr, Field
from app.utils.safe_str import safe_str


class LoginModelSchema(BaseModel):
    email: EmailStr = safe_str(max_length=254)
    password: str = Field(..., min_length=8, max_length=128)


class RecoverPasswordSchema(BaseModel):
    email: EmailStr = safe_str(max_length=254)

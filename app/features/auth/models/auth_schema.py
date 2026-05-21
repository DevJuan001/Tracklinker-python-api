from pydantic import BaseModel, EmailStr

class LoginModelSchema(BaseModel):
    email: EmailStr
    password: str

class RecoverPasswordSchema(BaseModel):
    email: EmailStr

class VerifyRoleModelSchema(BaseModel):
    roles: list[str]
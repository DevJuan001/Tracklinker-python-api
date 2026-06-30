from pydantic import BaseModel, EmailStr, Field, field_validator
from app.utils.safe_str import safe_str


_COMMON_PASSWORDS = {
    "password",
    "password1",
    "12345678",
    "123456789",
    "qwerty123",
    "abc12345",
    "admin123",
    "welcome1",
    "iloveyou1",
    "11111111",
}


class LoginModelSchema(BaseModel):
    email: EmailStr = safe_str(max_length=254)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("password", mode="after")
    @classmethod
    def _check_password(cls, value: str) -> str:
        if value.lower() in _COMMON_PASSWORDS:
            raise ValueError("Por favor elige una contraseña más segura.")
        if not any(c.isupper() for c in value):
            raise ValueError("La contraseña debe incluir al menos una mayúscula.")
        if not any(c.islower() for c in value):
            raise ValueError("La contraseña debe incluir al menos una minúscula.")
        if not any(c.isdigit() for c in value):
            raise ValueError("La contraseña debe incluir al menos un número.")
        return value


class RecoverPasswordSchema(BaseModel):
    email: EmailStr = safe_str(max_length=254)

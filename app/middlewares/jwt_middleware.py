from jose import jwt, JWTError
from fastapi import Cookie, HTTPException
from app.core.config import settings

# Función para verificar el token en todas las solicitudes protegidas
async def verify_jwt(access_token: str = Cookie(None)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido o expirado",
    )

    if not access_token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            access_token,
            settings.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id or not role:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return {
        "user_id": user_id,
        "role": role
    }

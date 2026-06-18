import jwt
from jwt.exceptions import PyJWTError
from fastapi import Cookie, HTTPException

from app.core.config import settings
from app.core.token_blacklist import is_blacklisted
from app.utils.logger import get_logger


logger = get_logger("jwt.middleware")


async def verify_jwt(access_token: str = Cookie(None)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido o expirado",
    )

    if not access_token:
        raise credentials_exception

    try:
        blacklisted = await is_blacklisted(access_token)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al verificar la blacklist: %s", e, exc_info=True)
        raise HTTPException(
            status_code=401,
            detail="No se pudo verificar el token",
        )

    if blacklisted:
        raise HTTPException(
            status_code=401,
            detail="Token invalidado. Inicia sesión nuevamente.",
        )

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

    except PyJWTError:
        raise credentials_exception

    return {
        "user_id": user_id,
        "role": role
    }

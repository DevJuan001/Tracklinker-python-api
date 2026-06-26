from datetime import timedelta

import jwt
from jwt import PyJWTError
from pydantic import EmailStr
from fastapi import Request, Response

from app.core.config import settings
from app.core.database import get_connection
from app.core.token_blacklist import add_to_blacklist, get_token_remaining_ttl
from app.utils.logger import get_logger
from app.core.exception import ServiceError
from app.tasks.email_tasks import recovery_password_email
from app.features.auth.models.auth_schema import VerifyRoleModelSchema
from app.features.users.repositories.users_repository import UsersRepository
from app.core.security import create_access_token, create_refresh_token, set_auth_cookies, verify_password

logger = get_logger("auth.service")


class AuthService:
    @staticmethod
    def login(email: EmailStr, password: str, response: Response):
        connection = get_connection()

        try:
            # Buscamos si el correo esta registrado
            error, user = UsersRepository.find_user_by_email(
                email, connection
            )

            if error or not user:
                raise ServiceError(error)

            # Validamos si la contraseña es la correcta
            success = verify_password(user[6], password)

            if not success:
                raise ServiceError("Contraseña incorrecta")

            # Tiempo en que expira el token
            expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)

            # Creación del token
            access_token = create_access_token({
                "sub": str(user[1]),
                "role": user[0]
            },
                expires_delta=expires
            )

            refresh_token = create_refresh_token({
                "sub": str(user[1]),
                "role": user[0]
            })

            set_auth_cookies(response, access_token, refresh_token)

            return None, True, "Inicio de sesión exitoso"

        except ServiceError as e:
            return e.message, False, "No autorizado"

        except Exception as e:
            logger.error("Error en login: %s", e, exc_info=True)
            return "No autorizado", False, None

    @staticmethod
    async def refresh_tokens(request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise ServiceError("Refresh token no encontrado")

        try:
            # Calculamos el tiempo que le queda para que expire
            ttl = get_token_remaining_ttl(refresh_token)

            # Agregamos el token con el tiempo que le queda de expiración a la blacklist
            added = await add_to_blacklist(refresh_token, ttl)

            if not added and ttl > 0:
                logger.warning(
                    "No se pudo blacklistear el refresh_token viejo en refresh_tokens"
                )

            payload = jwt.decode(
                refresh_token,
                settings.REFRESH_TOKEN_SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            user_id = payload.get("sub")

            if not user_id:
                raise ServiceError("Refresh token inválido")

            new_access_token = create_access_token({
                "sub": str(user_id),
                "role": payload.get("role")
            },
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
            )

            new_refresh_token = create_refresh_token({
                "sub": user_id,
                "role": payload.get("role")
            })

            set_auth_cookies(response, new_access_token, new_refresh_token)

            return None, True, "Tokens actualizados correctamente"

        except PyJWTError:
            raise ServiceError(
                "Refresh token expirado o inválido"
            )

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            logger.error("Error en refresh_tokens: %s", e, exc_info=True)
            return "Error al intentar refrescar los tokens", False, None

    @staticmethod
    def verify_roles(body: VerifyRoleModelSchema, payload: dict):
        try:
            user_role = payload.get("role")
            roles = body.roles

            if user_role not in roles:
                raise ServiceError("No autorizado")

            return None, True

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en verify_roles: %s", e, exc_info=True)
            return "Error al intentar verificar los roles", None

    @staticmethod
    async def logout(request: Request, response: Response):
        try:
            access_token = request.cookies.get("access_token")
            refresh_token = request.cookies.get("refresh_token")

            if access_token:
                # Calculamos el tiempo que le queda para que expire
                ttl = get_token_remaining_ttl(access_token)

                # Agregamos el token con el tiempo que le queda de expiración a la blacklist
                added = await add_to_blacklist(access_token, ttl)

                if not added and ttl > 0:
                    logger.warning(
                        "No se pudo blacklistear el access_token en logout"
                    )

            if refresh_token:
                # Calculamos el tiempo que le queda para que expire
                ttl = get_token_remaining_ttl(refresh_token)
                
                # Agregamos el token con el tiempo que le queda de expiración a la blacklist
                added = await add_to_blacklist(refresh_token, ttl)
                
                if not added and ttl > 0:
                    logger.warning(
                        "No se pudo blacklistear el refresh_token en logout"
                    )

            response.delete_cookie(
                key="access_token",
                path="/"
            )

            response.delete_cookie(
                key="refresh_token",
                path="/api/auth/refresh"
            )

            return None, True, "Sesión cerrada exitosamente"

        except Exception as e:
            logger.error("Error en logout: %s", e, exc_info=True)
            return "Error al intentar cerrar la sesión", False, None

    @staticmethod
    def recover_password(email: EmailStr):
        connection = get_connection()

        try:
            error, user = UsersRepository.find_user_by_email(
                email, connection
            )

            if user:
                recovery_password_email.delay(
                    user_email=email,
                    user_name=user[2]
                )

        except Exception:
            pass

        return True, "Correo enviado correctamente"

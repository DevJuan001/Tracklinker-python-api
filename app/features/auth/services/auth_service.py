from datetime import timedelta

from fastapi import Request, Response
from jose import JWTError, jwt
from pydantic import EmailStr

from app.core.config import settings
from app.core.exception import ServiceError
from app.core.security import create_access_token, create_refresh_token, set_auth_cookies, verify_password
from app.features.auth.models.auth_model import VerifyRoleModel
from app.features.users.services.users_service import UsersService
from app.tasks.email_tasks import recovery_password_email


class AuthService:
    @staticmethod
    def login(email: str, password: str, response: Response):
        try:
            error, user = UsersService.get_user_by_email(email)

            if error or not user:
                raise ServiceError(error)

            # Validación de los parametros recibidos
            verify_password(user[6], password)

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
            }
            )

            set_auth_cookies(response, access_token, refresh_token)

            return None, True, "Inicio de sesión exitoso"

        except ServiceError as e:
            return e.message, False, "No autorizado"

    @staticmethod
    def update_tokens(request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise ServiceError("Refresh token no encontrado")

        try:
            payload = jwt.decode(
                refresh_token,
                settings.REFRESH_TOKEN_SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")

            if not user_id:
                raise ServiceError("Refresh token inválido")

        except JWTError:
            raise ServiceError(
                "Refresh token expirado o inválido"
            )

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

    @staticmethod
    def verify_roles(body: VerifyRoleModel, payload: dict):
        try:
            user_role = payload.get("role")
            roles = body.roles

            if user_role not in roles:
                raise ServiceError("No autorizado")

            return None, True

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            return "Error al intentar verificar los roles", None

    @staticmethod
    def logout(response: Response):
        try:
            response.delete_cookie(key="access_token", path="/api")
            response.delete_cookie(key="refresh_token", path="/api/auth/refresh")
        
            return None, True, "Sesión cerrada exitosamente"

        except Exception as e:
            return "Error al intentar cerrar la sesión", False, None


    @staticmethod
    def recover_password(email: EmailStr):
        try:
            error, user = UsersService.get_user_by_email(email)

            if user:
                recovery_password_email.delay(
                    user_email=email,
                    user_name=user[2]
                )

        except Exception:
            pass

        return True, "Correo enviado correctamente"

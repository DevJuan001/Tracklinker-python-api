from datetime import timedelta
from jose import jwt, JWTError
from app.core.mail import config
from app.core.config import settings
from app.core.security import verify_password
from fastapi_mail import FastMail, MessageSchema
from fastapi import HTTPException, Response, Request
from app.features.users.services.users_service import UsersService
from app.core.security import set_auth_cookies, create_access_token, create_refresh_token


class AuthController:
    @staticmethod
    def login(email: str, password: str, response: Response):
        error, user = UsersService.get_user_by_email(email)

        # Validación de lo que retorna la función find_by_email
        if error or not user:
            raise HTTPException(
                status_code=401, detail="Usuario No encontrado"
            )

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

        return {
            "success": True,
            "message": "Inicio de sesion exitoso"
        }

    @staticmethod
    def refresh_token(request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise HTTPException(
                status_code=401, detail="Refresh token no encontrado")

        try:
            payload = jwt.decode(
                refresh_token,
                settings.REFRESH_TOKEN_SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")

            if not user_id:
                raise HTTPException(
                    status_code=401, detail="Refresh token inválido")

        except JWTError:
            raise HTTPException(
                status_code=401, detail="Refresh token expirado o inválido")

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

        return {
            "success": True,
            "message": "Tokens actualizados correctamente"
        }

    @staticmethod
    def verify_role(body: dict, payload: dict):
        user_role = payload.get("role")
        roles = body.get("roles", [])

        # Valida si el rol que hay dentro del jwt esta el lista de roles envaidos
        if user_role not in roles:
            raise HTTPException(status_code=403, detail="No autorizado")

        return {
            "success": True
        }

    @staticmethod
    def logout(response: Response):
        response.delete_cookie(key="access_token", path="/api")
        response.delete_cookie(key="refresh_token", path="/api/auth/refresh")

        return {
            "success": True,
            "message": "Sesion cerrada"
        }

    @staticmethod
    async def recover_user_password(email: str):
        user = UsersService.get_user_by_email(email)

        if not user:
            raise HTTPException(status_code=400, detail="Correo inválido")

        message = MessageSchema(
            subject="Recuperación de contraseña",
            recipients=[email],
            template_body={"name": user["user_name"]},
            subtype="html",
        )

        fm = FastMail(config)
        await fm.send_message(message, template_name="recover_password.html")

        return {
            "success": True,
            "messagge": "Correo enviado correctamente"
        }

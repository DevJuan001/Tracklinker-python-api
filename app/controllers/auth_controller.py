from fastapi import HTTPException, Response, Cookie, Request
from datetime import timedelta
from app.models.user_model import UpdateCurrentUser, UpdatePassword
from app.core.security import verify_password
from app.core.security import set_auth_cookies, create_access_token, create_refresh_token
from app.repository.user_repository import UserRepository
from app.core.config import settings
from jose import jwt, JWTError
from app.core.mail import config
from fastapi_mail import FastMail, MessageSchema


class AuthController:
    """
    Controlador de autenticaión

    Esta clase se encarga de gestionar las operaciones relacionadas con
    la autenticación por el momento solo maneja una que sería el inicio de sesión "Login".

    Metodos:
        login(email: str, password: str):
            Verifica las credenciales del usuario y retorna un JWT para que pueda realizar
            o acceder a diferentes rutas.   

    Nota:
        Este controlador debe estar relacionado o integrarse con el repository el cual se comunica
        con la base de datos para poder validar las credenciales del usuario.
    """
    @staticmethod
    def login(email: str, password: str, response: Response):
        user = UserRepository.find_user_by_email(email)

        # Validación de lo que retorna la función find_by_email
        if not user:
            raise HTTPException(
                status_code=401, detail="Usuario No encontrado")

        # Validación de los parametros recibidos
        verify_password(user, password)

        # Tiempo en que expira el token
        expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)

        # Creación del token
        access_token = create_access_token({
            "sub": str(user["user_id"]),
            "role": user["rol_name"]
        },
            expires_delta=expires)

        refresh_token = create_refresh_token(
            {"sub": str(user["user_id"]),
             "role": user["rol_name"]}
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
        }, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE))

        new_refresh_token = create_refresh_token(
            {"sub": user_id, "role": payload.get("role")})

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
    def get_current_user(access_token: str = Cookie(None)):
        if not access_token:
            raise HTTPException(status_code=401, detail="No autenticado")

        try:
            token = access_token.replace("Bearer ", "")
            payload = jwt.decode(
                token,
                settings.ACCESS_TOKEN_SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            error, data = UserRepository.find_user_by_id(payload["sub"])

            if error:
                raise HTTPException(status_code=404, detail=error)

            return {
                "user": data[0]
            }
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")

    @staticmethod
    def update_current_user(user_data: UpdateCurrentUser, payload: dict):
        error, success, message = UserRepository.update_current_user(
            int(payload["user_id"]), user_data)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_user_password(password_data: UpdatePassword, payload: dict):
        data = password_data.model_dump()

        if data["new_password"] != data["repeat_password"]:
            raise HTTPException(
                status_code=400, detail="Las contraseñas no coinciden")

        error, user = UserRepository.find_user_password_by_id(int(payload["user_id"]))

        # Validación de lo que retorna la función find_by_email
        if not user or error:
            raise HTTPException(
                status_code=401, detail="Usuario No encontrado")

        # Validación de que la contraseña antigua sea valida
        verify_password(user[0], data["old_password"])

        error, success, message = UserRepository.update_password(
            int(payload["user_id"]), data["new_password"])

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    async def recover_user_password(email: str):
        user = UserRepository.find_user_by_email(email)

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

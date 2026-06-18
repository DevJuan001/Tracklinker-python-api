from fastapi import HTTPException, Request, Response
from pydantic import EmailStr

from app.features.auth.services.auth_service import AuthService
from app.features.auth.models.auth_schema import VerifyRoleModelSchema


class AuthController:
    @staticmethod
    def login(email: str, password: str, response: Response):
        error, success, message = AuthService.login(
            email, password, response
        )

        if error or not success:
            raise HTTPException(
                status_code=401, detail="Credenciales invalidas"
            )

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    async def refresh_tokens(request: Request, response: Response):
        error, success, message = await AuthService.refresh_tokens(
            request, response
        )

        if error or not success:
            raise HTTPException(
                status_code=401, detail=error
            )

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def verify_roles(body: VerifyRoleModelSchema, payload: dict):
        error, success = AuthService.verify_roles(
            body, payload
        )

        if error or not success:
            raise HTTPException(status_code=401, detail="No autorizado")

        return {
            "success": success
        }

    @staticmethod
    async def logout(request: Request, response: Response):
        error, success, message = await AuthService.logout(
            request, response
        )

        if error or not success:
            raise HTTPException(status_code=401, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    async def recover_password(email: EmailStr):
        success, message = AuthService.recover_password(
            email
        )

        return {
            "success": success,
            "message": message
        }

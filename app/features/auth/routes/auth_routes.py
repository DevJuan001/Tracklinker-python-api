from fastapi import APIRouter, Depends, Request, Response
from fastapi_limiter.depends import RateLimiter

from app.features.auth.controllers.auth_controller import AuthController
from app.features.auth.models.auth_schema import LoginModelSchema, RecoverPasswordSchema, VerifyRoleModelSchema
from app.middlewares.jwt_middleware import verify_jwt


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


# Endpoint para loguearse
@router.post(
    "/login",
    dependencies=[
        Depends(RateLimiter(times=3, seconds=60))
    ]
)
def login(credentials: LoginModelSchema, response: Response):
    return AuthController.login(credentials.email, credentials.password, response)


# Endpoint para actualizar el token de acceso
@router.post(
    "/refresh",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
    ]
)
async def refresh_tokens(request: Request, response: Response):
    return await AuthController.refresh_tokens(request, response)


# Endpoint para cerrar sesión
@router.post(
    "/logout",
    dependencies=[
        Depends(RateLimiter(times=50, seconds=60)),
    ]
)
async def logout(request: Request, response: Response):
    return await AuthController.logout(request, response)


# Endpoint para recuperar contraseña
@router.post(
    "/recover-password",
    dependencies=[
        Depends(RateLimiter(times=3, seconds=60)),
    ]
)
async def recover_password(data: RecoverPasswordSchema):
    return await AuthController.recover_password(data.email)

from fastapi_limiter.depends import RateLimiter
from fastapi import APIRouter, Body, Depends, Response, Request
from app.middlewares.jwt_middleware import verify_jwt
from app.middlewares.roles_middleware import require_roles
from app.features.auth.controllers.auth_controller import AuthController
from app.features.auth.models.auth_model import LoginModel, RecoverPassword

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
def login(credentials: LoginModel, response: Response):
    return AuthController.login(credentials.email, credentials.password, response)

# Endpoint para actualizar el token de acceso
@router.post(
    "/refresh",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
    ]
)
def refresh_token(request: Request, response: Response):
    return AuthController.refresh_token(request, response)

# Endpoint para verificar el rol del usuario
@router.post(
    "/verify-roles",
    dependencies=[
        Depends(RateLimiter(times=50, seconds=60)),
    ]
)
def verifyRole(body: dict = Body(...), payload: dict = Depends(verify_jwt)):
    return AuthController.verify_role(body, payload)

#Endpoint para cerrar sesión
@router.post("/logout")
def logout(response: Response):
    return AuthController.logout(response)

# Endpoint para recuperar contraseña
@router.post(
    "/recover-password",
    dependencies=[
        Depends(RateLimiter(times=3, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
async def recover_user_password(data: RecoverPassword):
    return await AuthController.recover_user_password(data.email)
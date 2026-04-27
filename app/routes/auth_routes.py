from fastapi import APIRouter, Depends, Response, Cookie, Body, Request
from app.controllers.auth_controller import AuthController
from app.models.auth_model import LoginModel, RecoverPassword
from app.models.user_model import UpdateCurrentUser, UpdatePassword
from app.middlewares.roles_middleware import require_roles
from app.middlewares.jwt_middleware import verify_jwt
from fastapi_limiter.depends import RateLimiter

router = APIRouter(
    prefix="/api/auth", 
    tags=["Auth"]
)

# Endpoint para loguearse
@router.post(
    "/login",
    dependencies=[
        Depends(RateLimiter(times=2, seconds=60))
    ]
)
def login(credentials: LoginModel, response: Response):
    return AuthController.login(credentials.email, credentials.password, response)

# Endpoint para actualizar el token de acceso
@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    return AuthController.refresh_token(request, response)

# Endpoint para verificar el rol del usuario
@router.post("/verify-roles")
def verifyRole(body: dict = Body(...), payload: dict = Depends(verify_jwt)):
    return AuthController.verify_role(body, payload)

#Endpoint para cerrar sesión
@router.post("/logout")
def logout(response: Response):
    return AuthController.logout(response)

#Endpoint para obtener la informacion del usuario
@router.get(
    "/me",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen", "Tecnico"]))
    ]
)
def get_me(access_token: str = Cookie(None)):
    return AuthController.get_current_user(access_token)

#Endpoint para actualizar la informacion del usuario
@router.put(
    "/update/me",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen", "Tecnico"]))
    ]
)
def update_me(user_data: UpdateCurrentUser = Body(...), payload: dict = Depends(verify_jwt)):
    return AuthController.update_current_user(user_data, payload)

# Endpoint para actulizar la contraseña del usuario
@router.put("/update-password")
def update_user_password(password_data: UpdatePassword, payload: dict = Depends(verify_jwt)):
    return AuthController.update_user_password(password_data, payload)

# Endpoint para recuperar contraseña
@router.post(
    "/recover-password",
    dependencies=[
        Depends(RateLimiter(times=3, seconds=60))
    ]
)
async def recover_user_password(data: RecoverPassword = Body(...)):
    return await AuthController.recover_user_password(data.email)
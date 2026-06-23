from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from app.middlewares.jwt_middleware import verify_jwt
from app.middlewares.roles_middleware import require_roles
from app.features.users.controllers.users_controller import UsersController
from app.features.users.models.users_schemas import CreateClientSchema, CreateUserSchema, UpdateCurrentUserSchema, UpdatePasswordSchema, UpdateUserSchema, UsersFiltersSchema

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


# Endpoint para obtener todos los usuarios
@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_all_users(filters: UsersFiltersSchema = Depends()):
    return UsersController.get_all_users(filters)


# Endpoint para obtener la información del usuario autenticado
@router.get(
    "/me",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
def get_me(payload: dict = Depends(verify_jwt)):
    return UsersController.get_current_user(payload)


# Endpoint para obtener todos los roles existentes
@router.get(
    "/roles",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_all_roles():
    return UsersController.get_all_roles()


# Endpoint para obtener todas las ciudades existentes
@router.get(
    "/cities",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
def get_all_cities():
    return UsersController.get_all_cities()


# Endpoint para obtener todos los clientes activos
@router.get(
    "/active-clients",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
def get_active_clients():
    return UsersController.get_active_clients()


# Endpoint para crear o registrar un cliente
@router.post(
    "/clients/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Técnico"]))
    ]
)
async def create_client(
    client_data: CreateClientSchema
):
    return await UsersController.create_client(client_data)


# Endpoint para obtener un usuario mediante el id
@router.get(
    "/{user_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_user_by_id(user_id: int):
    return UsersController.get_user_by_id(user_id)


# Endpoint para crear o registrar un usuario
@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
async def create_user(
    user_data: CreateUserSchema
):
    return await UsersController.create_user(user_data)


# Endpoint para actualizar la informacion del usuario
@router.put(
    "/update/me",
    dependencies=[
        Depends(RateLimiter(times=10, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
def update_me(user_data: UpdateCurrentUserSchema, payload: dict = Depends(verify_jwt)):
    return UsersController.update_current_user(user_data, payload)


# Endpoint para actualizar la contraseña del usuario
@router.put(
    "/update-password",
    dependencies=[
        Depends(RateLimiter(times=10, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
def update_user_password(password_data: UpdatePasswordSchema, payload: dict = Depends(verify_jwt)):
    return UsersController.update_user_password(password_data, payload)


# Endpoint para actualizar la información de un usuario existente mediante su id
@router.put(
    "/update/{user_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def update_user(
    user_id: int,
    user_data: UpdateUserSchema
):
    return UsersController.update_user(user_id, user_data)


# Endpoint para deshabilitar un usuario mediante su id
@router.put(
    "/disable/{user_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def disable_user(
    user_id: int
):
    return UsersController.disable_user(user_id)


# Endpoint para habilitar un usuario mediante su id
@router.put(
    "/enable/{user_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def enable_user(
    user_id: int
):
    return UsersController.enable_user(user_id)

from fastapi import APIRouter, Depends, Body
from app.controllers.user_controller import UserController
from app.models.user_model import User, UpdateUser
from app.middlewares.roles_middleware import require_roles
from fastapi_limiter.depends import RateLimiter

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

# Endpoint para obtener todos los roles existentes
@router.get(
    "/roles",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_all_roles():
    return UserController.get_all_roles()

#Endpoint para obtener todas las ciudades existentes
@router.get(
    "/cities",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_all_cities():
    return UserController.get_all_cities()

# Endpoint para obtener todos los usuarios
@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_all_users(
    role_order: int = None,
    name_order: str = None,
    start_date: str = None,
    end_date: str = None,
    status: int = None,
    city: int = None,
):
    return UserController.get_all_users(
        role_order,
        name_order,
        start_date,
        end_date,
        status,
        city,
    )

# Endpoint para obtener un usuario mediante el id
@router.get(
    "/{user_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_user_by_id(user_id: int):
    return UserController.get_user_by_id(user_id)

# Endpoint para crear o registrar un usuario
@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
async def create_user(
    user_data: User
):
    return await UserController.create_user(user_data)

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
    user_data: UpdateUser
):
    return UserController.update_user(user_id, user_data)

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
    return UserController.disable_user(user_id)

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
    return UserController.enable_user(user_id)
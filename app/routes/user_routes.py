from fastapi import APIRouter, Depends, Body
from app.controllers.user_controller import UserController
from app.models.user_model import User, UpdateUser
from app.middlewares.roles_middleware import require_roles

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

# Endpoint para obtener todos los roles existentes
@router.get("/roles")
def get_all_roles():
    return UserController.get_all_roles()

#Endpoint para obtener todas las ciudades existentes
@router.get("/cities")
def get_all_cities():
    return UserController.get_all_cities()

# Endpoint para obtener todos los usuarios
@router.get("/")
def get_all_users(
    role_order: int = None,
    name_order: str = None,
    start_date: str = None,
    end_date: str = None,
    status: int = None,
):
    return UserController.get_all_users(
        role_order,
        name_order,
        start_date,
        end_date,
        status
    )

# Endpoint para obtener un usuario mediante el id
@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    return UserController.get_user_by_id(user_id)

# Endpoint para crear o registrar un usuario
@router.post("/create")
async def create_user(
    user_data: User
):
    return await UserController.create_user(user_data)

# Endpoint para actualizar la información de un usuario existente mediante su id
@router.put("/update/{user_id}")
def update_user(
    user_id: int, 
    user_data: UpdateUser
):
    return UserController.update_user(user_id, user_data)

# Endpoint para deshabilitar un usuario mediante su id
@router.put("/disable/{user_id}")
def disable_user(
    user_id: int
):
    return UserController.disable_user(user_id)

# Endpoint para habilitar un usuario mediante su id
@router.put("/enable/{user_id}")
def enable_user(
    user_id: int
):
    return UserController.enable_user(user_id)
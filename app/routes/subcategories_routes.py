from fastapi import APIRouter
from app.controllers.subcategories_controller import SubcategoriesController
from fastapi import Depends
from app.middlewares.roles_middleware import require_roles


router = APIRouter(
    prefix="/api/subcategories",
    tags=["subcategories"]
)
# Endpoint para obtener todas las subcategorías


@router.get("/")
def get_all_subcategories(
    start_date: str = None,
    end_date: str = None,
    category_order: int = None,
    status: int = None,
    name_order: str = None,
):
    return SubcategoriesController.get_all_subcategories(
        start_date,
        end_date,
        category_order,
        status,
        name_order
    )

# Endpoint para obtener las categorias activas
@router.get("/categories")
def get_categories():
    return SubcategoriesController.get_categories()

# Endpoint para obtener una subcategoría mediante el id
@router.get("/{subcategory_id}")
def get_subcategory_by_id(subcategory_id: int):
    return SubcategoriesController.get_subcategory_by_id(subcategory_id)

# Endpoint para crear o registrar una subcategoría
@router.post("/create")
def create_subcategory(
    subcategory_data: dict,
    payload: dict = Depends(require_roles(["Admin"]))
):
    return SubcategoriesController.create_subcategory(subcategory_data)


# Endpoint para actualizar la información de una subcategoría existente mediante su id
@router.put("/update/{subcategory_id}")
def update_subcategory(
    subcategory_id: int,
    subcategory_data: dict,
    payload: dict = Depends(require_roles(["Admin"]))
):
    return SubcategoriesController.update_subcategory(subcategory_id, subcategory_data)


# Endpoint para deshabilitiar una subcategoría mediante su id
@router.put("/disable/{subcategory_id}")
def disable_subcategory(
    subcategory_id: int,
    payload: dict = Depends(require_roles(["Admin"]))
):
    return SubcategoriesController.disable_subcategory(subcategory_id)

# Endpoint para habilitar una subcategoría mediante su id
@router.put("/enable/{subcategory_id}")
def enable_subcategory(
    subcategory_id: int,
    payload: dict = Depends(require_roles(["Admin"]))
):
    return SubcategoriesController.enable_subcategory(subcategory_id)

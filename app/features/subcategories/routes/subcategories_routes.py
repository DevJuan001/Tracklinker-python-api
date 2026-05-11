from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.features.subcategories.controllers.subcategories_controller import SubcategoriesController
from app.features.subcategories.models.subcategories_schemas import CreateSubcategorySchema, SubcategoriesFiltersSchema, UpdateSubcategorySchema
from app.middlewares.roles_middleware import require_roles


router = APIRouter(
    prefix="/api/subcategories",
    tags=["subcategories"]
)


# Endpoint para obtener todas las subcategorías
@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_all_subcategories(filters: SubcategoriesFiltersSchema = Depends()):
    return SubcategoriesController.get_all_subcategories(filters)


# Endpoint para obtener las categorias activas
@router.get(
    "/categories",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_categories():
    return SubcategoriesController.get_categories()


# Endpoint para obtener una subcategoría mediante el id
@router.get(
    "/{subcategory_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_subcategory_by_id(subcategory_id: int):
    return SubcategoriesController.get_subcategory_by_id(subcategory_id)


# Endpoint para crear o registrar una subcategoría
@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def create_subcategory(
    subcategory_data: CreateSubcategorySchema,
):
    return SubcategoriesController.create_subcategory(subcategory_data)


# Endpoint para actualizar la información de una subcategoría existente mediante su id
@router.put(
    "/update/{subcategory_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def update_subcategory(
    subcategory_id: int,
    subcategory_data: UpdateSubcategorySchema,
):
    return SubcategoriesController.update_subcategory(subcategory_id, subcategory_data)


# Endpoint para deshabilitiar una subcategoría mediante su id
@router.put(
    "/disable/{subcategory_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def disable_subcategory(
    subcategory_id: int,
):
    return SubcategoriesController.disable_subcategory(subcategory_id)


# Endpoint para habilitar una subcategoría mediante su id
@router.put(
    "/enable/{subcategory_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def enable_subcategory(
    subcategory_id: int,
):
    return SubcategoriesController.enable_subcategory(subcategory_id)

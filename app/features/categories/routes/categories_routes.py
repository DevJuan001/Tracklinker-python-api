from fastapi import APIRouter, Depends
from app.middlewares.roles_middleware import require_roles
from fastapi_limiter.depends import RateLimiter
from app.features.categories.controllers.categories_controller import CategoriesController
from app.features.categories.models.categories_model import CategoriesFilters, CreateCategory, UpdateCategory

router = APIRouter(
    prefix="/api/categories",
    tags=["Categorías"]
)

# Endpoint para obtener todas las categorias


@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
def get_all_categories(filters: CategoriesFilters):
    return CategoriesController.get_all_categories(filters)

# Endpoint para obtener una categoria mediante el id


@router.get(
    "/{category_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
def get_category_by_id(category_id: int):
    return CategoriesController.get_category_by_id(category_id)


@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
def create_category(category_data: CreateCategory):
    return CategoriesController.create_category(category_data)


@router.put(
    "/update/{category_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
def update_category(category_id: int, category_data: UpdateCategory):
    return CategoriesController.update_category(category_id, category_data)


@router.put(
    "/disable/{category_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
def disable_category(category_id: int):
    return CategoriesController.disable_category(category_id)


@router.put(
    "/enable/{category_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
def enable_category(category_id: int):
    return CategoriesController.enable_category(category_id)

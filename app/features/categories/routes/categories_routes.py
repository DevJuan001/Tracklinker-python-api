import json
from fastapi import APIRouter, Depends
from app.core.redis import get_redis
from app.core.cache import get_cache, set_cache, invalidate_cache
from fastapi_limiter.depends import RateLimiter
from app.middlewares.roles_middleware import require_roles
from app.features.categories.controllers.categories_controller import CategoriesController
from app.features.categories.models.categories_schemas import CategoriesFiltersSchema, CreateCategorySchema, UpdateCategorySchema

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
async def get_all_categories(filters: CategoriesFiltersSchema = Depends(), redis=Depends(get_redis)):
    cache_key = f"categories:{json.dumps(filters.model_dump(), sort_keys=True)}"

    cached = await get_cache(redis, cache_key)
    if cached:
        return cached

    result = CategoriesController.get_all_categories(filters)

    await set_cache(redis, cache_key, result, 300)

    return result


# Endpoint para obtener las categorias activas
@router.get(
    "/active-categories",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
async def get_active_categories(redis=Depends(get_redis)):
    cache_key = "categories:active"

    cached = await get_cache(redis, cache_key)
    if cached:
        return cached

    result = CategoriesController.get_active_categories()

    await set_cache(redis, cache_key, result, 300)

    return result


# Endpoint para obtener una categoria mediante el id
@router.get(
    "/{category_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
async def get_category_by_id(category_id: int, redis=Depends(get_redis)):
    cache_key = f"categories:{category_id}"

    cached = await get_cache(redis, cache_key)
    if cached:
        return cached

    result = CategoriesController.get_category_by_id(category_id)

    await set_cache(redis, cache_key, result, 300)

    return result


# Endpoint para crear una categoría
@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
async def create_category(category_data: CreateCategorySchema, redis=Depends(get_redis)):
    result = CategoriesController.create_category(category_data)

    await invalidate_cache(redis, "categories:*")

    return result


# Endpoint para actualizar una categoría
@router.put(
    "/update/{category_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
async def update_category(category_id: int, category_data: UpdateCategorySchema, redis=Depends(get_redis)):
    result = CategoriesController.update_category(category_id, category_data)

    await invalidate_cache(redis, "categories:*")

    return result


# Endpoint para deshabilitar una categoría
@router.put(
    "/disable/{category_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
async def disable_category(category_id: int, redis=Depends(get_redis)):
    result = CategoriesController.disable_category(category_id)

    await invalidate_cache(redis, "categories:*")

    return result


# Endpoint para habilitar una categoría
@router.put(
    "/enable/{category_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
async def enable_category(category_id: int, redis=Depends(get_redis)):
    result = CategoriesController.enable_category(category_id)

    await invalidate_cache(redis, "categories:*")

    return result

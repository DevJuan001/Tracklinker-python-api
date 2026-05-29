import json
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.core.redis import get_redis
from app.core.cache import get_cache, invalidate_cache, set_cache
from app.middlewares.roles_middleware import require_roles
from app.features.subcategories.controllers.subcategories_controller import SubcategoriesController
from app.features.subcategories.models.subcategories_schemas import CreateSubcategorySchema, SubcategoriesFiltersSchema, UpdateSubcategorySchema


router = APIRouter(
    prefix="/api/subcategories",
    tags=["subcategories"]
)


# Endpoint para obtener todas las subcategorías
@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
async def get_all_subcategories(filters: SubcategoriesFiltersSchema = Depends(), redis=Depends(get_redis)):
    cache_key = f"subcategories:{json.dumps(filters.model_dump(), sort_keys=True)}"

    cached = await get_cache(redis, cache_key)
    if cached:
        return cached

    result = SubcategoriesController.get_all_subcategories(filters)

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
    cache_key = "subcategories:active"

    cached = await get_cache(redis, cache_key)
    if cached:
        return cached

    result = SubcategoriesController.get_active_categories()

    await set_cache(redis, cache_key, result, 300)

    return result


# Endpoint para obtener una subcategoría mediante el id
@router.get(
    "/{subcategory_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
async def get_subcategory_by_id(subcategory_id: int, redis=Depends(get_redis)):
    cache_key = f"subcategories:{subcategory_id}"

    cached = await get_cache(redis, cache_key)
    if cached:
        return cached

    result = SubcategoriesController.get_subcategory_by_id(subcategory_id)

    await set_cache(redis, cache_key, result, 300)

    return result


# Endpoint para crear o registrar una subcategoría
@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
async def create_subcategory(
    subcategory_data: CreateSubcategorySchema,
    redis=Depends(get_redis),
):
    result = SubcategoriesController.create_subcategory(subcategory_data)

    await invalidate_cache(redis, "subcategories:*")

    return result


# Endpoint para actualizar la información de una subcategoría existente mediante su id
@router.put(
    "/update/{subcategory_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
async def update_subcategory(
    subcategory_id: int,
    subcategory_data: UpdateSubcategorySchema,
    redis=Depends(get_redis),
):
    result = SubcategoriesController.update_subcategory(
        subcategory_id, subcategory_data
    )

    await invalidate_cache(redis, "subcategories:*")

    return result


# Endpoint para deshabilitiar una subcategoría mediante su id
@router.put(
    "/disable/{subcategory_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
async def disable_subcategory(
    subcategory_id: int,
    redis=Depends(get_redis),
):
    result = SubcategoriesController.disable_subcategory(subcategory_id)

    await invalidate_cache(redis, "subcategories:*")

    return result


# Endpoint para habilitar una subcategoría mediante su id
@router.put(
    "/enable/{subcategory_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén"]))
    ]
)
async def enable_subcategory(
    subcategory_id: int,
    redis=Depends(get_redis),
):
    result = SubcategoriesController.enable_subcategory(subcategory_id)

    await invalidate_cache(redis, "subcategories:*")

    return result

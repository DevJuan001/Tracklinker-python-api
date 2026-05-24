from app.core.redis import get_redis
from app.core.cache import invalidate_cache
from fastapi import APIRouter, Depends, Body
from fastapi_limiter.depends import RateLimiter
from app.middlewares.roles_middleware import require_roles
from app.features.products.controllers.products_controller import ProductsController
from app.features.products.models.schemas.input_orders_schemas import CreateInputOrderSchema
from app.features.products.models.schemas.product_brands_schemas import CreateProductBrandSchema
from app.features.products.models.schemas.product_models_schemas import CreateProductModelSchema
from app.features.products.models.schemas.products_schemas import CreateProductSchema, UpdateProductStatusSchema, UpdateProductSchema, ProductsFilterSchema

router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


# Endpoint para obtener todos los productos
@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Almacén", "Técnico"]))
    ]
)
async def get_all_products(
    filters: ProductsFilterSchema = Depends(),
    redis=Depends(get_redis)
):
    result = ProductsController.get_all_products(filters)
    return result


# Endpoint para obtener todas las marcas de productos
@router.get(
    "/brands",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén", "Técnico"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def get_all_brands():
    return ProductsController.get_all_product_brands()


# Endpoint para obtener todos los modelos de productos
@router.get(
    "/models",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén", "Técnico"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def get_all_models():
    return ProductsController.get_all_product_models()


# Endpoint para obtener las ordenes de entrada de productos
@router.get(
    "/input-orders",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén", "Técnico"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def get_all_input_orders():
    return ProductsController.get_all_input_orders()


# Endpoint para obtener las estados de los productos
@router.get(
    "/status",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén", "Técnico"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def get_all_product_status():
    return ProductsController.get_all_product_status()


# Endpoint para crear o agregar productos
@router.post(
    "/create",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
async def create_product(product_data: CreateProductSchema, redis=Depends(get_redis)):
    result = ProductsController.create_product(product_data)
    await invalidate_cache(redis, "products:*")
    return result


# Endpoint para crear o agregar modelos de productos
@router.post(
    "/create-model",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def create_product_model(product_model: CreateProductModelSchema):
    return ProductsController.create_product_model(product_model)


# Endpoint para crear una marca de producto
@router.post(
    "/create-brand",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def create_product_brand(product_brand: CreateProductBrandSchema):
    return ProductsController.create_product_brand(product_brand)


# Endpoint para crear una orden de entrada de productos
@router.post(
    "/create-input-order",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def create_product_entry(input_order: CreateInputOrderSchema):
    return ProductsController.create_input_order(input_order)


# Endpoint para actualizar la informacion de un producto
@router.put(
    "/update",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def update_product(product_data: UpdateProductSchema = Body(...)):
    return ProductsController.update_product(product_data)


# Endpoint para actualizar el estado de un producto
@router.put(
    "/update-status",
    dependencies=[
        Depends(require_roles(["Admin", "Almacén"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def update_product_status(product_data: UpdateProductStatusSchema):
    return ProductsController.update_product_status(product_data)

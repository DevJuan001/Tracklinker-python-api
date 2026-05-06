from app.core.redis import get_redis
from app.core.cache import invalidate_cache
from fastapi import APIRouter, Depends, Body
from fastapi_limiter.depends import RateLimiter
from app.middlewares.roles_middleware import require_roles
from app.features.products.models.input_order_model import CreateInputOrder
from app.features.products.models.product_brand_model import CreateProductBrand
from app.features.products.models.product_models_model import CreateProductModel
from app.features.products.controllers.products_controller import ProductsController
from app.features.products.models.product_model import CreateProduct, UpdateProductStatus, UpdateProduct, ProductsFilter

router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)

# Endpoint para obtener todos los productos
@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
async def get_all_products(
    filters: ProductsFilter = Depends(),
    redis=Depends(get_redis)
):
    result = ProductsController.get_all_products(filters)
    return result

# Endpoint para obtener todas las marcas de productos
@router.get(
    "/brands",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def get_all_brands():
    return ProductsController.get_all_product_brands()

# Endpoint para obtener todos los modelos de productos
@router.get(
    "/models",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def get_all_models():
    return ProductsController.get_all_product_models()

# Endpoint para obtener las ordenes de entrada de productos
@router.get(
    "/input-orders",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def get_all_input_orders():
    return ProductsController.get_all_input_orders()

# Endpoint para obtener las estados de los productos
@router.get(
    "/status",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def get_all_product_status():
    return ProductsController.get_all_product_status()

# Endpoint para crear o agregar productos
@router.post(
    "/create",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
async def create_product(product_data: CreateProduct, redis=Depends(get_redis)):
    result = ProductsController.create_product(product_data)
    await invalidate_cache(redis, "products:*")
    return result

# Endpoint para crear o agregar modelos de productos
@router.post(
    "/create-model",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def create_product_model(product_model: CreateProductModel):
    return ProductsController.create_product_model(product_model)

# Endpoint para crear una marca de producto
@router.post(
    "/create-brand",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def create_product_brand(product_brand: CreateProductBrand):
    return ProductsController.create_product_brand(product_brand)

# Endpoint para crear una orden de entrada de productos
@router.post(
    "/create-input-order",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def create_product_entry(input_order: CreateInputOrder):
    return ProductsController.create_input_order(input_order)

# Endpoint para actualizar la informacion de un producto
@router.put(
    "/update",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def update_product(product_data: UpdateProduct = Body(...)):
    return ProductsController.update_product(product_data)

# Endpoint para actualizar el estado de un producto
@router.put(
    "/update-status",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=50, seconds=60))
    ]
)
def update_product_status(product_data: UpdateProductStatus):
    return ProductsController.update_product_status(product_data)

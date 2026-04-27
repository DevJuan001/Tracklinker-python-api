from app.core.redis import get_redis
from app.core.cache import invalidate_cache
import json
from fastapi import APIRouter, Depends, Body
from fastapi.encoders import jsonable_encoder
from fastapi_limiter.depends import RateLimiter
from app.middlewares.roles_middleware import require_roles
from app.controllers.products_controller import ProductsController
from app.models.input_order_model import InputOrder
from app.models.product_brand_model import ProductBrand
from app.models.product_model import Product, UpdateProduct
from app.models.product_details_model import ProductDetails

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
    start_date: str = None,
    end_date: str = None,
    input_order: int = None,
    category_order: int = None,
    subcategory_order: int = None,
    warranty_time: int = None,
    product_status: int = None,
    brand: int = None,
    product_model: int = None,
    redis=Depends(get_redis)
):
    result = ProductsController.get_all_products(
        start_date,
        end_date,
        input_order,
        category_order,
        subcategory_order,
        warranty_time,
        product_status,
        brand,
        product_model,
    )
    return result

# Endpoint para obtener todas las marcas de productos
@router.get("/brands")
def get_all_brands():
    return ProductsController.get_all_product_brands()

# Endpoint para obtener todos los modelos de productos
@router.get("/models")
def get_all_models():
    return ProductsController.get_all_product_models()

# Endpoint para obtener las ordenes de entrada de productos
@router.get("/input-orders")
def get_all_input_orders():
    return ProductsController.get_all_input_orders()

# Endpoint para obtener las estados de los productos
@router.get("/status")
def get_all_product_status():
    return ProductsController.get_all_product_status()

# Endpoint para crear o agregar productos
@router.post(
    "/create",
    dependencies=[
        Depends(require_roles(["Admin", "Almacen"])),
        Depends(RateLimiter(times=5, seconds=60))
    ]
)
async def create_product(product_data: Product, redis=Depends(get_redis)):
    result = ProductsController.create_product(product_data)
    await invalidate_cache(redis, "products:*")
    return result

# Endpoint para crear o agregar modelos de productos
@router.post("/create-model")
def create_product_model(product_model: ProductDetails):
    return ProductsController.create_product_model(product_model)

# Endpoint para crear una marca de producto
@router.post("/create-brand")
def create_product_brand(product_brand: ProductBrand):
    return ProductsController.create_product_brand(product_brand)

# Endpoint para crear una orden de entrada de productos
@router.post("/create-input-order")
def create_product_entry(input_order: InputOrder):
    return ProductsController.create_input_order(input_order)

# Endpoint para actualizar la informacion de un producto
@router.put("/update")
def update_product(product_data: UpdateProduct = Body(...)):
    return ProductsController.update_product(product_data)

# Endpoint para actualizar el estado de un producto
@router.put("/update-status")
def update_product_status(product_data: dict = Body(...)):
    return ProductsController.update_product_status(product_data)



from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.features.dashboard.controllers.dashboard_controller import DashboardController
from app.middlewares.roles_middleware import require_roles


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


# Endpoint para obtener todos los productos y el numero de productos nuevos
@router.get(
    "/all-and-new",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_old_and_new_products_ammount():
    return DashboardController.get_all_and_new_products_ammount()


# Endopoint para obtener las entradas mensuales de cada proveedor
@router.get(
    "/monthly-inputs",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_monthly_suppliers_inputs():
    return DashboardController.get_all_monthly_supplier_inputs()


# Endpoint para obtener las salidas mensuales con su mes y año
@router.get(
    "/monthly-outputs",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_monthly_outputs():
    return DashboardController.get_all_outputs_by_month()


# Endpoint para obtener todos los estados de garantías y sus cantidades
@router.get(
    "/warranty-status",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_all_warranties_group_by_status():
    return DashboardController.get_all_warranties_group_by_status()


# Endpoint para obtener el numero de usuarios existentes y los nuevos
@router.get(
    "/new-users",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_new_users():
    return DashboardController.get_all_and_new_users()


# Endpoint para obtener el numero de productos que hay por cada marca
@router.get(
    "/stock_by_brand",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_stock_by_brand():
    return DashboardController.get_stock_by_brand()


# Endpoint para obtener el numero de ordenes de salida que existen y las nuevas
@router.get(
    "/output-orders",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_output_orders():
    return DashboardController.get_output_orders_amount()


# Endponit para obtener el numero de categorias que existen
@router.get(
    "/categories",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_categories():
    return DashboardController.get_categories_amount()


# Endpoint para obtener las subcategorias con el número de productos que tienen
@router.get(
    "/subcategories-with-stock",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_subcategories_with_stock():
    return DashboardController.get_subcategories_with_stock()

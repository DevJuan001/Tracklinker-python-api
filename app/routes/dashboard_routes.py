from fastapi import APIRouter, Depends
from app.controllers.dashboard_controller import DashboardController
from app.middlewares.roles_middleware import require_roles

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

# Endpoint para obtener todos los productos y el numero de productos nuevos
@router.get("/all-and-new")
def get_old_and_new_products_ammount():
    return DashboardController.get_all_and_new_products_ammount()

# Endopoint para obtener las entradas mensuales de cada proveedor
@router.get("/monthly-inputs")
def get_monthly_suppliers_inputs():
    return DashboardController.get_all_monthly_supplier_inputs()

# Endpoint para obtener las salidas mensuales con su mes y año
@router.get("/monthly-outputs")
def get_monthly_outputs():
    return DashboardController.get_all_outputs()

# Endpoint para obtener todos los estados de garantías y sus cantidades
@router.get("/warranty-status")
def get_all_warranty_status():
    return DashboardController.get_all_warranty_status()

# Endpoint para obtener el numero de usuarios existentes y los nuevos
@router.get("/new-users")
def get_new_users():
    return DashboardController.get_all_and_new_users()

# Endpoint para obtener el numero de productos que hay por cada marca
@router.get("/stock_by_brand")
def get_stock_by_brand():
    return DashboardController.get_stock_by_brand()

# Endpoint para obtener el numero de ordenes de salida que existen y las nuevas
@router.get("/output-orders")
def get_output_orders():
    return DashboardController.get_output_orders_amount()

# Endponit para obtener el numero de categorias que existen
@router.get("/categories")
def get_categories():
    return DashboardController.get_categories_amount()

# Endpoint para obtener las subcategorias con el número de productos que tienen
@router.get("/subcategories-with-stock")
def get_subcategories_with_stock():
    return DashboardController.get_subcategories_with_stock()
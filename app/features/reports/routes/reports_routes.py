from fastapi import APIRouter, Depends
from app.middlewares.roles_middleware import require_roles
from app.features.reports.controllers.reports_controller import ReportsController

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)
#   ------------ REPORTES DE USUARIOS ------------

# Endpoint para obtener reportes de usuarios por rol
@router.get("/get_users_by_rol/{period}")
def get_users_by_rol(period: str = "30d", payload: dict = Depends(require_roles(["Admin"]))):
    return ReportsController.get_users_by_rol(period)

# Endpoint para obtener reporte de los ultimos 6 usuarios creados
@router.get("/get_recent_users")
def get_recent_users():
    return ReportsController.get_recent_users()

# Endpoint para obtener el crecimiento mensual de usuarios
@router.get("/get_user_growth/{period}")
def get_user_growth(period: str = "30d"):
    return ReportsController.get_user_growth(period)

# Endpoint para obtener los usuarios activos, deshabilitados y recien creados
@router.get("/get_users_by_status")
def get_users_by_status():
    return ReportsController.get_users_by_status()


#   ------------ REPORTES DE PRODUCTOS ------------

# Endpoint para obtener reporte de los ultimos 6 productos agregados
@router.get("/get_recent_products")
def get_recent_products():
    return ReportsController.get_recent_products()

# Endpoint para obtener el crecimiento de productos
@router.get("/get_products_growth/{period}")
def get_products_growth(period: str = "30d"):
    return ReportsController.get_products_growth(period)

# Endpoint para obtener productos por marca
@router.get("/get_products_by_brand/{period}")
def get_products_by_brand(period: str = "30d"):
    return ReportsController.get_products_by_brand(period)

# Endpoint para obtener productos por estado
@router.get("/get_products_by_status")
def get_products_by_status():
    return ReportsController.get_products_by_status()

#   ------------ REPORTES DE CATEGORIAS ------------
# Endpoint para obtener reporte de las ultimas 6 categorias agregados
@router.get("/get_recent_categories")
def get_recent_categories():
    return ReportsController.get_recent_categories()

# Endpoint para obtener el crecimiento de categorias
@router.get("/get_categories_growth/{period}")
def get_categories_growth(period: str = "30d"):
    return ReportsController.get_categories_growth(period)

# Endpoint para obtener cateegorias por estado
@router.get("/get_categories_by_status")
def get_categories_by_status():
    return ReportsController.get_categories_by_status()

#   ------------ REPORTES DE SUBCATEGORIAS ------------
# Endpoint para obtener reporte de las ultimas 6 subcategorias agregados
@router.get("/get_recent_subcategories")
def get_recent_subcategories():
    return ReportsController.get_recent_subcategories()

# Endpoint para obtener el crecimiento de categorias
@router.get("/get_subcategories_growth/{period}")
def get_subcategories_growth(period: str = "30d"):
    return ReportsController.get_subcategories_growth(period)

# Endpoint para obtener subcategorias por categoria
@router.get("/get_subcategories_by_category/{period}")
def get_subcategories_by_category(period: str = "30d"):
    return ReportsController.get_subcategories_by_category(period)

# Endpoint para obtener subcategorias por estado
@router.get("/get_subcategories_by_status")
def get_subcategories_by_status():
    return ReportsController.get_subcategories_by_status()

#   ------------ REPORTES DE GARANTIAS ------------
# Endpoint para obtener reporte de las ultimas 6 garantias agregados
@router.get("/get_recent_warranties")
def get_recent_warranties():
    return ReportsController.get_recent_warranties()

# Endpoint para obtener el crecimiento de garantias
@router.get("/get_warranties_growth/{period}")
def get_warranties_growth(period: str = "30d"):
    return ReportsController.get_warranties_growth(period)

# Endpoint para obtener garantias por marca
@router.get("/get_warranties_by_brand/{period}")
def get_warranties_by_brand(period: str = "30d"):
    return ReportsController.get_warranties_by_brand(period)

# Endpoint para obtener garantias por estado
@router.get("/get_warranties_by_status")
def get_warranties_by_status():
    return ReportsController.get_warranties_by_status()

#   ------------ REPORTES DE PROVEEDORES ------------
# Endpoint para obtener reporte de las ultimos 6 proveedores agregados
@router.get("/get_recent_suppliers")
def get_recent_suppliers():
    return ReportsController.get_recent_suppliers()

# Endpoint para obtener el crecimiento de proveedores
@router.get("/get_suppliers_growth/{period}")
def get_suppliers_growth(period: str = "30d"):
    return ReportsController.get_suppliers_growth(period)

# Endpoint para obtener proveedores por marca
@router.get("/get_suppliers_by_brand/{period}")
def get_suppliers_by_brand(period: str = "30d"):
    return ReportsController.get_suppliers_by_brand(period)

# Endpoint para obtener proveedores por estado
@router.get("/get_suppliers_by_status")
def get_suppliers_by_status():
    return ReportsController.get_suppliers_by_status()

#   ------------ REPORTES DE ORDENES DE SALIDA ------------
# Endpoint para obtener reporte de las ultimas 6 ordenes agregados
@router.get("/get_recent_outputs")
def get_recent_outputs():
    return ReportsController.get_recent_outputs()

# Endpoint para obtener el crecimiento de ordenes
@router.get("/get_outputs_growth/{period}")
def get_outputs_growth(period: str = "30d"):
    return ReportsController.get_outputs_growth(period)

# Endpoint para obtener ordenes por *
@router.get("/get_outputs_by_brand/{period}")
def get_outputs_by_brand(period: str = "30d"):
    return ReportsController.get_outputs_by_brand(period)

# Endpoint para obtener salidas por estado
@router.get("/get_outputs_by_status")
def get_outputs_by_status():
    return ReportsController.get_outputs_by_status()
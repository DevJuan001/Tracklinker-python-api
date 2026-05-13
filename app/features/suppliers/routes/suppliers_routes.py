from fastapi import APIRouter, Depends
from app.models.suppliers_model import Supplier, UpdateSupplier
from app.controllers.suppliers_controller import SuppliersController
from app.middlewares.roles_middleware import require_roles
from fastapi_limiter.depends import RateLimiter

router = APIRouter(
    prefix="/api/suppliers",
    tags=["Suppliers"]
)

# Endpoint para obtener todos los proveedores
@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_all_suppliers(
    name_order: str = None,
    start_date: str = None,
    end_date: str = None,
    status: int = None,
    city: int = None,
):
    return SuppliersController.get_all_suppliers(
        name_order,
        start_date,
        end_date,
        status,
        city,
    )

# Endpoint para obtener un proveedor mediante el id
@router.get(
    "/{supplier_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_supplier_by_id(supplier_id: int):
    return SuppliersController.get_supplier_by_id(supplier_id)

# Endpoint para crear un proveedor
@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def create_supplier(supplier_data: Supplier):
    return SuppliersController.create_supplier(supplier_data)

# Endpoint para actualizar un proveedor mediante el id
@router.put(
    "/update/{supplier_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def update_supplier(supplier_id: int, supplier_data: UpdateSupplier):
    return SuppliersController.update_supplier(supplier_id, supplier_data)

# Endpoint para deshabilitar un proveedor mediante el id
@router.put(
    "/disable/{supplier_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def disable_supplier(supplier_id: int):
    return SuppliersController.disable_supplier(supplier_id)

# Endpoint para habilitar un proveedor mediante el id
@router.put(
    "/enable/{supplier_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def enable_supplier(supplier_id: int):
    return SuppliersController.enable_supplier(supplier_id)
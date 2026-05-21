

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.features.suppliers.controllers.suppliers_controller import SuppliersController
from app.features.suppliers.models.suppliers_schema import CreateSupplierSchema, FilterSuppliersSchema, UpdateSupplierSchema


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
def get_all_suppliers(filters: FilterSuppliersSchema = Depends()):
    return SuppliersController.get_all_suppliers(filters)


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
def create_supplier(supplier_data: CreateSupplierSchema):
    return SuppliersController.create_supplier(supplier_data)


# Endpoint para actualizar un proveedor mediante el id
@router.put(
    "/update/{supplier_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def update_supplier(supplier_id: int, supplier_data: UpdateSupplierSchema):
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

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from app.middlewares.jwt_middleware import verify_jwt
from app.middlewares.roles_middleware import require_roles
from app.features.warranties.controllers.warranties_controller import WarrantiesController
from app.features.warranties.models.warranties_model import WarrantyUpdate, WarrantiesFilter, CreateWarranty

router =APIRouter(
    prefix="/api/warranty_incidents",
    tags= ["Warranty incidents"]
)

# Endpoint para obtener todos las garantías 
@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_all_warranties(filters: WarrantiesFilter = Depends()):
    return WarrantiesController.get_all_warranties(filters)

# Endpoint para obtener una garantía mediante su id
@router.get(
    "/{warranty_incidents_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_warranty_by_id(warranty_incidents_id: int):
       return WarrantiesController.get_warranty_by_id(warranty_incidents_id)

# Endpoint para crear o registrar una garantía
@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def create_warranty(
    warranty_data: CreateWarranty,
    payload: dict = Depends(verify_jwt)
):
    return WarrantiesController.create_warranty(warranty_data, payload)

# Endpoint para actualizar la informacion de la garantía mediante su id
@router.put(
    "/update/{warranty_incidents_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def update_warranty(
    warranty_incidents_id: int,
    warranty_data: WarrantyUpdate,
    payload: dict = Depends(verify_jwt)
):
    return WarrantiesController.update_warranty(warranty_incidents_id, payload, warranty_data)
from fastapi import APIRouter
from app.controllers.warranties_controller import WarrantiesController
from fastapi import Depends
from app.models.warranties_model import Warranty, WarrantyUpdate
from app.middlewares.roles_middleware import require_roles
from fastapi_limiter.depends import RateLimiter

router =APIRouter(
    prefix="/api/warranty_incidents",
    tags= ["Warranty incidents"]
)

# Endpoint para obtener todos las solicitudes de garantía 
@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_all_warranties(
    start_date: str = None,
    end_date: str = None,
    status: int = None,
):
    return WarrantiesController.get_all_warranties(
        start_date,
        end_date,
        status,
    )

# Endpoint para ontener solicitud por mediante id
@router.get(
    "/{warranty_incidents_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_warranty_by_id(warranty_incidents_id: int):
       return WarrantiesController.get_warranty_by_id(warranty_incidents_id)

# Endpont para crear o registrar incidencia de garantía
@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def create_warranty(warranty_data: Warranty):
    return WarrantiesController.create_warranty(warranty_data)

# Endpoint para actualizar la informacion de la incidencia mediante su id
@router.put(
    "/update/{warranty_incidents_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def update_warranty(
    warranty_incidents_id:int,
    warranty_data:  WarrantyUpdate,
):
    return WarrantiesController.update_warranty(warranty_incidents_id, warranty_data)

@router.delete(
    "/delete/{warranty_incidents_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def delete_warranty(warranty_incidents_id:int):
  return WarrantiesController.delete_warranty(warranty_incidents_id)
from fastapi import APIRouter
from app.controllers.warranties_controller import WarrantiesController
from fastapi import Depends
from app.models.warranties_model import Warranty, WarrantyUpdate
from app.middlewares.roles_middleware import require_roles



router =APIRouter(
    prefix="/api/warranty_incidents",
    tags= ["Warranty incidents"]
)

# Endpoint para obtener todos las solicitudes de garantía 
@router.get("/")
def get_all_warranties(
    start_date: str = None,
    end_date: str = None,
    status: int = None,
    payload: dict= Depends(require_roles(["Admin"]))
):
    return WarrantiesController.get_all_warranties(
        start_date,
        end_date,
        status,
    )

# Endpoint para ontener solicitud por mediante id
@router.get("/{warranty_incidents_id}")
def get_warranty_by_id(
    warranty_incidents_id: int,
    payload: dict= Depends(require_roles(["Admin"]))
    ):
       return WarrantiesController.get_warranty_by_id(warranty_incidents_id)

# Endpont para crear o registrar incidencia de garantía
@router.post("/create")
def create_warranty(
    warranty_data: Warranty,
    payload: dict = Depends (require_roles("Admin"))
    ):
    return WarrantiesController.create_warranty(warranty_data)

# Endpoint para actualizar la informacion de la incidencia mediante su id
@router.put("/update/{warranty_incidents_id}")
def update_warranty(
    warranty_incidents_id:int,
    warranty_data:  WarrantyUpdate,
    payload: dict= Depends(require_roles(["Admin"]))

):
    return WarrantiesController.update_warranty(warranty_incidents_id, warranty_data)

@router.delete("/delete/{warranty_incidents_id}")
def delete_warranty(
    warranty_incidents_id:int,
    payload: dict = Depends (require_roles(["Admin"]))
):
  return WarrantiesController.delete_warranty(warranty_incidents_id)
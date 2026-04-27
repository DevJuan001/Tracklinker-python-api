from fastapi import APIRouter
from app.controllers.output_details_controller import OutputDetailsController
from fastapi import Depends
from app.models.output_details_model import OutputDetails
from app.middlewares.roles_middleware import require_roles

router = APIRouter(
    prefix="/api/output_details",
    tags=["Output details"]
)

# Endpoint para obtener todos los detalles de salida
@router.get("/")
def get_all_outputDetails():
    return OutputDetailsController.get_all_outputDetails()

# Endpoint para obtener los detalles de salida por id
@router.get("/{output_details_id}")
def get_outputDetails_by_id(
    output_details_id: int
):
    return OutputDetailsController.get_outputDetails_by_id(output_details_id)

# Endpoint para crear un detalle de salida
@router.post("/create")
def create_outputDetails(
    outputDetails_data: OutputDetails
):
    return OutputDetailsController.create_outputDetails(outputDetails_data)

# Endpoint para actualizar detalles de salida
@router.put("/update/{output_details_id}")
def update_outputDetails(
    output_details_id: int,
    outputDetails_data: dict
):
    return OutputDetailsController.update_outputDetails(output_details_id, outputDetails_data)

# Endpoint para deshabilitar la orden de salida
@router.put("/disable/{out_order_id}")
def disable_output_order(
    out_order_id: int    
):
    return OutputDetailsController.disable_output(out_order_id)

# Endpoint para habilitar la orden de salida
@router.put("/enable/{out_order_id}")
def enable_output_order(out_order_id: int ):
    return OutputDetailsController.enable_output(out_order_id)
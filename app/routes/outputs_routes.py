from fastapi import APIRouter, Depends
from app.controllers.output_orders_controller import OutputOrdersController
from app.models.output_orders_model import OutputOrder
from app.middlewares.roles_middleware import require_roles

router =APIRouter(
    prefix="/api/outputs",
    tags =["Transformations"]
)

# Endpoint para obtener todas las órdenes de salida
@router.get("/")       
def get_all_output_orders(
    #payload: dict=Depends(require_roles(["Admin"]))
    ):
    return OutputOrdersController.get_all_output_orders()

# Endpoint para obtener una orden de salida por ID
@router.get("/{out_order_id}")
def get_output_order_by_id(
    out_order_id: int,
    #payload: dict= Depends(require_roles(["Admin"]))
    ):
       return OutputOrdersController.get_output_order_by_id(out_order_id)

# Endpoint para crear o registrar una orden de salida
@router.post("/create")             
def create_output_order(
    output_order_data:OutputOrder,
    payload: dict = Depends (require_roles(["Admin"]))
    
    ):
    return OutputOrdersController.create_output_order(output_order_data)
# Endpoint para actualizar la informacion de la orden de salida mediante su id
@router.put("/update/{output_order_id}")
def update_output_order(
    output_order_id:int,
    output_order_data:dict,
    payload: dict= Depends(require_roles(["Admin"]))

):
    return OutputOrdersController.update_output_order(output_order_id, output_order_data)
@router.delete("/delete/{output_order_id}")
def delete_output_order(
    output_order_id:int,
    payload: dict = Depends (require_roles(["Admin"]))
):
  return OutputOrdersController.delete_output_order(output_order_id)

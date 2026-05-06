from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from app.middlewares.roles_middleware import require_roles
from app.features.output_orders.controllers.output_orders_controller import OutputOrdersController
from app.features.output_orders.models.output_orders_model import CreateOutputOrder, OutputOrdersFilters

router =APIRouter(
    prefix="/api/output_orders",
    tags =["Output_orders"]
)

# Endpoint para obtener todas las órdenes de salida
@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)       
def get_all_output_orders(filters: OutputOrdersFilters = Depends()):
    return OutputOrdersController.get_all_output_orders(filters)

# Endpoint para obtener una orden de salida por ID
@router.get(
    "/{out_order_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def get_output_order_by_id(
    out_order_id: int,
):
    return OutputOrdersController.get_output_order_by_id(out_order_id)

# Endpoint para crear o registrar una orden de salida
@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)             
def create_output_order(
    output_order_data: CreateOutputOrder,
):
    return OutputOrdersController.create_output_order(output_order_data)

# Endpoint para actualizar la informacion de la orden de salida mediante su id
@router.put(
    "/update/{output_order_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def update_output_order(
    output_order_id: int,
    output_order_data: dict,
):
    return OutputOrdersController.update_output_order(output_order_id, output_order_data)

@router.delete(
    "/delete/{output_order_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def delete_output_order(
    output_order_id: int,
):
  return OutputOrdersController.delete_output_order(output_order_id)

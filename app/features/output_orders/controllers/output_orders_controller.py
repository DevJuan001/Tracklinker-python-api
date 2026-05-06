from fastapi import HTTPException
from app.features.output_orders.services.output_orders_service import OutputOrdersService
from app.features.output_orders.models.output_orders_model import CreateOutputOrder, OutputOrdersFilters, UpdateOutputOrder


class OutputOrdersController:

    @staticmethod
    def get_all_output_orders(filters: OutputOrdersFilters):
        error, output_orders = OutputOrdersService.get_all_output_orders(
            filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": output_orders
        }

    @staticmethod
    def get_output_order_by_id(out_order_id: int):
        error, output_order = OutputOrdersService.get_output_order_by_id(
            out_order_id
        )
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": output_order
        }

    @staticmethod
    def create_output_order(output_order_data: CreateOutputOrder):
        error, success, message = OutputOrdersService.create_output_order(
            output_order_data
        )
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_output_order(output_order_id: int, output_order_data: UpdateOutputOrder):
        error, success, message = OutputOrdersService.update_output_order(
            output_order_id, output_order_data
        )
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def disable_output_order(output_order_id: int):
        error, success, message = OutputOrdersService.disable_output_order(
            output_order_id
        )
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def enable_output_order(output_order_id: int):
        error, success, message = OutputOrdersService.enable_output_order(
            output_order_id
        )
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

from fastapi import HTTPException
from app.repository.output_orders_repository import OutputOrdersRepository 
from app.models.output_orders_model import OutputOrder
from app.core.config import settings


class OutputOrdersController:
       
    @staticmethod
    def get_all_output_orders():
        error, output_orders = OutputOrdersRepository.find_all_output_orders()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": output_orders
        }
    
    @staticmethod
    def get_output_order_by_id(out_order_id: int):
        error, output_order = OutputOrdersRepository.find_by_id(out_order_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": output_order
        }
   
    @staticmethod
    def create_output_order(output_order_data: OutputOrder):
        error, success, message = OutputOrdersRepository.create(output_order_data)
        if error:
            raise HTTPException (status_code=400, detail=error)
        return{
            "seccess":success,
            "message": message
        }

    @staticmethod
    def update_output_order(output_order_id:int, output_order_data: dict):
        error, message, output_order= OutputOrdersRepository.update(output_order_id, output_order_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return{
            "message": message,
            "data": output_order

        } 
    
    @staticmethod
    def delete_output_order(output_order_id:int):
        error, success, message= OutputOrdersRepository.delete(output_order_id)
        if error:
            raise HTTPException(status_code=400, detail= error)
        return{
            "success": success,
            "message": message
        }
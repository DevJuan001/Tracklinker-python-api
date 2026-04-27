from app.repository.suppliers_repository import SuppliersRepository
from app.models.suppliers_model import Supplier
from fastapi import HTTPException


class SuppliersController:

    @staticmethod
    def get_all_suppliers():
        error, data = SuppliersRepository.find_all_suppliers()

        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_supplier_by_id(supplier_id: int):
        error, data = SuppliersRepository.find_supplier_by_id(supplier_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def create_supplier(supplier_data: Supplier):
        error, success, message = SuppliersRepository.create_supplier(
            supplier_data)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_supplier(supplier_id: int, supplier_data: dict):
        error, success, message = SuppliersRepository.update_supplier(
            supplier_id, supplier_data)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "success": success,
            "message": message,
        }

    @staticmethod
    def disable_supplier(supplier_id: int):
        error, success, message = SuppliersRepository.disable_supplier(
            supplier_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "success": success,
            "message": message
        }
    
    @staticmethod
    def enable_supplier(supplier_id: int):
        error, success, message = SuppliersRepository.enable_supplier(
            supplier_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "success": success,
            "message": message
        }

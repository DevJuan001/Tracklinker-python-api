from fastapi import HTTPException
from app.features.suppliers.services.suppliers_service import SuppliersService
from app.features.suppliers.models.suppliers_schema import CreateSupplierSchema, FilterSuppliersSchema, UpdateSupplierSchema


class SuppliersController:

    @staticmethod
    def get_all_suppliers(filters: FilterSuppliersSchema):
        error, data = SuppliersService.get_all_suppliers(filters)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_supplier_by_id(supplier_id: int):
        error, data = SuppliersService.get_supplier_by_id(supplier_id)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def create_supplier(supplier_data: CreateSupplierSchema):
        error, success, message = SuppliersService.create_supplier(
            supplier_data
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_supplier(supplier_id: int, supplier_data: UpdateSupplierSchema):
        error, success, message = SuppliersService.update_supplier(
            supplier_id, supplier_data
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "success": success,
            "message": message,
        }

    @staticmethod
    def disable_supplier(supplier_id: int):
        error, success, message = SuppliersService.disable_supplier(
            supplier_id
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def enable_supplier(supplier_id: int):
        error, success, message = SuppliersService.enable_supplier(
            supplier_id
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "success": success,
            "message": message
        }

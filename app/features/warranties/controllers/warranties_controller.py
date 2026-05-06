from fastapi import HTTPException
from app.features.warranties.services.warranties_service import WarrantiesService
from app.features.warranties.models.warranties_model import WarrantyUpdate, WarrantiesFilter, CreateWarranty


class WarrantiesController:

    @staticmethod
    def get_all_warranties(filters: WarrantiesFilter):
        error, warranties = WarrantiesService.get_all_warranties(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": warranties
        }

    @staticmethod
    def get_warranty_by_id(warranty_incidents_id: int):
        error, warranty = WarrantiesService.get_warranty_by_id(
            warranty_incidents_id
        )
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": warranty
        }

    @staticmethod
    def create_warranty(warranty_data: CreateWarranty, payload: dict):
        error, success, message = WarrantiesService.create_warranty(
            warranty_data, payload["user_id"]
        )
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_warranty(warranty_incidents_id: int, payload: int, warranty_data: WarrantyUpdate):
        error, success, message = WarrantiesService.update_warranty(
            warranty_incidents_id, payload["user_id"], warranty_data
        )
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

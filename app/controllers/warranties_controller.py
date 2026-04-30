from fastapi import HTTPException
from app.repository.warranties_repository import WarrantiesRepository
from app.models.warranties_model import Warranty, WarrantyUpdate


class WarrantiesController:

    @staticmethod
    def get_all_warranties(
        start_date: str = None,
        end_date: str = None,
        status: int = None,
    ):
        error, warranties = WarrantiesRepository.find_all_warranties(
            start_date,
            end_date,
            status,
        )
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": warranties
        }

    @staticmethod
    def get_warranty_by_id(warranty_incidents_id: int):
        error, warranties = WarrantiesRepository.find_warranty_by_id(
            warranty_incidents_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": warranties
        }

    @staticmethod
    def create_warranty(warranty_data: Warranty):
        error, success, message = WarrantiesRepository.create_warranty(
            warranty_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_warranty(warranty_incidents_id: int, warranty_data: WarrantyUpdate):
        error, success, message = WarrantiesRepository.update_warranty(
            warranty_incidents_id, warranty_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def delete_warranty(warranty_incidents_id: int):
        error, success, message = WarrantiesRepository.delete_warranty(
            warranty_incidents_id)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

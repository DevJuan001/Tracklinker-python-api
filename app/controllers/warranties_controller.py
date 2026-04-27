from fastapi import HTTPException
from app.repository.warranties_repository import WarrantiesRepository
from app.models.warranties_model import Warranty, WarrantyUpdate


class WarrantiesController:

    @staticmethod
    def get_all_guarantee(
        start_date: str = None,
        end_date: str = None,
        status: int = None,
    ):
        error, guarantiee = WarrantiesRepository.find_all_guarantiee(
            start_date,
            end_date,
            status,
        )
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": guarantiee
        }

    @staticmethod
    def get_guarantiee_by_id(warranty_incidents_id: int):
        error, guarantiee = WarrantiesRepository.find_by_id(
            warranty_incidents_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": guarantiee
        }

    @staticmethod
    def create_guarantiee(warranty_data: Warranty):
        error, success, message = WarrantiesRepository.create(warranty_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_garantee(warranty_incidents_id: int, warranty_data: WarrantyUpdate):
        error, success, message = WarrantiesRepository.update(
            warranty_incidents_id, warranty_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def delete_garantee(warranty_incidents_id: int):
        error, success, message = WarrantiesRepository.delete(
            warranty_incidents_id)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def get_deleted_guarantees_by_date_range(start_date: str, end_date: str):
        error, guarantees = WarrantiesRepository.find_deleted_guarantees_by_date_range(
            start_date, end_date)

        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": guarantees
        }

    @staticmethod
    def get_all_guarantees():
        error, guarantees = WarrantiesRepository.find_all_guarantees()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": guarantees
        }

    @staticmethod
    def get_disabled_guarantees():
        error, guarantees = WarrantiesRepository.find_disabled_guarantees()

        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": guarantees
        }

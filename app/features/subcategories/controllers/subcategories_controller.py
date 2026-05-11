from fastapi import HTTPException
from app.features.subcategories.models.subcategories_schemas import SubcategoriesFiltersSchema
from app.features.subcategories.repositories.subcategories_repository import SubcategoriesRepository


class SubcategoriesController:

    @staticmethod
    def get_all_subcategories(filters: SubcategoriesFiltersSchema):
        error, subcategories = SubcategoriesRepository.find_all_subcategories(
            filters
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": subcategories
        }

    @staticmethod
    def get_subcategory_by_id(subcategory_id: int):
        error, subcategory = SubcategoriesRepository.find_by_id(subcategory_id)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": subcategory
        }

    @staticmethod
    def get_categories():
        error, categories = SubcategoriesRepository.find_categories()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": categories
        }

    @staticmethod
    def create_subcategory(subcategory_data: dict):
        error, message = SubcategoriesRepository.create_subcategory(
            subcategory_data
            )
        
        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": True,
            "message": message
        }

    @staticmethod
    def update_subcategory(subcategory_id: int, subcategory_data: dict):
        error, message, subcategory = SubcategoriesRepository.update_subcategory(
            subcategory_id, subcategory_data
            )
        
        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": True,
            "message": message,
        }

    @staticmethod
    def disable_subcategory(subcategory_id: int):
        error, message = SubcategoriesRepository.disable_subcategory(
            subcategory_id
            )
        
        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": True,
            "message": message
        }

    @staticmethod
    def enable_subcategory(subcategory_id: int):
        error, message = SubcategoriesRepository.enable_subcategory(
            subcategory_id
            )
        
        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": True,
            "message": message
        }

    @staticmethod
    def get_subcategories_by_date_range(start_date: str, end_date: str):
        error, subcategories = SubcategoriesRepository.find_subcategories_by_date_range(
            start_date, end_date
            )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": subcategories
        }

    @staticmethod
    def get_deleted_subcategories_by_date_range(start_date: str, end_date: str):
        error, subcategories = SubcategoriesRepository.find_deleted_subcategories_by_date_range(
            start_date, end_date
            )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": subcategories
        }

    @staticmethod
    def get_disabled_subcategories():
        error, subcategories = SubcategoriesRepository.find_disabled_subcategories()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": subcategories
        }

from app.repository.subcategories_repository import SubcategoriesRepository
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token


class SubcategoriesController:

    @staticmethod
    def get_all_subcategories(
        start_date: str = None,
        end_date: str = None,
        category_order: int = None,
        status: int = None,
        name_order: str = None,
    ):
        error, subcategories = SubcategoriesRepository.find_all_subcategories(
            start_date,
            end_date,
            category_order,
            status,
            name_order,
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
            subcategory_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": True,
            "message": message
        }

    @staticmethod
    def update_subcategory(subcategory_id: int, subcategory_data: dict):
        error, message, subcategory = SubcategoriesRepository.update_subcategory(
            subcategory_id, subcategory_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": True,
            "message": message,
            "data": subcategory
        }

    @staticmethod
    def disable_subcategory(subcategory_id: int):
        error, message = SubcategoriesRepository.disable_subcategory(
            subcategory_id)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": True,
            "message": message
        }
    
    @staticmethod
    def enable_subcategory(subcategory_id: int):
        error, message = SubcategoriesRepository.enable_subcategory(
            subcategory_id)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": True,
            "message": message
        }

    @staticmethod
    def get_subcategories_by_date_range(start_date: str, end_date: str):
        error, subcategories = SubcategoriesRepository.find_subcategories_by_date_range(
            start_date, end_date)

        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": subcategories
        }

    @staticmethod
    def get_deleted_subcategories_by_date_range(start_date: str, end_date: str):
        error, subcategories = SubcategoriesRepository.find_deleted_subcategories_by_date_range(
            start_date, end_date)

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

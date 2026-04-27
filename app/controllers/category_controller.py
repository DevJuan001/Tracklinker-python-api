from app.repository.category_repository import CategoryRepository
from app.models.category_model import CategoryCreate, CategoryUpdate
from fastapi import HTTPException


class CategoryController:

    @staticmethod
    def get_all_categories(
        name_order: str = None,
        start_date: str = None,
        end_date: str = None,
        status: int = None,
    ):
        error, categories = CategoryRepository.find_all_categories(
            name_order,
            start_date,
            end_date,
            status,
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "message": "Categorías obtenidas correctamente",
            "data": categories
        }

    @staticmethod
    def get_category_by_id(category_id: int):
        error, category = CategoryRepository.find_by_id(category_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": category
        }

    @staticmethod
    def create_category(category_data: CategoryCreate):
        data_dict = category_data.dict()

        error, success, message = CategoryRepository.create_category(data_dict)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message,
        }

    @staticmethod
    def update_category(category_id: int, category_data: CategoryUpdate):
        error, success, message = CategoryRepository.update_category(
            category_id, category_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def enable_category(category_id: int):
        error, success, message = CategoryRepository.enable_category(
            category_id)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def disable_category(category_id: int):
        error, success, message = CategoryRepository.disable_category(
            category_id)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

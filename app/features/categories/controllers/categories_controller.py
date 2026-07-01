from fastapi import HTTPException
from app.features.categories.models.categories_schemas import CategoriesFiltersSchema, CreateCategorySchema, UpdateCategorySchema
from app.features.categories.services.categories_service import CategoriesService


class CategoriesController:

    @staticmethod
    def get_all_categories(filters: CategoriesFiltersSchema):
        error, categories = CategoriesService.get_all_categories(filters)

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "data": categories
        }

    @staticmethod
    def get_category_by_id(category_id: int):
        error, category = CategoriesService.get_category_by_id(category_id)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": category
        }

    @staticmethod
    def get_active_categories():
        error, categories = CategoriesService.get_active_categories()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": categories
        }

    @staticmethod
    def create_category(category_data: CreateCategorySchema):
        error, success, message = CategoriesService.create_category(
            category_data)

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message,
        }

    @staticmethod
    def update_category(category_id: int, category_data: UpdateCategorySchema):
        error, success, message = CategoriesService.update_category(
            category_id, category_data
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def enable_category(category_id: int):
        error, success, message = CategoriesService.enable_category(
            category_id
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def disable_category(category_id: int):
        error, success, message = CategoriesService.disable_category(
            category_id
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

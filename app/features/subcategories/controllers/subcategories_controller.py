from fastapi import HTTPException
from app.features.subcategories.models.subcategories_schemas import CreateSubcategorySchema, SubcategoriesFiltersSchema, UpdateSubcategorySchema
from app.features.subcategories.services.subcategories_service import SubcategoriesService


class SubcategoriesController:

    @staticmethod
    def get_all_subcategories(filters: SubcategoriesFiltersSchema):
        error, subcategories = SubcategoriesService.get_all_subcategories(
            filters
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": subcategories
        }

    @staticmethod
    def get_subcategory_by_id(subcategory_id: int):
        error, subcategory = SubcategoriesService.get_subcategory_by_id(
            subcategory_id
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": subcategory
        }

    @staticmethod
    def get_active_categories():
        error, categories = SubcategoriesService.get_active_categories()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": categories
        }

    @staticmethod
    def create_subcategory(subcategory_data: CreateSubcategorySchema):
        error, message = SubcategoriesService.create_subcategory(
            subcategory_data
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": True,
            "message": message
        }

    @staticmethod
    def update_subcategory(subcategory_id: int, subcategory_data: UpdateSubcategorySchema):
        error, success, message = SubcategoriesService.update_subcategory(
            subcategory_id, subcategory_data
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message,
        }

    @staticmethod
    def disable_subcategory(subcategory_id: int):
        error, success, message = SubcategoriesService.disable_subcategory(
            subcategory_id
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def enable_subcategory(subcategory_id: int):
        error, success, message = SubcategoriesService.enable_subcategory(
            subcategory_id
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

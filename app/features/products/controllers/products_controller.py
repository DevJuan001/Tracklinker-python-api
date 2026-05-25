

from fastapi import HTTPException
from app.features.products.services.products_service import ProductsService
from app.features.products.services.input_orders_service import InputOrdersService
from app.features.products.services.product_brands_service import ProductBrandsService
from app.features.products.services.product_models_service import ProductModelsService
from app.features.products.models.schemas.input_orders_schemas import CreateInputOrderSchema
from app.features.products.models.schemas.product_brands_schemas import CreateProductBrandSchema
from app.features.products.models.schemas.product_models_schemas import CreateProductModelSchema
from app.features.products.models.schemas.products_schemas import CreateProductSchema, ProductsFilterSchema, UpdateProductSchema, UpdateProductStatusSchema


class ProductsController:
    @staticmethod
    def get_all_products(filters: ProductsFilterSchema):
        error, products = ProductsService.get_all_products(filters)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": products
        }

    @staticmethod
    def get_all_input_orders():
        error, input_orders = InputOrdersService.get_all_input_orders()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": input_orders
        }

    @staticmethod
    def get_all_product_brands():
        error, brands = ProductBrandsService.get_all_product_brands()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": brands
        }

    @staticmethod
    def get_all_product_models():
        error, models = ProductModelsService.get_all_product_models()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": models
        }

    @staticmethod
    def get_all_product_status():
        error, status = ProductsService.get_all_products_status()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": status
        }

    @staticmethod
    def create_product(product_data: CreateProductSchema):
        error, success, message = ProductsService.create_product(
            product_data
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def create_product_model(product_model: CreateProductModelSchema):
        error, success, message = ProductModelsService.create_product_model(
            product_model
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def create_product_brand(product_brand: CreateProductBrandSchema):
        error, success, message = ProductBrandsService.create_product_brand(
            product_brand
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def create_input_order(input_order: CreateInputOrderSchema):
        error, success, message = InputOrdersService.create_input_order(
            input_order
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_product(product_data: UpdateProductSchema):
        error, success, message = ProductsService.update_product(
            product_data
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_product_status(product_data: UpdateProductStatusSchema):
        error, success, message = ProductsService.update_product_status(
            product_data
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

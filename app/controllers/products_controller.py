from app.repository.products_repository import ProductsRepository
from app.repository.product_details_repository import ProductDetailsRepository
from app.repository.product_brands_repository import ProductBrandsRepository
from app.repository.input_orders_repository import InputOrdersRepository
from app.repository.product_models_repository import ProductModelsRepository
from app.models.product_model import UpdateProduct, Product
from fastapi import HTTPException


class ProductsController:
    @staticmethod
    def get_all_products(
        start_date: str = None,
        end_date: str = None,
        input_order: int = None,
        category_order: int = None,
        subcategory_order: int = None,
        warranty_time: int = None,
        product_status: int = None,
        brand: int = None,
        product_model: int = None,
    ):
        error, products = ProductsRepository.find_all_products(
            start_date,
            end_date,
            input_order,
            category_order,
            subcategory_order,
            warranty_time,
            product_status,
            brand,
            product_model,
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": products
        }

    @staticmethod
    def get_all_input_orders():
        error, input_orders = InputOrdersRepository.find_all_input_orders()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": input_orders
        }

    @staticmethod
    def get_all_product_brands():
        error, brands = ProductBrandsRepository.find_all_product_brands()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": brands
        }

    @staticmethod
    def get_all_product_models():
        error, models = ProductModelsRepository.find_all_product_models()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": models
        }

    @staticmethod
    def get_all_product_status():
        error, status = ProductsRepository.find_all_product_status()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": status
        }

    @staticmethod
    def create_product(product_data: Product):
        error, success, message = ProductsRepository.create_product(
            product_data)

        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "sucess": success,
            "message": message
        }

    @staticmethod
    def create_product_model(product_model):
        error, success, message = ProductDetailsRepository.create_product_details(
            product_model)

        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def create_product_brand(product_brand):
        error, success, message = ProductBrandsRepository.create_product_brand(
            product_brand)

        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def create_input_order(input_order):
        error, success, message = InputOrdersRepository.create_input_order(
            input_order)

        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_product(product_data: UpdateProduct):
        error, success, message = ProductsRepository.update_product(
            product_data)

        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_product_status(product_data: dict):
        error, success, message = ProductsRepository.update_product_status(
            product_data)

        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message
        }

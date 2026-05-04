from fastapi import HTTPException
from app.repository.user_repository import UserRepository
from app.repository.category_repository import CategoryRepository
from app.repository.suppliers_repository import SuppliersRepository
from app.repository.output_orders_repository import OutputOrdersRepository
from app.repository.subcategories_repository import SubcategoriesRepository
from app.features.warranties.warranties_repository import WarrantiesRepository
from app.features.products.repositories.products_repository import ProductsRepository


class ReportsController:

    #   ------------ REPORTES DE USUARIOS ------------
    @staticmethod
    def get_recent_users():
        error, user = UserRepository.find_recent_users()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": user
        }

    @staticmethod
    def get_users_by_rol(period: str):
        error, user = UserRepository.find_users_by_rol(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": user
        }

    @staticmethod
    def get_users_by_month(period: str):
        error, data = UserRepository.find_users_by_month(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_user_growth(period: str):
        error, data = UserRepository.find_users_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_users_by_status():
        error, data = UserRepository.find_users_by_status()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

#   ------------ REPORTES DE PRODUCTOS ------------
    @staticmethod
    def get_recent_products():
        error, products = ProductsRepository.find_recent_products()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": products
        }

    @staticmethod
    def get_products_growth(period: str):
        error, data = ProductsRepository.find_products_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_products_by_brand(period: str):
        error, data = ProductsRepository.find_products_by_brand(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_products_by_status():
        error, data = ProductsRepository.find_products_by_status()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }


#   ------------ REPORTES DE CATEGORIAS ------------

    @staticmethod
    def get_recent_categories():
        error, categories = CategoryRepository.find_recent_categories()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": categories
        }

    @staticmethod
    def get_categories_growth(period: str):
        error, data = CategoryRepository.find_categories_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_categories_by_brand(period: str):
        error, data = CategoryRepository.find_categories_by_brand(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_categories_by_status():
        error, data = CategoryRepository.find_categories_by_status()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

#   ------------ REPORTES DE SUBCATEGORIAS ------------
    @staticmethod
    def get_recent_subcategories():
        error, subcategories = SubcategoriesRepository.find_recent_subcategories()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": subcategories
        }

    @staticmethod
    def get_subcategories_growth(period: str):
        error, data = SubcategoriesRepository.find_subcategories_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_subcategories_by_category(period: str):
        error, data = SubcategoriesRepository.find_subcategories_by_category(
            period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_subcategories_by_status():
        error, data = SubcategoriesRepository.find_subcategories_by_status()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

#   ------------ REPORTES DE GARANTÍAS ------------
    @staticmethod
    def get_recent_warranties():
        error, warranties = WarrantiesRepository.find_recent_warranties()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": warranties
        }

    @staticmethod
    def get_warranties_growth(period: str):
        error, data = WarrantiesRepository.find_warranties_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_warranties_by_brand(period: str):
        error, data = WarrantiesRepository.find_warranties_by_brand(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_warranties_by_status():
        error, data = WarrantiesRepository.find_warranties_by_status()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

#   ------------ REPORTES DE PROVEEDORES ------------
    @staticmethod
    def get_recent_suppliers():
        error, suppliers = SuppliersRepository.find_recent_suppliers()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": suppliers
        }

    @staticmethod
    def get_suppliers_growth(period: str):
        error, data = SuppliersRepository.find_suppliers_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_suppliers_by_brand(period: str):
        error, data = SuppliersRepository.find_suppliers_by_brand(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_suppliers_by_status():
        error, data = SuppliersRepository.find_suppliers_by_status()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }


#   ------------ REPORTES DE ORDENES DE SALIDA ------------

    @staticmethod
    def get_recent_outputs():
        error, outputs = OutputOrdersRepository.find_recent_outputs()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": outputs
        }

    @staticmethod
    def get_outputs_growth(period: str):
        error, data = OutputOrdersRepository.find_outputs_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_outputs_by_brand(period: str):
        error, data = OutputOrdersRepository.find_outputs_by_brand(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

    @staticmethod
    def get_outputs_by_status():
        error, data = OutputOrdersRepository.find_outputs_by_status()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

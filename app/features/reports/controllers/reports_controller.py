

from fastapi import HTTPException
from app.features.reports.services.reports_service import ReportsService


class ReportsController:

    #   ------------ REPORTES DE USUARIOS ------------
    @staticmethod
    def get_recent_users():
        error, users = ReportsService.get_recent_users()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": users
        }

    @staticmethod
    def get_users_by_rol(period: str):
        error, users = ReportsService.get_users_by_rol(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": users
        }

    @staticmethod
    def get_users_growth(period: str):
        error, data = ReportsService.get_users_growth(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_users_by_status():
        error, data = ReportsService.get_users_by_status()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

#   ------------ REPORTES DE PRODUCTOS ------------
    @staticmethod
    def get_recent_products():
        error, products = ReportsService.get_recent_products()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": products
        }

    @staticmethod
    def get_products_growth(period: str):
        error, data = ReportsService.get_products_growth(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_products_by_brand(period: str):
        error, data = ReportsService.get_products_by_brand(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_products_by_status():
        error, data = ReportsService.get_products_by_status()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }


#   ------------ REPORTES DE CATEGORIAS ------------

    @staticmethod
    def get_recent_categories():
        error, categories = ReportsService.get_recent_categories()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": categories
        }

    @staticmethod
    def get_categories_growth(period: str):
        error, data = ReportsService.get_categories_growth(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_categories_by_brand(period: str):
        error, data = ReportsService.get_categories_by_brand(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_categories_by_status():
        error, data = ReportsService.get_categories_by_status()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

#   ------------ REPORTES DE SUBCATEGORIAS ------------
    @staticmethod
    def get_recent_subcategories():
        error, subcategories = ReportsService.get_recent_subcategories()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": subcategories
        }

    @staticmethod
    def get_subcategories_growth(period: str):
        error, data = ReportsService.get_subcategories_growth(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_subcategories_by_category(period: str):
        error, data = ReportsService.get_subcategories_by_category(
            period
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_subcategories_by_status():
        error, data = ReportsService.get_subcategories_by_status()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

#   ------------ REPORTES DE GARANTÍAS ------------
    @staticmethod
    def get_recent_warranties():
        error, warranties = ReportsService.get_recent_warranties()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": warranties
        }

    @staticmethod
    def get_warranties_growth(period: str):
        error, data = ReportsService.get_warranties_growth(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_warranties_by_brand(period: str):
        error, data = ReportsService.get_warranties_by_brand(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_warranties_by_status():
        error, data = ReportsService.get_warranties_by_status()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

#   ------------ REPORTES DE PROVEEDORES ------------
    @staticmethod
    def get_recent_suppliers():
        error, suppliers = ReportsService.get_recent_suppliers()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": suppliers
        }

    @staticmethod
    def get_suppliers_growth(period: str):
        error, data = ReportsService.get_suppliers_growth(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_suppliers_by_brand(period: str):
        error, data = ReportsService.get_suppliers_by_brand(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_suppliers_by_status():
        error, data = ReportsService.get_suppliers_by_status()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }


#   ------------ REPORTES DE ORDENES DE SALIDA ------------

    @staticmethod
    def get_recent_outputs():
        error, outputs = ReportsService.get_recent_outputs()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": outputs
        }

    @staticmethod
    def get_outputs_growth(period: str):
        error, data = ReportsService.get_outputs_growth(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_outputs_by_brand(period: str):
        error, data = ReportsService.get_outputs_by_brand(period)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_outputs_by_status():
        error, data = ReportsService.get_outputs_by_status()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

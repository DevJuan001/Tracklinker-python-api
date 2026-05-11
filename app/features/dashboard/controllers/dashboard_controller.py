

from fastapi import HTTPException
from app.features.dashboard.services.dashboard_service import DashboardService


class DashboardController:

    @staticmethod
    def get_all_and_new_products_ammount():
        error, data = DashboardService.get_all_and_new_products_ammount()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_all_monthly_supplier_inputs():
        error, data = DashboardService.get_all_monthly_supplier_inputs()

        if error:
            raise HTTPException(status_code=404, detail=error)
        
        return {
            "data": data
        }

    @staticmethod
    def get_all_outputs_by_month():
        error, data = DashboardService.get_all_outputs_by_month()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_all_warranties_group_by_status():
        error, data = DashboardService.get_all_warranties_group_by_status()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_all_and_new_users():
        error, data = DashboardService.get_all_and_new_users()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_stock_by_brand():
        error, data = DashboardService.get_stock_by_brand()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_output_orders_amount():
        error, data = DashboardService.get_output_orders_amount()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_categories_amount():
        error, data = DashboardService.get_categories_amount()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_subcategories_with_stock():
        error, data = DashboardService.get_subcategories_with_stock()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

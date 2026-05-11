

from app.features.dashboard.models.dashboard_responses import (
    OutputByMonthResponse,
    OutputOrdersAmountResponse,
    ProductsAmountResponse,
    StockByBrandResponse,
    SupplierInputResponse,
    UsersAmountResponse,
    WarrantyByStatusResponse,
    CategoriesAmountResponse,
    SubcategoryStockResponse
)
from app.utils.logger import get_logger


logger = get_logger("products.repository")


class DashboardRepository:

    @staticmethod
    def find_all_and_new_products_ammount(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            (SELECT COUNT(*) FROM PRODUCTS) AS total,
            (SELECT COUNT(*)
            FROM PRODUCTS AS p
            INNER JOIN PRODUCT_SERIALS AS ps
                ON p.product_id = ps.product_id
            INNER JOIN INPUT_ORDERS AS io
                ON ps.input_order_id = io.input_order_id
            WHERE MONTH(io.input_order_date) = MONTH(CURDATE())
            AND YEAR(io.input_order_date) = YEAR(CURDATE())
            ) AS new_products"""

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                ProductsAmountResponse(
                    products=item[0],
                    new_products=item[1]
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_all_and_new_products_ammount: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los productos nuevos y totales", None

        finally:
            cursor.close()

    @staticmethod
    def find_all_suppliers_inputs(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            s.supplier_name,
            COUNT(*) AS orders
            FROM INPUT_ORDERS io
            JOIN SUPPLIERS s 
                ON io.supplier_id = s.supplier_id
            GROUP BY s.supplier_id
        """

        try:
            cursor.execute(query)

            result = cursor.fetchall()

            data = [
                SupplierInputResponse(
                    supplier_name=item[0],
                    orders=item[1]
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_all_suppliers_inputs: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las ordenes de entrada por proveedor", None

        finally:
            cursor.close()

    @staticmethod
    def find_all_outputs_by_month(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            DATE_FORMAT(out_order_date, '%M') AS month,
            COUNT(*) AS output_orders
        FROM OUTPUT_ORDERS
        GROUP BY
            DATE_FORMAT(out_order_date, '%M')
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                OutputByMonthResponse(
                    month=item[0],
                    output_orders=item[1]
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_all_outputs_by_month: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las salidas por mes", None

        finally:
            cursor.close()

    @staticmethod
    def find_all_warranties_group_by_status(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            warranty_status,
            COUNT(*) AS total
        FROM WARRANTY_INCIDENTS
        GROUP BY warranty_status
        """

        try:
            cursor.execute(query)

            result = cursor.fetchall()

            data = [
                WarrantyByStatusResponse(
                    status=item[0],
                    total=item[1]
                )
                for item in result
            ]
            return None, data

        except Exception as e:
            logger.error(
                "Error en find_all_warranties_group_by_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las garantías agrupadas por estado", None

        finally:
            cursor.close()

    @staticmethod
    def find_all_and_new_users(connection):
        cursor = connection.cursor()

        query = """
        SELECT 
        (SELECT COUNT(*) FROM USERS) AS total_users,
        (SELECT COUNT(*) 
        FROM USERS 
        WHERE MONTH(user_date) = MONTH(CURDATE())
        AND YEAR(user_date) = YEAR(CURDATE())
        ) AS new_users
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                UsersAmountResponse(
                    users=item[0],
                    new_users=item[1]
                )
                for item in result
            ]
            return None, data

        except Exception as e:
            logger.error(
                "Error en find_all_and_new_users: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los usuarios nuevos y totales", None

        finally:
            cursor.close()

    @staticmethod
    def find_stock_by_brand(connection):
        cursor = connection.cursor()

        query = """
        SELECT 
            product_brand_name AS brand,
            SUM(stock) AS products
        FROM get_all_products_with_stock
        GROUP BY product_brand_name
        ORDER BY products DESC
        LIMIT 7
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                StockByBrandResponse(
                    brand=item[0],
                    products=item[1]
                )
                for item in result
            ]
            return None, data

        except Exception as e:
            logger.error(
                "Error en find_stock_by_brand: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el stock por marca", None

        finally:
            cursor.close()

    @staticmethod
    def find_output_orders_amount(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            (SELECT COUNT(*) FROM OUTPUT_ORDERS) AS orders,
            (SELECT COUNT(*) 
        FROM OUTPUT_ORDERS 
        WHERE MONTH(out_order_date) = MONTH(CURDATE())
        AND YEAR(out_order_date) = YEAR(CURDATE())
        ) AS new_orders
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                OutputOrdersAmountResponse(
                    orders=item[0],
                    new_orders=item[1]
                )
                for item in result
            ]
            return None, data

        except Exception as e:
            logger.error(
                "Error en find_output_orders_amount: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener la cantidad de ordenes de salida", None

        finally:
            cursor.close()

    @staticmethod
    def find_categories_amount(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            (SELECT COUNT(*) FROM CATEGORIES) AS categories,
            (SELECT COUNT(*)
        FROM CATEGORIES 
        WHERE MONTH(category_date) = MONTH(CURDATE())
        AND YEAR(category_date) = YEAR(CURDATE())
        ) AS new_categories
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                CategoriesAmountResponse(
                    categories=item[0],
                    new_categories=item[1]
                )
                for item in result
            ]
            return None, data

        except Exception as e:
            logger.error(
                "Error en find_categories_amount: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las cantidad de categorias", None

        finally:
            cursor.close()

    @staticmethod
    def find_subcategories_with_stock(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            subcategory_name,
            SUM(stock) AS total_stock
        FROM get_all_products_with_stock
        GROUP BY subcategory_name
        ORDER BY total_stock DESC
        LIMIT 5
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                SubcategoryStockResponse(
                    subcategory=item[0],
                    stock=item[1]
                )
                for item in result
            ]
            return None, data

        except Exception as e:
            logger.error(
                "Error en find_subcategories_with_stock: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el stock de productos agrupado por subcategorias", None

        finally:
            cursor.close()

from app.core.database import get_connection


class DashboardRepository:

    @staticmethod
    def find_all_and_new_products_ammount():
        connection = get_connection()
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
            ) AS new_products;"""

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                {
                    "products": item[0],
                    "new_products": item[1]
                }
                for item in result
            ]

            return None, data
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            connection.close()
            cursor.close()

    @staticmethod
    def find_products_out_of_stock():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT * FROM PRODUCTS
        WHERE stock = 0
        ORDER BY product_id DESC"""
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return None, results
        except Exception:
            return f"❌ Error al ejecutar la consulta:", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_all_suppliers_inputs():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT 
            s.supplier_name, 
            COUNT(*) AS orders
            FROM INPUT_ORDERS io
            JOIN SUPPLIERS s ON io.supplier_id = s.supplier_id
            GROUP BY s.supplier_id;
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return None, result
        except Exception as e:
            return f"Error al ejecutar la consulta {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_all_outputs():
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT 
            DATE_FORMAT(out_order_date, '%M') AS month,
            COUNT(*) AS output_orders
        FROM OUTPUT_ORDERS
        GROUP BY 
            DATE_FORMAT(out_order_date, '%M');
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            # Mapeamos lo que devuelve la consulta para que tenga llaves y pueda ser usada
            data = [
                {
                    "month": item[0],
                    "output_orders": item[1]
                }
                for item in result
            ]

            return None, data
        except Exception as e:
            return f"Error al ejecutar al consulta {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_all_warranty_status():
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT 
            warranty_status,
            COUNT(*) AS total
        FROM WARRANTY_INCIDENTS
        GROUP BY warranty_status;
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                {
                    "status": item[0],
                    "total": item[1]
                }
                for item in result
            ]
            return None, data
        except Exception as e:
            return f"Error al ejecutar la consulta {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_all_and_new_users():

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT 
        (SELECT COUNT(*) FROM USERS) AS total_users,
        (SELECT COUNT(*) 
        FROM USERS 
        WHERE MONTH(user_date) = MONTH(CURDATE())
        AND YEAR(user_date) = YEAR(CURDATE())
        ) AS new_users;
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                {
                    "users": item[0],
                    "new_users": item[1]
                }
                for item in result
            ]
            return None, data
        except Exception as e:
            return f"Error al ejecutar la consulta {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_stock_by_brand():
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT 
            product_brand_name AS brand,
            SUM(stock) AS products
        FROM get_all_products_with_stock
        GROUP BY product_brand_name
        ORDER BY products DESC
        LIMIT 7;
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            data = [
                {
                    "brand": item[0],
                    "products": item[1]
                }
                for item in result
            ]
            return None, data
        except Exception as e:
            return f"Error al ejecutar la consulta {e}", None
        finally:
            connection.close()
            cursor.close()

    @staticmethod
    def find_output_orders_amount():
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            (SELECT COUNT(*) FROM OUTPUT_ORDERS) AS orders,
            (SELECT COUNT(*) 
        FROM OUTPUT_ORDERS 
        WHERE MONTH(out_order_date) = MONTH(CURDATE())
        AND YEAR(out_order_date) = YEAR(CURDATE())
        ) AS new_orders;
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                {
                    "orders": item[0],
                    "new_orders": item[1]
                }
                for item in result
            ]
            return None, data
        except Exception as e:
            return f"Error al ejecutar la consulta {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_categories_amount():
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            (SELECT COUNT(*) FROM CATEGORIES) AS categories,
            (SELECT COUNT(*)
        FROM CATEGORIES 
        WHERE MONTH(category_date) = MONTH(CURDATE())
        AND YEAR(category_date) = YEAR(CURDATE())
        ) AS new_categories;
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                {
                    "categories": item[0],
                    "new_categories": item[1]
                }
                for item in result
            ]
            return None, data
        except Exception as e:
            return f"Error al ejecutar la consulta {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_subcategories_with_stock():
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            subcategory_name,
            SUM(stock) AS total_stock
        FROM get_all_products_with_stock
        GROUP BY subcategory_name
        ORDER BY total_stock DESC
        LIMIT 5;
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            data = [
                {
                    "subcategory": item[0],
                    "stock": item[1]
                }
                for item in result
            ]
            return None, data
        except Exception as e:
            return f"Error al intentar ejecutar la consulta {e}", None
        finally:
            cursor.close()
            connection.close()

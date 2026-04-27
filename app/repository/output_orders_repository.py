from app. core.database import get_connection
from app.utils.periods import period_map, daily_periods
from app.utils.date_formatter import date_formatter


class OutputOrdersRepository:

    @staticmethod
    def find_all_output_orders():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT * FROM get_output_products ORDER BY out_order_id DESC
        """
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return None, results
        except Exception as e:
            return f"❌ Error al ejecutar la consulta: {e}", None
        finally:
            cursor.close()
            connection.close()

    # Obtener una orden de salida por ID

    @staticmethod
    def find_by_id(out_order_id: int):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """ 
        SELECT * FROM OUTPUT_ORDERS WHERE out_order_id = %s
        """
        try:
            cursor.execute(query, (out_order_id,))
            result = cursor.fetchall()
            return None, result
        except Exception as e:
            return f"❌ Error al ejecutar la consulta: {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create():
        connection = get_connection()
        cursor = connection.cursor()

        # Construir la consulta SQL dinamicamente
        query = """
        INSERT INTO OUTPUT_ORDERS (out_order_status)
        VALUES (1)
        """
        try:
            cursor.execute(query)
            connection.commit()
            output_order_id = cursor.lastrowid
            return None, True, output_order_id
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", False, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update(output_order_id: int, output_order_data: dict):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        UPDATE OUTPUT_ORDERS SET 
            out_order_status = %s
        WHERE out_order_id = %s
        """
        try:
            cursor.execute(query, (
                output_order_data["out_order_status"],
                output_order_id
            ))
            connection.commit()

            # Obtener la orden de salida actualizada
            cursor.execute(
                "SELECT * FROM OUTPUT_ORDERS WHERE out_order_id = %s", (output_order_id,))
            updated_order = cursor.fetchone()

            return None, "Orden de salida actualizada exitosamente.", updated_order
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", None, None
        finally:
            cursor.close()
            connection.close()


#   ------------ REPORTES DE ORDENES DE SALIDA ------------


    @staticmethod
    def find_recent_outputs():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            od.product_serial,
            od.out_product_garanty,
            oo.out_order_date,
            oo.out_order_status
        FROM OUTPUT_ORDERS as oo
        INNER JOIN OUTPUT_DETAILS AS od
            ON oo.out_order_id = od.out_order_id
        ORDER BY oo.out_order_date DESC
        LIMIT 6
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            data = [
                {
                    "serial": item["product_serial"],
                    "warranty_time": item["out_product_garanty"],
                    "date": date_formatter(item["out_order_date"]),
                    "status": item["out_order_status"],
                }
                for item in results
            ]
            return None, data
        except Exception as e:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_outputs_by_brand(period: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        interval = period_map.get(period, "30 DAY")

        query = f"""
        SELECT
            pb.product_brand_name,
            COUNT(DISTINCT oo.out_order_id) as outputs
        FROM OUTPUT_ORDERS AS oo
        INNER JOIN OUTPUT_DETAILS AS od
            ON oo.out_order_id = od.out_order_id
        INNER JOIN PRODUCT_SERIALS AS ps
            ON od.product_serial = ps.product_serial
        INNER JOIN PRODUCTS AS p
            ON ps.product_id = p.product_id
        INNER JOIN PRODUCT_DETAILS AS pd
            ON p.product_details_id = pd.product_details_id
        INNER JOIN PRODUCT_BRANDS AS pb
            ON pd.product_brand_id = pb.product_brand_id
        WHERE oo.out_order_date >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY pb.product_brand_name
        ORDER BY pb.product_brand_name ASC
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                {
                    "name": item["product_brand_name"],
                    "value": item["outputs"]
                }
                for item in results
            ]
            return None, data
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_outputs_by_status():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            (SELECT COUNT(*) FROM OUTPUT_ORDERS) AS total_outputs,
            COUNT(CASE WHEN out_order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_outputs,
            SUM(CASE WHEN out_order_status = 0 THEN 0 ELSE 0 END) AS inactive_outputs,
            SUM(CASE WHEN out_order_status = 1 THEN 1 ELSE 0 END) AS active_outputs
        FROM OUTPUT_ORDERS
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return None, results
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_outputs_growth(period: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if period not in period_map:
            period = "30d"

        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods

        if use_daily:
            group_expr = "DATE(out_order_date)"
            select_expr = "DATE(out_order_date) as label"
        else:
            group_expr = "DATE_FORMAT(out_order_date, '%Y-%m')"
            select_expr = "DATE_FORMAT(out_order_date, '%Y-%m') as label"

        query = f"""
        SELECT
            {select_expr},
            COUNT(DISTINCT out_order_id) as outputs
        FROM OUTPUT_ORDERS
        WHERE out_order_date >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY {group_expr}
        ORDER BY {group_expr} ASC
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return None, results
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", None
        finally:
            cursor.close()
            connection.close()

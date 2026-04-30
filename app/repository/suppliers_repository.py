from app.core.database import get_connection
from app.models.suppliers_model import Supplier, UpdateSupplier
from app.utils.periods import period_map, daily_periods
from app.utils.logger import get_logger
from app.utils.date_formatter import date_formatter

logger = get_logger(__name__)


class SuppliersRepository:

    @staticmethod
    def find_all_suppliers(
        name_order: str = None,
        start_date: str = None,
        end_date: str = None,
        status: int = None,
        city: int = None,
    ):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            s.supplier_id,
            s.supplier_name,
            s.supplier_city,
            c.city_name,
            s.supplier_address,
            s.supplier_email,
            s.supplier_phone,
            s.supplier_status,
            s.supplier_date
        FROM SUPPLIERS AS s
        INNER JOIN CITIES AS c
            ON s.supplier_city = c.city_id
        """

        filters = []
        values = []

        if start_date:
            filters.append("DATE(s.supplier_date) >= %s")
            values.append(start_date)

        if end_date:
            filters.append("DATE(s.supplier_date) <= %s")
            values.append(end_date)

        if name_order == "asc":
            query += " ORDER BY s.supplier_name ASC"
        elif name_order == "desc":
            query += " ORDER BY s.supplier_name DESC"

        if status:
            filters.append("s.supplier_status = %s")
            values.append(status)

        if city:
            filters.append("s.supplier_city = %s")
            values.append(city)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        try:
            cursor.execute(query, values)
            result = cursor.fetchall()

            data = [
                {
                    "id": item[0],
                    "name": item[1],
                    "city": item[2],
                    "city_name": item[3],
                    "address": item[4],
                    "email": item[5],
                    "phone": item[6],
                    "status": item[7],
                    "date": date_formatter(item[8])
                }
                for item in result
            ]
            return None, data
        except Exception as e:
            logger.error("Error en find_all_suppliers: %s", e, exc_info=True)
            return "Error al intentar obtener los proveedores", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_supplier_by_id(supplier_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            supplier_id,
            supplier_name,
            supplier_city,
            supplier_address,
            supplier_email,
            supplier_phone,
            supplier_status,
            supplier_date
        FROM SUPPLIERS
        WHERE supplier_id = %s"""

        try:
            cursor.execute(query, (supplier_id,))
            result = cursor.fetchall()
            data = [
                {
                    "id": item[0],
                    "name": item[1],
                    "city": item[2],
                    "address": item[3],
                    "email": item[4],
                    "phone": item[5],
                    "status": item[6],
                    "date": date_formatter(item[7])
                }
                for item in result
            ]
            return None, data
        except Exception as e:
            logger.error("Error en find_supplier_by_id: %s", e, exc_info=True)
            return "Error al intentar obtener el proveedor", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create_supplier(supplier_data: Supplier):
        data = supplier_data.model_dump()

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """
        INSERT INTO SUPPLIERS (
            supplier_name,
            supplier_email,
            supplier_phone,
            supplier_city,
            supplier_address
        ) VALUES(%s, %s, %s, %s, %s)"""

        try:
            cursor.execute(
                query, (data["name"], data["email"], data["phone"], data["city"], data["address"]))
            connection.commit()

            return None, True, "Proveedor creado correctamente"
        except Exception as e:
            logger.error("Error en create_supplier: %s", e, exc_info=True)
            return "Error al intentar crear el proveedor", None, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_supplier(supplier_id: int, supplier_data: UpdateSupplier):
        data = supplier_data.model_dump(exclude_none=True)

        SUPPLIER_FIELDS = {
            "name": "supplier_name",
            "email": "supplier_email",
            "phone": "supplier_phone",
            "city": "supplier_city",
            "address": "supplier_address",
            "status": "supplier_status"
        }

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Verificar si existe el proveedor
            cursor.execute(
                "SELECT supplier_name FROM SUPPLIERS WHERE supplier_id = %s", (supplier_id,))
            supplier = cursor.fetchone()

            if not supplier:
                return "Proveedor no encontrado", False, None

            supplier_fields = {
                key: data[key]
                for key in SUPPLIER_FIELDS.keys()
                if key in data
            }

            mapped = {
                SUPPLIER_FIELDS[key]: value for key, value in supplier_fields.items()
            }

            if not mapped:
                return "No hay campos para actualizar", False, None

            columns = ", ".join(f"{col} = %s" for col in mapped.keys())
            values = list(mapped.values()) + [supplier_id]

            cursor.execute(
                f"UPDATE SUPPLIERS SET {columns} WHERE supplier_id = %s",
                values
            )

            connection.commit()

            return None, True, "Proveedor actualizado correctamente"
        except Exception as e:
            connection.rollback()
            logger.error("Error en update_supplier: %s", e, exc_info=True)
            return "Error al ejecutar la consulta", False, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def disable_supplier(supplier_id: int):
        connection = get_connection()
        cursor = connection.cursor()

        query = "UPDATE SUPPLIERS SET supplier_status = 1 WHERE supplier_id = %s"

        try:
            # Comprobar si el proveedor existe
            cursor.execute(
                "SELECT supplier_id FROM SUPPLIERS WHERE supplier_id = %s", (supplier_id,))

            supplier = cursor.fetchone()

            if not supplier:
                return "Proveedor no encontrado", False, None

            cursor.execute(query, (supplier_id,))
            connection.commit()

            return None, True, "Proveedor deshabilitado correctamente"
        except Exception as e:
            logger.error("Error en disable_supplier: %s", e, exc_info=True)
            return "Error al intentar deshabilitar el proveedor", False, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def enable_supplier(supplier_id: int):
        connection = get_connection()
        cursor = connection.cursor()

        query = "UPDATE SUPPLIERS SET supplier_status = 2 WHERE supplier_id = %s"

        try:
            # Comprobar si el proveedor existe
            cursor.execute(
                "SELECT supplier_id FROM SUPPLIERS WHERE supplier_id = %s", (supplier_id,))

            supplier = cursor.fetchone()

            if not supplier:
                return "Proveedor no encontrado", False, None

            cursor.execute(query, (supplier_id,))
            connection.commit()

            return None, True, "Proveedor habilitado correctamente"
        except Exception as e:
            logger.error("Error en enable_supplier: %s", e, exc_info=True)
            return "Error al intentar habilitar el proveedor", False, None
        finally:
            cursor.close()
            connection.close()

#   ------------ REPORTES DE PROVEEDORES ------------

    @staticmethod
    def find_recent_suppliers():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            supplier_name,
            supplier_city,
            supplier_address,
            supplier_email,
            supplier_phone,
            supplier_date,
            supplier_status
        FROM SUPPLIERS as c
        ORDER BY supplier_id DESC
        LIMIT 6
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            data = [
                {
                    "name": item["supplier_name"],
                    "city": item["supplier_city"],
                    "address": item["supplier_address"],
                    "email": item["supplier_email"],
                    "phone": item["supplier_phone"],
                    "date": date_formatter(item["supplier_date"]),
                    "status": item["supplier_status"],
                }
                for item in results
            ]
            return None, data
        except Exception as e:
            return f"Error al ejecutar la consulta :{e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_suppliers_by_brand(period: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        interval = period_map.get(period, "30 DAY")

        query = f"""
        SELECT
            pb.product_brand_name,
            COUNT(DISTINCT s.supplier_id) as suppliers
        FROM SUPPLIERS AS s
        INNER JOIN INPUT_ORDERS AS io
            ON s.supplier_id = io.supplier_id
        INNER JOIN PRODUCT_SERIALS AS ps
            ON io.input_order_id = ps.input_order_id
        INNER JOIN PRODUCTS AS p
            ON ps.product_id = p.product_id
        INNER JOIN PRODUCT_DETAILS AS pd
            ON p.product_details_id = pd.product_details_id
        INNER JOIN PRODUCT_BRANDS AS pb
            ON pd.product_brand_id = pb.product_brand_id
        WHERE s.supplier_date >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY pb.product_brand_name
        ORDER BY pb.product_brand_name ASC
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                {
                    "name": item["product_brand_name"],
                    "value": item["suppliers"]
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
    def find_suppliers_by_status():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            (SELECT COUNT(*) FROM SUPPLIERS) AS total_suppliers,
            COUNT(CASE WHEN supplier_date >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_suppliers,
            SUM(CASE WHEN supplier_status = 0 THEN 0 ELSE 0 END) AS inactive_suppliers,
            SUM(CASE WHEN supplier_status = 1 THEN 1 ELSE 0 END) AS active_suppliers
        FROM SUPPLIERS
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
    def find_suppliers_growth(period: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if period not in period_map:
            period = "30d"

        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods

        if use_daily:
            group_expr = "DATE(supplier_date)"
            select_expr = "DATE(supplier_date) as label"
        else:
            group_expr = "DATE_FORMAT(supplier_date, '%Y-%m')"
            select_expr = "DATE_FORMAT(supplier_date, '%Y-%m') as label"

        query = f"""
        SELECT
            {select_expr},
            COUNT(DISTINCT supplier_id) as suppliers
        FROM SUPPLIERS
        WHERE supplier_date >= DATE_SUB(NOW(), INTERVAL {interval})
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

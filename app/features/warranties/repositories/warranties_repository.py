from app.utils.logger import get_logger
from app.utils.date_formatter import date_formatter
from app.core.database import get_connection
from app.utils.periods import period_map, daily_periods
from app.features.warranties.models.warranties_model import Warranty, WarrantyUpdate, WarrantiesFilter, CreateWarranty

logger = get_logger("warranties.repository")


class WarrantiesRepository:

    @staticmethod
    def find_all_warranties(filters: WarrantiesFilter, connection):
        data = filters.model_dump(exclude_none=True)

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            wi.warranty_incidents_id,
            wi.product_serial,
            wi.warranty_customer,
            wi.warranty_phone,
            wi.warranty_address,
            wi.warranty_description,
            wi.warranty_link_attachments,
            wi.warranty_city,
            c.city_name,
            wi.warranty_date,
            wi.warranty_status,
            CONCAT(u.user_name, ' ', u.user_first_surname) AS created_by,
            CONCAT(tech.user_name, ' ', tech.user_first_surname) AS assigned_to
        FROM WARRANTY_INCIDENTS AS wi
        INNER JOIN CITIES as c
            ON wi.warranty_city = c.city_id
        INNER JOIN USERS AS u
            ON wi.created_by = u.user_id
        LEFT JOIN TECHNICAL AS t
            ON wi.warranty_incidents_id = t.warranty_incidents_id
        LEFT JOIN USERS AS tech
            ON t.user_id = tech.user_id
        """

        filters = []
        values = []

        if "start_date" in data:
            filters.append("DATE(warranty_date) >= %s")
            values.append(data["start_date"])

        if "end_date" in data:
            filters.append("DATE(warranty_date) <= %s")
            values.append(data["end_date"])

        if "status" in data:
            filters.append("warranty_status = %s")
            values.append(data["status"])

        if "city" in data:
            filters.append("warranty_city = %s")
            values.append(data["city"])

        if filters:
            query += " WHERE " + " AND ".join(filters)

        try:
            cursor.execute(query, values)
            results = cursor.fetchall()

            data = [
                Warranty(
                    id=item["warranty_incidents_id"],
                    product_serial=item["product_serial"],
                    customer=item["warranty_customer"],
                    created_by=item["created_by"],
                    assigned_to=item["assigned_to"],
                    phone=item["warranty_phone"],
                    address=item["warranty_address"],
                    description=item["warranty_description"],
                    link_attachments=item["warranty_link_attachments"],
                    city=item["warranty_city"],
                    city_name=item["city_name"],
                    date=date_formatter(item["warranty_date"]),
                    status=item["warranty_status"]
                )
                for item in results
            ]

            return None, data
        except Exception as e:
            logger.error("Error en find_all_warranties: %s", e, exc_info=True)
            return "Error al intentar obtener las garantías", None
        finally:
            cursor.close()

    # Obtener una incidencia por ID
    @staticmethod
    def find_warranty_by_id(warranty_incidents_id: int, connection):
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """
        SELECT warranty_customer, warranty_status FROM WARRANTY_INCIDENTS WHERE warranty_incidents_id = %s
        """
        try:
            cursor.execute(query, (warranty_incidents_id,))
            return cursor.fetchone()
        except Exception as e:
            logger.error("Error en find_warranty_by_id: %s", e, exc_info=True)
            return None
        finally:
            cursor.close()

    @staticmethod
    def find_active_warranty_by_serial(product_serial: str, connection):
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT
                    warranty_incidents_id 
                FROM WARRANTY_INCIDENTS 
                    WHERE product_serial = %s 
                    AND warranty_status IN (2, 3)
            """, (product_serial,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(
                "Error en find_active_warranty_by_serial: %s", e, exc_info=True)
            return None
        finally:
            cursor.close()

    @staticmethod
    def create_warranty(warranty_data: CreateWarranty, user_id: int, connection):
        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        INSERT INTO WARRANTY_INCIDENTS (
            product_serial,
            warranty_customer,
            warranty_phone,
            warranty_address,
            warranty_description,
            warranty_link_attachments,
            warranty_city,
            created_by
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.execute(query, (
                warranty_data["product_serial"],
                warranty_data["customer"],
                warranty_data["phone"],
                warranty_data["address"],
                warranty_data["description"],
                warranty_data["link_attachments"],
                warranty_data["city"],
                user_id
            ))
            connection.commit()

            return None, True, "Garantía creada correctamente"
        except Exception as e:
            logger.error("Error en create_warranty: %s", e, exc_info=True)
            return "Error al intentar crear la garantía", None, None
        finally:
            cursor.close()

    @staticmethod
    def update_warranty(warranty_incidents_id: int, warranty_data: WarrantyUpdate, connection):
        WARRANTY_FIELDS = {
            "customer": "warranty_customer",
            "phone": "warranty_phone",
            "address": "warranty_address",
            "description": "warranty_description",
            "link_attachments": "warranty_link_attachments",
            "city": "warranty_city",
            "status": "warranty_status"
        }

        cursor = connection.cursor()

        try:
            mapped = {
                WARRANTY_FIELDS[key]: warranty_data[key]
                for key in WARRANTY_FIELDS
                if key in warranty_data
            }

            if not mapped:
                return "No hay campos válidos para actualizar", False, None

            columns = ", ".join(f"{col} = %s" for col in mapped.keys())
            values = list(mapped.values()) + [warranty_incidents_id]

            cursor.execute(
                f"UPDATE WARRANTY_INCIDENTS SET {columns} WHERE warranty_incidents_id = %s",
                values
            )
            return None, True, "Garantía actualizada correctamente"
        except Exception as e:
            logger.error("Error en update_warranty: %s", e, exc_info=True)
            return "Error al intentar actualizar la garantía", False, None
        finally:
            cursor.close()


#   ------------ REPORTES DE GARANTÍAS ------------

    @staticmethod
    def find_recent_warranties():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            product_serial,
            warranty_customer,
            warranty_description,
            warranty_date,
            warranty_status
        FROM WARRANTY_INCIDENTS as c
        ORDER BY warranty_incidents_id DESC
        LIMIT 6
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            data = [
                {
                    "serial": item["product_serial"],
                    "customer": item["warranty_customer"],
                    "description": item["warranty_description"],
                    "date": date_formatter(item["warranty_date"]),
                    "status": item["warranty_status"],
                }
                for item in results
            ]
            return None, data
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_warranties_by_brand(period: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        interval = period_map.get(period, "30 DAY")

        query = f"""
        SELECT
            pb.product_brand_name,
            COUNT(DISTINCT wi.warranty_incidents_id) as warranties
        FROM WARRANTY_INCIDENTS AS wi
        INNER JOIN OUTPUT_DETAILS AS od
            ON wi.product_serial = od.product_serial
        INNER JOIN PRODUCT_SERIALS AS ps
            ON od.product_serial = ps.product_serial
        INNER JOIN PRODUCTS AS p
            ON ps.product_id = p.product_id
        INNER JOIN PRODUCT_DETAILS AS pd
            ON p.product_details_id = pd.product_details_id
        INNER JOIN PRODUCT_BRANDS AS pb
            ON pd.product_brand_id = pb.product_brand_id
        WHERE wi.warranty_date >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY pb.product_brand_name
        ORDER BY pb.product_brand_name ASC
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                {
                    "name": item["product_brand_name"],
                    "value": item["warranties"]
                }
                for item in results
            ]
            return None, data
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_warranties_by_status():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            (SELECT COUNT(*) FROM WARRANTY_INCIDENTS) AS total_warranties,
            SUM(CASE WHEN warranty_status = 0 THEN 0 ELSE 0 END) AS without_make_warranties,
            SUM(CASE WHEN warranty_status = 1 THEN 1 ELSE 0 END) AS inprocess_warranties,
            SUM(CASE WHEN warranty_status = 2 THEN 1 ELSE 0 END) AS complete_warranties
        FROM WARRANTY_INCIDENTS
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return None, results
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_warranties_growth(period: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if period not in period_map:
            period = "30d"

        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods

        if use_daily:
            group_expr = "DATE(warranty_date)"
            select_expr = "DATE(warranty_date) as label"
        else:
            group_expr = "DATE_FORMAT(warranty_date, '%Y-%m')"
            select_expr = "DATE_FORMAT(warranty_date, '%Y-%m') as label"

        query = f"""
        SELECT
            {select_expr},
            COUNT(DISTINCT warranty_incidents_id) as warranties
        FROM WARRANTY_INCIDENTS
        WHERE warranty_date >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY {group_expr}
        ORDER BY {group_expr} ASC
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return None, results
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

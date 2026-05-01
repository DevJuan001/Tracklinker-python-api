from app.core.database import get_connection
from app.features.warranties.warranties_model import Warranty, WarrantyUpdate, WarrantiesFilter, CreateWarranty
from app.utils.date_formatter import date_formatter
from app.utils.periods import period_map, daily_periods
from app.utils.logger import get_logger
from app.repository.products_repository import ProductsRepository
from app.repository.output_details_repository import OutputDetailsRepository
from app.models.output_details_model import OutputDetails
from dateutil.relativedelta import relativedelta
from datetime import datetime

logger = get_logger(__name__)


class WarrantiesRepository:

    @staticmethod
    def find_all_warranties(filters: WarrantiesFilter):
        data = filters.model_dump(exclude_none=True)

        connection = get_connection()
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
            wi.warranty_status
        FROM WARRANTY_INCIDENTS AS wi
        INNER JOIN CITIES as c
            ON wi.warranty_city = c.city_id
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
            connection.close()

    # Obtener una incidencia por ID
    @staticmethod
    def find_warranty_by_id(warranty_incidents_id: int):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """
        SELECT * FROM WARRANTY_INCIDENTS WHERE warranty_incidents_id = %s
        """
        try:
            cursor.execute(query, (warranty_incidents_id,))
            result = cursor.fetchall()

            return None, result
        except Exception as e:
            logger.error("Error en find_warranty_by_id: %s", e, exc_info=True)
            return "Error al intentar obtener la garantía", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create_warranty(warranty_data: CreateWarranty):

        data = warranty_data.model_dump()

        connection = get_connection()
        cursor = connection.cursor(buffered=True)

        # Petición a la base de datos
        query = """
        INSERT INTO WARRANTY_INCIDENTS (
            product_serial,
            warranty_customer,
            warranty_phone,
            warranty_address,
            warranty_description,
            warranty_link_attachments,
            warranty_city
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.execute("""
                SELECT 
                    warranty_incidents_id 
                FROM WARRANTY_INCIDENTS 
                WHERE product_serial = %s 
                AND DATE(warranty_date) = CURDATE()
            """, (data["product_serial"],))

            existing_warranty = cursor.fetchone()

            if existing_warranty:
                return "Ya existe una garantía creada hoy para este serial", None, None

            cursor.execute("""
            SELECT 
                product_id
            FROM PRODUCT_SERIALS WHERE product_serial = %s
            """, (data["product_serial"],))

            product_id = cursor.fetchone()

            if not product_id:
                return "Serial no encontrado", None, None

            error, output_order_id, output_order_date = OutputDetailsRepository.find_by_product_serial(
                data["product_serial"])

            if error is not None:
                return error, False, None

            garanty_time = (datetime.now() + relativedelta(months=12)).date()

            if output_order_date and output_order_date.date() == datetime.now().date():
                return "Ya existe una garantía creada hoy para este serial", None, None

            if not output_order_id and not output_order_date:
                error, success, message = OutputDetailsRepository.create(OutputDetails(
                    product_serial=data["product_serial"],
                    out_product_garanty=garanty_time,
                    product_transformation="No necesita"
                ))

                if error is not None or not success:
                    return error, success, message

            error, success, message = ProductsRepository.update_product_status(
                {"product_id": product_id[0], "product_status": 4}
            )

            if error is not None or not success:
                return error, success, message

            cursor.execute(query, (
                data["product_serial"],
                data["customer"],
                data["phone"],
                data["address"],
                data["description"],
                data["link_attachments"],
                data["city"],
            ))
            connection.commit()

            return None, True, "Garantía creada correctamente"
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_warranty: %s", e, exc_info=True)

            return "Error al intentar crear la garantía", None, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_warranty(warranty_incidents_id: int, warranty_data: WarrantyUpdate):
        data = warranty_data.model_dump()

        WARRANTY_FIELDS = {
            "customer": "warranty_customer",
            "phone": "warranty_phone",
            "address": "warranty_address",
            "description": "warranty_description",
            "link_attachments": "warranty_link_attachments",
            "city": "warranty_city",
            "status": "warranty_status"
        }

        connection = get_connection()
        cursor = connection.cursor(exclude_none=True)

        try:
            # Verificar si existe la garantía
            cursor.execute(
                "SELECT warranty_incidents_id FROM WARRANTY_INCIDENTS WHERE warranty_incidents_id = %s",
                (warranty_incidents_id,)
            )
            if not cursor.fetchone():
                return "Garantía no encontrada", False, None

            warranty_fields = {
                key: data[key]
                for key in WARRANTY_FIELDS.keys()
                if key in data
            }

            mapped = {
                WARRANTY_FIELDS[key]: value for key, value in warranty_fields.items()
            }

            if not mapped:
                return "No hay campos para actualizar", False, None

            if data.get("warranty_status") == 3:
                product_serial = data.get("product_serial")

                if not product_serial:
                    return "Serial requerido para este estado", False, None

                cursor.execute("""
                SELECT
                    product_id
                FROM PRODUCT_SERIALS
                WHERE product_serial = %s
                """, (data["product_serial"],))

                row = cursor.fetchone()

                if not row:
                    return "Serial no encontrado", False, None

                product_id = row["product_id"]

                error, success, message = ProductsRepository.update_product_status({
                    "product_status": 3,
                    "product_id": product_id
                })

                if error is not None or not success:
                    return error, success, message

            columns = ", ".join(f"{col} = %s" for col in mapped.keys())
            values = list(mapped.values()) + [warranty_incidents_id]

            cursor.execute(
                f"UPDATE WARRANTY_INCIDENTS SET {columns} WHERE warranty_incidents_id = %s",
                values
            )

            connection.commit()
            return None, True, "Garantía actualizada correctamente"
        except Exception as e:
            connection.rollback()

            logger.error("Error en update_warranty: %s", e, exc_info=True)
            return "Error al intentar actualizar la garantía", False, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_warranty(warranty_incidents_id: int):
        connection = get_connection()
        cursor = connection.cursor()
        query = """
        DELETE FROM WARRANTY_INCIDENTS WHERE warranty_incidents_id = %s
        """
        try:
            cursor.execute(query, (warranty_incidents_id,))
            connection.commit()
            return None, True, "Garantía eliminada correctamente"
        except Exception as e:
            logger.error("Error en delete_warranty: %s", e, exc_info=True)
            return "Error al intentar eliminar la garantía", None, None
        finally:
            cursor.close()
            connection.close()


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



from app.utils.logger import get_logger
from app.utils.date_formatter import date_formatter
from app.utils.periods import daily_periods, period_map
from app.features.suppliers.models.suppliers_schema import CreateSupplierSchema, FilterSuppliersSchema, UpdateSupplierSchema
from app.features.suppliers.models.suppliers_response import RecentSupplierResponse, SupplierByBrandResponse, SupplierByStatusResponse, SupplierGrowthResponse, SupplierResponse


logger = get_logger("suppliers.repository")


class SuppliersRepository:

    @staticmethod
    def find_all_suppliers(filters_data: FilterSuppliersSchema, connection):
        data = filters_data.model_dump(exclude_none=True)

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

        if "start_date" in data:
            filters.append("DATE(s.supplier_date) >= %s")
            values.append(data["start_date"])

        if "end_date" in data:
            filters.append("DATE(s.supplier_date) <= %s")
            values.append(data["end_date"])

        if data.get("name_order") == "asc":
            query += " ORDER BY s.supplier_name ASC"
        elif data.get("name_order") == "desc":
            query += " ORDER BY s.supplier_name DESC"

        if "status" in data:
            filters.append("s.supplier_status = %s")
            values.append(data["status"])

        if "city" in data:
            filters.append("s.supplier_city = %s")
            values.append(data["city"])

        if filters:
            query += " WHERE " + " AND ".join(filters)

        try:
            cursor.execute(query, values)
            result = cursor.fetchall()

            data = [
                SupplierResponse(
                    id=item[0],
                    name=item[1],
                    city_id=item[2],
                    city_name=item[3],
                    address=item[4],
                    email=item[5],
                    phone=item[6],
                    status=item[7],
                    date=date_formatter(item[8])
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error("Error en find_all_suppliers: %s", e, exc_info=True)
            return "Error al intentar obtener los proveedores", None

        finally:
            cursor.close()

    @staticmethod
    def find_supplier_by_id(supplier_id: int, connection):
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
                SupplierResponse(
                    id=item[0],
                    name=item[1],
                    city_id=item[2],
                    city_name=item[3],
                    address=item[4],
                    email=item[5],
                    phone=item[6],
                    status=item[7],
                    date=date_formatter(item[8])
                )

                for item in result
            ]
            return None, data

        except Exception as e:
            logger.error("Error en find_supplier_by_id: %s", e, exc_info=True)
            return "Error al intentar obtener el proveedor", None

        finally:
            cursor.close()

    @staticmethod
    def find_supplier_by_name(supplier_name: str, connection):
        cursor = connection.cursor()

        try:
            cursor.execute("""
            SELECT
                supplier_id
            FROM SUPPLIERS
            WHERE LOWER(supplier_name) = LOWER(%s)
            """, (supplier_name,))

            supplier = cursor.fetchone()

            return None, supplier

        except Exception as e:
            logger.error("Error en find_supplier_by_name: %s",
                         e, exc_info=True)
            return "Error al intentar obtener el proveedor mediante el nombre", None, None

        finally:
            cursor.close()

    @staticmethod
    def create_supplier(supplier_data: CreateSupplierSchema, connection):
        data = supplier_data.model_dump()

        cursor = connection.cursor()

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
                query, (
                    data["name"],
                    data["email"],
                    data["phone"],
                    data["city"],
                    data["address"]
                ))

            return None, True, "Proveedor creado correctamente"

        except Exception as e:
            logger.error("Error en create_supplier: %s", e, exc_info=True)
            return "Error al intentar crear el proveedor", False, None

        finally:
            cursor.close()

    @staticmethod
    def update_supplier(supplier_id: int, supplier_data: UpdateSupplierSchema, connection):
        data = supplier_data.model_dump(exclude_none=True)

        SUPPLIER_FIELDS = {
            "name": "supplier_name",
            "email": "supplier_email",
            "phone": "supplier_phone",
            "city": "supplier_city",
            "address": "supplier_address",
            "status": "supplier_status"
        }

        cursor = connection.cursor()

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

            return None, True, "Proveedor actualizado correctamente"

        except Exception as e:
            connection.rollback()
            logger.error("Error en update_supplier: %s", e, exc_info=True)
            return "Error al ejecutar la consulta", False, None

        finally:
            cursor.close()

    @staticmethod
    def disable_supplier(supplier_id: int, connection):
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

            return None, True, "Proveedor deshabilitado correctamente"

        except Exception as e:
            logger.error("Error en disable_supplier: %s", e, exc_info=True)
            return "Error al intentar deshabilitar el proveedor", False, None

        finally:
            cursor.close()

    @staticmethod
    def enable_supplier(supplier_id: int, connection):
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

            return None, True, "Proveedor habilitado correctamente"

        except Exception as e:
            logger.error("Error en enable_supplier: %s", e, exc_info=True)
            return "Error al intentar habilitar el proveedor", False, None

        finally:
            cursor.close()

#   ------------ REPORTES DE PROVEEDORES ------------

    @staticmethod
    def find_recent_suppliers(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            s.supplier_name,
            c.city_name,
            s.supplier_address,
            s.supplier_email,
            s.supplier_phone,
            s.supplier_date,
            s.supplier_status
        FROM SUPPLIERS as s
        INNER JOIN CITIES AS c
            ON s.supplier_city = c.city_id
        ORDER BY supplier_id DESC
        LIMIT 6
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                RecentSupplierResponse(
                    name=item[0],
                    city=item[1],
                    address=item[2],
                    email=item[3],
                    phone=item[4],
                    date=date_formatter(item[5]),
                    status=item[6],
                )
                for item in results
            ]
            return None, data

        except Exception as e:
            logger.error(
                "Error en find_recent_suppliers: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los proveedores agregados recientemente", None

        finally:
            cursor.close()

    @staticmethod
    def find_suppliers_by_brand(period: str, connection):
        cursor = connection.cursor()

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
        INNER JOIN PRODUCT_MODELS as pm
            ON pd.product_model_id = pm.product_model_id
        INNER JOIN PRODUCT_BRANDS AS pb
            ON pm.product_brand_id = pb.product_brand_id
        WHERE s.supplier_date >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY pb.product_brand_name
        ORDER BY pb.product_brand_name ASC
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                SupplierByBrandResponse(
                    brand=item[0],
                    suppliers=item[1]
                )
                for item in results
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_suppliers_by_brand: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los proveedores agrupados por marca", None

        finally:
            cursor.close()

    @staticmethod
    def find_suppliers_by_status(connection):
        cursor = connection.cursor()

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

            data = [
                SupplierByStatusResponse(
                    total_suppliers=item[0],
                    recent_suppliers=item[1],
                    inactive_suppliers=item[2],
                    active_suppliers=item[3],
                )
                for item in results
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_suppliers_by_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los proveedores agrupados por estado", None

        finally:
            cursor.close()

    @staticmethod
    def find_suppliers_growth(period: str, connection):
        cursor = connection.cursor()

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

            data = [
                SupplierGrowthResponse(
                    date=item[0],
                    suppliers=item[1]
                )
                for item in results
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_suppliers_growth: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los proveedores agrupados por estado", None

        finally:
            cursor.close()

from tarfile import data_filter
from app.core.database import get_connection
from app.features.subcategories.models.subcategories_responses import ActiveCategoryResponse, SubcategoryResponse
from app.features.subcategories.models.subcategories_schemas import CreateSubcategorySchema, SubcategoriesFiltersSchema, UpdateSubcategorySchema
from app.utils.date_formatter import date_formatter
from app.utils.logger import get_logger
from app.utils.periods import daily_periods, period_map


logger = get_logger("subcategories.repository")


class SubcategoriesRepository:
    # Obtener todas las subcategorías
    @staticmethod
    def find_all_subcategories(filters: SubcategoriesFiltersSchema, connection):
        filters_data = filters.model_dump(exclude_none=True)

        cursor = connection.cursor()

        query = """
        SELECT
            c.category_id,
            c.category_name,
            s.subcategory_id,
            s.subcategory_name,
            s.subcategory_date,
            s.subcategory_status
        FROM SUBCATEGORIES AS s
        INNER JOIN CATEGORIES AS c 
            ON s.category_id = c.category_id
        """
        filters = []
        values = []

        if "start_date" in filters_data:
            filters.append("DATE(s.subcategory_date) >= %s")
            values.append(filters_data["start_date"])

        if "end_date" in filters_data:
            filters.append("DATE(s.subcategory_date) <= %s")
            values.append(filters_data["end_date"])

        if "category_order" in filters_data:
            filters.append("c.category_id = %s")
            values.append(filters_data["category_order"])

        if "status" in filters_data:
            filters.append("s.subcategory_status = %s")
            values.append(filters_data["status"])

        if filters:
            query += " WHERE " + " AND ".join(filters)

        if filters_data.get("name_order") == "asc":
            query += " ORDER BY s.subcategory_name ASC"
        elif filters_data.get("name_order") == "desc":
            query += " ORDER BY s.subcategory_name DESC"

        try:
            cursor.execute(query, values)
            result = cursor.fetchall()

            subcategories = [
                SubcategoryResponse(
                    category_id=item[0],
                    category_name=item[1],
                    subcategory_id=item[2],
                    subcategory_name=item[3],
                    subcategory_date=date_formatter(item[4]),
                    subcategory_status=item[5]
                )
                for item in result
            ]
            return None, subcategories

        except Exception as e:
            logger.error(
                "Error en find_all_subcategories: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener la subcategorias", None

        finally:
            cursor.close()

    @staticmethod
    def find_active_categories(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            category_id,
            category_name
        FROM CATEGORIES
        WHERE category_status = 2 
        """

        try:
            cursor.execute(query)

            result = cursor.fetchall()

            data = [
                ActiveCategoryResponse(
                    category_id=item[0],
                    category_name=item[1]
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_active_categories: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las categorias activas", None

        finally:
            cursor.close()

    # Obtener una subcategoría por el ID
    @staticmethod
    def find_subcategory_by_id(subcategory_id: int, connection):
        cursor = connection.cursor()

        query = """
        SELECT
            c.category_id,
            c.category_name,
            s.subcategory_id,
            s.subcategory_name,
            s.subcategory_date,
            s.subcategory_status
        FROM SUBCATEGORIES as s
        INNER JOIN CATEGORIES as c
            ON s.category_id = c.category_id
        WHERE subcategory_id = %s

        """

        try:
            cursor.execute(query, (subcategory_id,))

            result = cursor.fetchall()

            data = [
                SubcategoryResponse(
                    category_id=item[0],
                    category_name=item[1],
                    subcategory_id=item[2],
                    subcategory_name=item[3],
                    subcategory_date=date_formatter(item[4]),
                    subcategory_status=item[5]
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_subcategory_by_id: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener la subcategoría mediante el id", None

        finally:
            cursor.close()

    # Crear una nueva subcategoría
    @staticmethod
    def create_subcategory(subcategory_data: CreateSubcategorySchema, connection):
        data = subcategory_data.model_dump()

        cursor = connection.cursor()

        query = """
        INSERT INTO SUBCATEGORIES (
            category_id,
            subcategory_name
        )
        VALUES (%s, %s)
        """

        try:
            cursor.execute(query, (
                data["category_id"],
                data["subcategory_name"]
            ))

            return None, True, "Subcategoria creada correctamente"

        except Exception as e:
            logger.error(
                "Error en create_subcategory: %s",
                e,
                exc_info=True
            )
            return "Error al intentar crear la subcategoría", False, None

        finally:
            cursor.close()

    # Actualizar una subcategoría existente
    @staticmethod
    def update_subcategory(subcategory_id: int, subcategory_data: UpdateSubcategorySchema, connection):
        data = subcategory_data.model_dump(exclude_none=True)

        SUBCATEGORIES_FIELDS = {
            "category_id": "category_id",
            "subcategory_name": "subcategory_name",
        }

        cursor = connection.cursor()

        try:
            subcategories_fields = {
                key: data[key]
                for key in SUBCATEGORIES_FIELDS.keys()
                if key in data
            }

            if subcategories_fields:
                mapped = {
                    SUBCATEGORIES_FIELDS[key]: value for key,
                    value in subcategories_fields.items()
                }

                columns = ", ".join(f"{col} = %s" for col in mapped.keys())
                values = list(mapped.values()) + [subcategory_id]

                cursor.execute(
                    f"UPDATE SUBCATEGORIES SET {columns} WHERE subcategory_id = %s",
                    values
                )

            return None, True, "Subcategoria actualizada correctamente"

        except Exception as e:
            logger.error(
                "Error en update_subcategory: %s",
                e,
                exc_info=True
            )
            return "Error al intentar actualizar la subcategoría", False, None

        finally:
            cursor.close()

    @staticmethod
    def disable_subcategory(subcategory_id: int, connection):
        cursor = connection.cursor()

        query = """
        UPDATE SUBCATEGORIES SET 
            subcategory_status = 1
        WHERE subcategory_id = %s"""

        try:
            cursor.execute(query, (subcategory_id,))

            return None, True, "Categoria deshabiltiada correctamente"

        except Exception as e:
            logger.error(
                "Error en disable_subcategory: %s",
                e,
                exc_info=True
            )
            return "Error al intentar deshabilitar la subcategoria", False, None

        finally:
            cursor.close()

    @staticmethod
    def enable_subcategory(subcategory_id: int, connection):
        cursor = connection.cursor()

        query = """
        UPDATE SUBCATEGORIES SET 
            subcategory_status = 2
        WHERE subcategory_id = %s"""

        try:
            cursor.execute(query, (subcategory_id,))

            return None, True, "Categoria habiltiada correctamente"

        except Exception as e:
            logger.error(
                "Error en enable_subcategory: %s",
                e,
                exc_info=True
            )
            return "Error al ejecutar la consulta", False, None

        finally:
            cursor.close()


#   ------------ REPORTES DE SUBCATEGORIAS ------------


    @staticmethod
    def find_recent_subcategories():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            sc.subcategory_name,
            c.category_name,
            sc.subcategory_date,
            sc.subcategory_status
        FROM CATEGORIES as c
        INNER JOIN SUBCATEGORIES AS sc
            ON c.category_id = sc.category_id
        ORDER BY sc.subcategory_id DESC
        LIMIT 6
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            data = [
                {
                    "name": item["subcategory_name"],
                    "category": item["category_name"],
                    "date": date_formatter(item["subcategory_date"]),
                    "status": item["subcategory_status"],
                }
                for item in results
            ]
            return None, data
        except Exception:
            return "Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_subcategories_by_category(period: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        interval = period_map.get(period, "30 DAY")

        query = f"""
        SELECT
            c.category_name,
            COUNT(DISTINCT sc.subcategory_id) as subcategories
        FROM SUBCATEGORIES AS sc
        INNER JOIN CATEGORIES AS c
            ON sc.category_id = c.category_id
        WHERE sc.subcategory_date >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY c.category_name
        ORDER BY c.category_name ASC
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                {
                    "name": item["category_name"],
                    "value": item["subcategories"]
                }
                for item in results
            ]
            return None, data
        except Exception:
            return "Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_subcategories_by_status():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            (SELECT COUNT(*)
            FROM SUBCATEGORIES
            WHERE subcategory_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            ) AS recent_subcategories,
            (SELECT COUNT(*) FROM SUBCATEGORIES) AS total_subcategories,
            SUM(CASE WHEN subcategory_status = 1 THEN 1 ELSE 0 END) AS inactive_subcategories,
            SUM(CASE WHEN subcategory_status = 2 THEN 1 ELSE 0 END) AS active_subcategories
        FROM SUBCATEGORIES
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return None, results
        except Exception:
            return "Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_subcategories_growth(period: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if period not in period_map:
            period = "30d"

        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods

        if use_daily:
            group_expr = "DATE(subcategory_date)"
            select_expr = "DATE(subcategory_date) as label"
        else:
            group_expr = "DATE_FORMAT(subcategory_date, '%Y-%m')"
            select_expr = "DATE_FORMAT(subcategory_date, '%Y-%m') as label"

        query = f"""
        SELECT
            {select_expr},
            COUNT(DISTINCT subcategory_id) as subcategories
        FROM SUBCATEGORIES
        WHERE subcategory_date >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY {group_expr}
        ORDER BY {group_expr} ASC
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return None, results
        except Exception:
            return "Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

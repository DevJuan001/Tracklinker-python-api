from app.utils.logger import get_logger
from app.utils.date_formatter import date_formatter
from app.utils.periods import period_map, daily_periods
from app.features.categories.models.categories_schemas import CategoriesFiltersSchema, CreateCategorySchema, UpdateCategorySchema
from app.features.categories.models.categories_responses import CategoryByStatusResponse, CategoryResponse, GrowthCategoryResponse, RecentCategoryResponse

logger = get_logger("categories.repository")


class CategoriesRepository:

    # Obtener todas las categorias
    @staticmethod
    def find_all_categories(filters_data: CategoriesFiltersSchema, connection):
        data = filters_data.model_dump(exclude_none=True)

        cursor = connection.cursor(buffered=True)

        query = """
        SELECT 
            category_id,
            category_name,
            category_description,
            category_date,
            category_status
        FROM CATEGORIES"""

        filters = []
        values = []

        if "start_date" in data:
            filters.append("DATE(category_date) >= %s")
            values.append(data["start_date"])

        if "end_date" in data:
            filters.append("DATE(category_date) <= %s")
            values.append(data["end_date"])

        if "status" in data:
            filters.append("category_status = %s")
            values.append(data["status"])

        if filters:
            query += " WHERE " + " AND ".join(filters)

        if data.get("name_order") == "asc":
            query += " ORDER BY category_name ASC"
        elif data.get("name_order") == "desc":
            query += " ORDER BY category_name DESC"

        query += "ORDER BY category_id DESC LIMIT %s OFFSET %s"

        per_page = filters_data.per_page
        offset = (filters_data.page - 1) * per_page
        values += [per_page, offset]

        try:
            cursor.execute(query, values)
            result = cursor.fetchall()

            data = [
                CategoryResponse(
                    id=item[0],
                    name=item[1],
                    description=item[2],
                    date=date_formatter(item[3]),
                    status=item[4]
                )
                for item in result
            ]
            return None, data

        except Exception as e:
            logger.error("Error en find_all_categories: %s", e, exc_info=True)
            return "Error al intentar obtener las categorias", None

        finally:
            cursor.close()

    # Obtener una categoria por el ID
    @staticmethod
    def find_category_by_id(category_id: int, connection):
        cursor = connection.cursor(buffered=True)

        query = """
        SELECT
            category_id,
            category_name,
            category_description,
            category_date,
            category_status
        FROM CATEGORIES
        WHERE category_id = %s"""

        try:
            cursor.execute(query, (category_id,))
            result = cursor.fetchall()

            data = [
                CategoryResponse(
                    id=item[0],
                    name=item[1],
                    description=item[2],
                    date=date_formatter(item[3]),
                    status=item[4]
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error("Error en find_category_by_id: %s", e, exc_info=True)
            return "Error al intentar obtener la categoría", None

        finally:
            cursor.close()

    # Obtener una categoria por el ID
    @staticmethod
    def find_category_by_name(category_name: str, connection):
        cursor = connection.cursor(buffered=True)

        query = """
        SELECT
            category_id,
            category_name,
            category_description,
            category_date,
            category_status
        FROM CATEGORIES
        WHERE LOWER(category_name) = LOWER(%s)"""

        try:
            cursor.execute(query, (category_name,))
            result = cursor.fetchall()

            data = [
                CategoryResponse(
                    id=item[0],
                    name=item[1],
                    description=item[2],
                    date=date_formatter(item[3]),
                    status=item[4]
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_category_by_name: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener la categoría mediante el nombre", None

        finally:
            cursor.close()

    @staticmethod
    def create_category(category_data: CreateCategorySchema, connection):
        data = category_data.model_dump()

        cursor = connection.cursor()

        try:
            query = "INSERT INTO CATEGORIES (category_name, category_description) VALUES (%s, %s)"

            cursor.execute(
                query, (data["name"], data["description"])
            )

            return None, True, "Categoría creada correctamente"

        except Exception as e:
            logger.error("Error en create_category: %s", e, exc_info=True)
            return "Error al intentar crear la categoría", None, None

        finally:
            cursor.close()

    @staticmethod
    def update_category(category_id: int, category_data: UpdateCategorySchema, connection):
        data = category_data.model_dump(exclude_none=True)

        CATEGORY_FIELDS = {
            "name": "category_name",
            "description": "category_description"
        }

        cursor = connection.cursor(buffered=True)

        try:
            category_fields = {
                key: data[key]
                for key in CATEGORY_FIELDS.keys()
                if key in data
            }

            if category_fields:
                mapped = {
                    CATEGORY_FIELDS[key]: value for key,
                    value in category_fields.items()
                }

                columns = ", ".join(f"{col} = %s" for col in mapped.keys())
                values = list(mapped.values()) + [category_id]

                cursor.execute(
                    f"UPDATE CATEGORIES SET {columns} WHERE category_id = %s",
                    values
                )

            return None, True, "Categoría actualizada correctamente"

        except Exception as e:
            logger.error("Error en update_category: %s", e, exc_info=True)
            return "Error al intentar actualizar la categoría", None, None

        finally:
            cursor.close()

    @staticmethod
    def disable_category(category_id: int, connection):
        cursor = connection.cursor()

        query = """
        UPDATE CATEGORIES SET
            category_status = 1
        WHERE category_id = %s"""

        try:
            cursor.execute(query, (category_id,))

            return None, True, "Categoría deshabilitada correctamente"

        except Exception as e:
            logger.error("Error en disable_category: %s", e, exc_info=True)
            return "Error al intentar deshabilitar la categoría", False, None

        finally:
            cursor.close()

    @staticmethod
    def enable_category(category_id: int, connection):
        cursor = connection.cursor()

        query = """
        UPDATE CATEGORIES SET
            category_status = 2
        WHERE category_id = %s"""

        try:
            cursor.execute(query, (category_id,))

            return None, True, "Categoría habilitada correctamente"

        except Exception as e:
            logger.error("Error en enable_category: %s", e, exc_info=True)
            return "Error al intentar habilitar la categoría", False, None

        finally:
            cursor.close()

#   ------------ REPORTES DE CATEGORIAS ------------

    @staticmethod
    def find_recent_categories(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            category_name,
            category_date,
            category_description,
            category_status
        FROM CATEGORIES
        ORDER BY category_id DESC
        LIMIT 6
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                RecentCategoryResponse(
                    name=item[0],
                    date=date_formatter(item[1]),
                    description=item[2],
                    status=item[3],
                )
                for item in results
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_recent_categories: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las categorias recientes", None

        finally:
            cursor.close()

    @staticmethod
    def find_categories_by_status(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            (SELECT COUNT(*)
            FROM CATEGORIES
            WHERE category_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            ) AS recent_categories,
            (SELECT COUNT(*) FROM CATEGORIES) AS total_categories,
            SUM(CASE WHEN category_status = 1 THEN 1 ELSE 0 END) AS inactive_categories,
            SUM(CASE WHEN category_status = 2 THEN 1 ELSE 0 END) AS active_categories
        FROM CATEGORIES
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                CategoryByStatusResponse(
                    recent_categories=item[0],
                    total_categories=item[1],
                    inactive_categories=item[2],
                    active_categories=item[3]
                )
                for item in results
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_categories_by_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las categorias agrupadas por estado", None

        finally:
            cursor.close()

    @staticmethod
    def find_categories_growth(period: str, connection):
        cursor = connection.cursor()

        if period not in period_map:
            period = "30d"

        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods

        if use_daily:
            group_expr = "DATE(category_date)"
            select_expr = "DATE(category_date) as label"
        else:
            group_expr = "DATE_FORMAT(category_date, '%Y-%m')"
            select_expr = "DATE_FORMAT(category_date, '%Y-%m') as label"

        query = f"""
        SELECT
            {select_expr},
            COUNT(DISTINCT category_id) as categories
        FROM CATEGORIES
        WHERE category_date >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY {group_expr}
        ORDER BY {group_expr} ASC
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                GrowthCategoryResponse(
                    date=item[0],
                    categories=item[1]
                )
                for item in results
            ]

            return None, data

        except Exception as e:
            logger.error(
                "Error en find_categories_growth: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el crecimiento de las categorias", None

        finally:
            cursor.close()

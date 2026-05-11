from app.core.database import get_connection
from datetime import datetime
from app.utils.date_formatter import date_formatter
from app.utils.periods import period_map, daily_periods


class SubcategoriesRepository:
    # Obtener todas las subcategorías
    @staticmethod
    def find_all_subcategories(
        start_date: str = None,
        end_date: str = None,
        category_order: int = None,
        status: int = None,
        name_order: str = None,
    ):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

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

        if start_date:
            filters.append("DATE(s.subcategory_date) >= %s")
            values.append(start_date)

        if end_date:
            filters.append("DATE(s.subcategory_date) <= %s")
            values.append(end_date)

        if category_order:
            filters.append("c.category_id = %s")
            values.append(category_order)

        if name_order == "asc":
            query += " ORDER BY s.subcategory_name ASC"
        elif name_order == "desc":
            query += " ORDER BY s.subcategory_name DESC"

        if status:
            filters.append("s.subcategory_status = %s")
            values.append(status)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        try:
            cursor.execute(query, values)
            result = cursor.fetchall()

            data = [
                {
                    "category_id": item["category_id"],
                    "category_name": item["category_name"],
                    "subcategory_id": item["subcategory_id"],
                    "subcategory_name": item["subcategory_name"],
                    "subcategory_date": date_formatter(item["subcategory_date"]),
                    "subcategory_status": item["subcategory_status"]
                }
                for item in result
            ]
            return None, data
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_categories():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

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

            return None, result
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    # Obtener una subcategoría por el ID
    @staticmethod
    def find_by_id(subcategory_id: int):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """
        SELECT * FROM SUBCATEGORIES WHERE subcategory_id 
        INNER JOIN CATEGORIES 
        ON SUBCATEGORIES.category_id = CATEGORIES.category_id
        WHERE subcategory_id = %s

        """

        try:
            cursor.execute(query, (subcategory_id,))
            result = cursor.fetchone()
            return None, result
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    # Crear una nueva subcategoría
    @staticmethod
    def create_subcategory(subcategory_data: dict):
        connection = get_connection()
        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        INSERT INTO SUBCATEGORIES (subcategory_name, category_id)
        VALUES (%s, %s)
        """

        try:
            cursor.execute(query, (
                subcategory_data["subcategory_name"],
                subcategory_data["category_id"]
            ))
            connection.commit()
            return None, cursor.lastrowid
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    # Actualizar una subcategoría existente
    @staticmethod
    def update_subcategory(subcategory_id: int, subcategory_data: dict):
        connection = get_connection()
        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        UPDATE SUBCATEGORIES
        SET subcategory_name = %s, category_id = %s
        WHERE subcategory_id = %s
        """

        try:
            cursor.execute(query, (
                subcategory_data["subcategory_name"],
                subcategory_data["category_id"],
                subcategory_id
            ))
            connection.commit()
            cursor.execute(
                "SELECT * FROM SUBCATEGORIES WHERE subcategory_id = %s", (subcategory_id,))
            result = cursor.fetchall()

            data = [
                {
                    "category_id": item[0],
                    "subcategory_id": item[1],
                    "subcategory_name": item[2]
                }
                for item in result
            ]
            return None, cursor.rowcount, data
        except Exception:
            return f"Error al ejecutar la consulta", None, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def disable_subcategory(subcategory_id: int):
        connection = get_connection()
        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        UPDATE SUBCATEGORIES SET 
            subcategory_status = 1
        WHERE subcategory_id = %s"""

        try:
            cursor.execute(query, (subcategory_id,))
            connection.commit()
            return None, "Categoria deshabiltiada correctamente"
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def enable_subcategory(subcategory_id: int):
        connection = get_connection()
        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        UPDATE SUBCATEGORIES SET 
            subcategory_status = 2
        WHERE subcategory_id = %s"""

        try:
            cursor.execute(query, (subcategory_id,))
            connection.commit()
            return None, "Categoria deshabiltiada correctamente"
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    # Obtener subcategorías por categoría ID
    @staticmethod
    def find_by_category_id(category_id: int):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """
        SELECT * FROM SUBCATEGORIES 
        WHERE category_id = %s
        """

        try:
            cursor.execute(query, (category_id,))
            results = cursor.fetchall()
            return None, results
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_subcategories_by_date_range(start_date: str, end_date: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """
        SELECT * FROM SUBCATEGORIES 
        WHERE created_at BETWEEN %s AND %s
        """

        try:
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            return None, results
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_deleted_subcategories_by_date_range(start_date: str, end_date: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """
        SELECT * FROM SUBCATEGORIES 
        WHERE deleted_at BETWEEN %s AND %s
        """

        try:
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            return None, results
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_disabled_subcategories():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """
        SELECT * FROM SUBCATEGORIES 
        WHERE is_disabled = TRUE
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

    # Obtener subcategorías actualizadas antes de una fecha específica
    @staticmethod
    def find_updated_before(date: datetime):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """
        SELECT * FROM SUBCATEGORIES 
        WHERE updated_at < %s
        """

        try:
            cursor.execute(query, (date,))
            results = cursor.fetchall()
            return None, results
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    # Obtener subcategorías por estado (activo/inactivo)
    @staticmethod
    def find_by_status(is_active: bool):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Petición a la base de datos
        query = """
        SELECT * FROM SUBCATEGORIES 
        WHERE is_active = %s
        """

        try:
            cursor.execute(query, (is_active,))
            results = cursor.fetchall()
            return None, results
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    # Activar o desactivar una subcategoría
    @staticmethod
    def set_active_status(subcategory_id: int, is_active: bool):
        connection = get_connection()
        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        UPDATE SUBCATEGORIES
        SET is_active = %s
        WHERE subcategory_id = %s
        """

        try:
            cursor.execute(query, (is_active, subcategory_id))
            connection.commit()
            return None, cursor.rowcount
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

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
            return f"Error al ejecutar la consulta", None
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
            return f"Error al ejecutar la consulta", None
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
            return f"Error al ejecutar la consulta", None
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
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

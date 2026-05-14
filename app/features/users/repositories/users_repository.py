import bcrypt
from app.utils.logger import get_logger
from app.utils.date_formatter import date_formatter
from app.utils.periods import period_map, daily_periods
from app.features.users.models.roles_responses import RolResponse
from app.features.users.models.cities_reponses import CityResponse
from app.features.users.models.users_schemas import CreateUserSchema, UpdateUserSchema, UsersFiltersSchema
from app.features.users.models.users_responses import CurrentUserResponse, RecentUserResponse, UserResponse, UsersByRolResponse, UsersByStatusResponse, UsersGrowthResponse

logger = get_logger("users.repository")


class UsersRepository:

    # Obtener todos los usuarios
    @staticmethod
    def find_all_users(filters_data: UsersFiltersSchema, connection):
        data = filters_data.model_dump(exclude_none=True)

        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        SELECT
            r.rol_id,
            r.rol_name,
            u.user_id,
            u.user_name,
            u.user_first_surname,
            u.user_second_surname,
            u.user_phone,
            u.user_email,
            u.user_address,
            u.user_city,
            c.city_name,
            u.user_date,
            u.user_status
        FROM USERS AS u 
        INNER JOIN ROLES AS r 
            ON u.rol_id = r.rol_id
        INNER JOIN CITIES AS c
            ON u.user_city = c.city_id
        """

        filters = []
        values = []

        if "role_order" in data:
            filters.append("r.rol_id = %s")
            values.append(data["role_order"])

        if "start_date" in data:
            filters.append("DATE(u.user_date) >= %s")
            values.append(data["start_date"])

        if "end_date" in data:
            filters.append("DATE(u.user_date) <= %s")
            values.append(data["end_date"])

        if "status" in data:
            filters.append("u.user_status = %s")
            values.append(data["status"])

        if "city" in data:
            filters.append("u.user_city = %s")
            values.append(data["city"])

        if filters:
            query += " WHERE " + " AND ".join(filters)

        if data.get("name_order") == "asc":
            query += " ORDER BY u.user_name ASC"
        elif data.get("name_order") == "desc":
            query += " ORDER BY u.user_name DESC"

        try:
            cursor.execute(query, values)

            results = cursor.fetchall()

            users = [
                UserResponse(
                    rol_id=item[0],
                    rol_name=item[1],
                    id=item[2],
                    name=item[3],
                    first_surname=item[4],
                    second_surname=item[5],
                    phone=item[6],
                    email=item[7],
                    address=item[8],
                    city=item[9],
                    city_name=item[10],
                    date=date_formatter(item[11]),
                    status=item[12]
                )
                for item in results
            ]
            return None, users

        except Exception as e:
            logger.error("Error en find_all_users: %s", e, exc_info=True)
            return "Error al intentar obtener todos los usuarios", None

        finally:
            cursor.close()

    # Obtener un usuario por el ID
    @staticmethod
    def find_user_by_id(user_id: int, connection):
        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        SELECT
            u.user_id,
            u.user_name,
            u.user_first_surname,
            u.user_second_surname,
            u.user_phone,
            u.user_email,
            u.user_address,
            u.user_city
        FROM USERS AS u 
        INNER JOIN ROLES AS r 
            ON u.rol_id = r.rol_id
        INNER JOIN CITIES AS c
            ON u.user_city = c.city_id
        WHERE user_id = %s
        """

        try:
            cursor.execute(query, (user_id,))

            result = cursor.fetchall()

            if not result:
                return "Usuario no encontrado", None

            data = [
                CurrentUserResponse(
                    id=item[0],
                    name=item[1],
                    first_surname=item[2],
                    second_surname=item[3],
                    phone=item[4],
                    email=item[5],
                    address=item[6],
                    city=item[7],
                )
                for item in result
            ]
            return None, data
        except Exception as e:
            logger.error("Error en find_user_by_id: %s", e, exc_info=True)
            return "Error al intentar obtener el usuario", None
        finally:
            cursor.close()

    @staticmethod
    def find_user_password_by_id(user_id: int, connection):
        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        SELECT
            user_password
        FROM USERS
        WHERE user_id = %s
        """

        try:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if not result:
                return "Usuario no encontrado", None

            return None, result

        except Exception as e:
            logger.error(
                "Error en find_user_password_by_id: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el usuario", None

        finally:
            cursor.close()

    # Obtener un usuario mediante el correo
    @staticmethod
    def find_user_by_email(email: str, connection):
        cursor = connection.cursor(buffered=True)

        # Petición a la base de datos
        query = """
        SELECT
            r.rol_name,
            u.user_id,
            u.user_name,
            u.user_first_surname,
            u.user_second_surname,
            u.user_email, 
            u.user_password
        FROM USERS AS u 
        INNER JOIN ROLES AS r 
            ON r.rol_id = u.rol_id 
        WHERE u.user_email = %s
        """

        try:
            cursor.execute(query, (email,))

            result = cursor.fetchone()

            return None, result

        except Exception as e:
            logger.error("Error en find_user_by_email: %s", e, exc_info=True)
            return "Error al intentar obtener el usuario mediante el correo", None

        finally:
            cursor.close()

    # Crear un usuario
    @staticmethod
    def create_user(user_data: CreateUserSchema, hash_password: str, connection):
        data = user_data.model_dump()

        cursor = connection.cursor()

        # Petición a la base de datos
        query = """INSERT INTO USERS (
            rol_id,
            user_name,
            user_first_surname,
            user_second_surname,
            user_address,
            user_city,
            user_password,
            user_email,
            user_phone
        ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            cursor.execute(query, (
                data["rol_id"],
                data["name"],
                data["first_surname"],
                data["second_surname"],
                data["address"],
                data["city"],
                hash_password,
                data["email"],
                data["phone"]))

            return None, True, "Usuario creado correctamente"

        except Exception as e:
            logger.error("Error en create_user: %s", e, exc_info=True)
            return "Error al intentar crear el usuario", False, None

        finally:
            cursor.close()

    # Actualizar la información de un usuario
    @staticmethod
    def update_user(user_id: int, user_data: UpdateUserSchema, connection):
        data = user_data.model_dump(exclude_none=True)

        USER_FIELDS = {
            "name": "user_name",
            "first_surname": "user_first_surname",
            "second_surname": "user_second_surname",
            "email": "user_email",
            "phone": "user_phone",
            "city": "user_city",
            "address": "user_address",
            "status": "user_status"
        }

        cursor = connection.cursor()

        try:
            user_fields = {
                key: data[key]
                for key in USER_FIELDS.keys()
                if key in data
            }

            if user_fields:
                mapped = {
                    USER_FIELDS[key]: value for key, value in user_fields.items()}

                columns = ", ".join(f"{col} = %s" for col in mapped.keys())
                values = list(mapped.values()) + [user_id]

                cursor.execute(
                    f"UPDATE USERS SET {columns} WHERE user_id = %s",
                    values
                )

            return None, True, "Usuario actualizado correctamente"

        except Exception as e:
            logger.error("Error en update_user: %s", e, exc_info=True)
            return "Error al intentar actualizar el usuario", False, None

        finally:
            cursor.close()

    @staticmethod
    def update_user_password(user_id: int, password: str, connection):
        cursor = connection.cursor()

        query = """
        UPDATE USERS SET
            user_password = %s
        WHERE user_id = %s
        """
        new_password = password.encode("utf-8")
        hash_password = bcrypt.hashpw(
            new_password, bcrypt.gensalt(rounds=12)).decode("utf-8")

        try:
            cursor.execute(query, (hash_password, user_id))

            return None, True, "Contraseña actualizada correctamente"

        except Exception:
            return "Error al intentar actualizar la contraseña", False, None

        finally:
            cursor.close()

    # Deshabilitar un usuario
    @staticmethod
    def disable_user(user_id: int, connection):
        cursor = connection.cursor()

        query = "UPDATE USERS SET user_status = 1 WHERE user_id = %s"

        try:
            cursor.execute(query, (user_id,))
            return None, True, "Usuario deshabilitado correctamente"

        except Exception as e:
            logger.error("Error en disable_user: %s", e, exc_info=True)
            return "Error la intentar deshabilitar el usuario", False, None

        finally:
            cursor.close()

    # Habilitar un usuario
    @staticmethod
    def enable_user(user_id: int, connection):
        cursor = connection.cursor()

        query = "UPDATE USERS SET user_status = 2 WHERE user_id = %s"

        try:
            cursor.execute(query, (user_id,))

            return None, True, "Usuario habilitado correctamente"

        except Exception as e:
            logger.error("Error en enable_user: %s", e, exc_info=True)
            return "Error la intentar habilitar el usuario", False, None

        finally:
            cursor.close()

    #   ------------ REPORTES DE USUARIOS ------------

    @staticmethod
    def find_recent_users(connection):
        cursor = connection.cursor()

        try:

            query = """
            SELECT
                user_name,
                user_first_surname,
                user_email,
                user_phone,
                user_date,
                user_status
            FROM USERS
            ORDER BY user_date DESC
            LIMIT 6
            """

            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                RecentUserResponse(
                    name=item[0],
                    surname=item[1],
                    email=item[2],
                    phone=item[3],
                    date=date_formatter(item[4]),
                    status=item[5]
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error("Error en find_recent_users: %s", e, exc_info=True)
            return "Error al intentar obtener los usuarios recientes", None

        finally:
            cursor.close()

    @staticmethod
    def find_users_by_rol(period: str, connection):
        cursor = connection.cursor()

        try:
            if period not in period_map:
                period = "30d"

            interval = period_map.get(period, "30 DAY")

            query = f"""
            SELECT
                r.rol_name,
                COUNT(u.user_id) as users
            FROM USERS AS u 
            INNER JOIN ROLES AS r
            ON u.rol_id = r.rol_id
            WHERE u.user_date >= DATE_SUB(NOW(), INTERVAL {interval})
            GROUP BY r.rol_name
            """

            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                UsersByRolResponse(
                    rol=item[0],
                    users=item[1]
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error("Error en find_users_by_rol: %s", e, exc_info=True)
            return "Error al intentar obtener los usuarios por rol", None

        finally:
            cursor.close()

    @staticmethod
    def find_users_growth(period: str, connection):
        cursor = connection.cursor()

        if period not in period_map:
            period = "30d"

        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods

        if use_daily:
            group_expr = "DATE(user_date)"
            select_expr = "DATE(user_date) as label"
        else:
            group_expr = "DATE_FORMAT(user_date, '%Y-%m')"
            select_expr = "DATE_FORMAT(user_date, '%Y-%m') as label"

        query = f"""
        SELECT
            {select_expr},
            COUNT(DISTINCT user_id) as users
        FROM USERS
        WHERE user_date >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY {group_expr}
        ORDER BY {group_expr} ASC
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                UsersGrowthResponse(
                    date=item[0],
                    users=item[1]
                )
                for item in results
            ]

            return None, data

        except Exception as e:
            logger.error("Error en find_users_growth: %s", e, exc_info=True)
            return "Error al intentar obtener el crecimiento de los usuarios", None

        finally:
            cursor.close()

    @staticmethod
    def find_users_by_status(connection):
        cursor = connection.cursor()

        query = """
        SELECT
            COUNT(CASE WHEN user_date >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_users,
            COUNT(CASE WHEN user_status = 2 THEN 1 END) as active_users,
            COUNT(CASE WHEN user_status = 1 THEN 1 END) as inactive_users,
            COUNT(user_id) as total_users
        FROM USERS
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = [
                UsersByStatusResponse(
                    recent_users=item[0],
                    active_users=item[1],
                    inactive_users=item[2],
                    total_users=item[3]
                )
                for item in results
            ]

            return None, data

        except Exception as e:
            logger.error("Error en find_users_by_status: %s", e, exc_info=True)
            return "Error al intentar obtener los usuarios por estado", None

        finally:
            cursor.close()

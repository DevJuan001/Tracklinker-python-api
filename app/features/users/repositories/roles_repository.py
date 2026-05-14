from app.features.users.models.roles_responses import RolResponse
from app.utils.logger import get_logger

logger = get_logger("roles.repository")


class RolesRepository:
    @staticmethod
    def find_all_roles(connection):
        cursor = connection.cursor()

        query = "SELECT rol_id, rol_name FROM ROLES"

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            data = [
                RolResponse
                (
                    id=item[0],
                    name=item[1]
                )
                for item in result
            ]
            return None, data
        
        except Exception as e:
            logger.error("Error en find_all_roles: %s", e, exc_info=True)
            return "Error al intentar obtener los roles"
        
        finally:
            cursor.close()

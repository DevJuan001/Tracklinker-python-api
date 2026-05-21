from app.utils.logger import get_logger
from app.features.users.models.cities_reponses import CityResponse

logger = get_logger("cities.repository")


class CitiesRepository:
    # Obtener todas las ciudades
    @staticmethod
    def find_all_cities(connection):
        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        SELECT
            city_id,
            city_name
        FROM CITIES
        """

        try:
            cursor.execute(query)

            result = cursor.fetchall()

            data = [
                CityResponse(
                    id=item[0],
                    name=item[1]
                )
                for item in result
            ]

            return None, data

        except Exception as e:
            logger.error("Error en find_all_cities: %s", e, exc_info=True)
            return "Error al intentar obtener las ciudades", None

        finally:
            cursor.close()

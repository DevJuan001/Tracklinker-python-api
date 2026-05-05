from app.utils.logger import get_logger

logger = get_logger("technicians.repository")


class TechniciansRepository:
    @staticmethod
    def assign_technician(warranty_id: int, user_id: int, connection):
        cursor = connection.cursor()

        try:
            cursor.execute(
                """INSERT INTO TECHNICAL (
                    user_id,
                    warranty_incidents_id
                ) VALUES (%s, %s)""", (
                    user_id, warranty_id
                )
            )

            return None, True, "Técnico asignado correctamente"
        except Exception as e:
            logger.error("Error en assign_technician: %s", e, exc_info=True)
            return "Error al intentar asignar el técnico", False, None
        finally:
            cursor.close()

    @staticmethod
    def unassign_technician(warranty_id: int, connection):
        cursor = connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM TECHNICAL WHERE warranty_incidents_id = %s",
                (warranty_id,),
            )

            return None, True, "Técnico desasignado correctamente"
        except Exception as e:
            logger.error("Error en unassign_technician: %s", e, exc_info=True)
            return "Error al intentar desasignar el técnico", False, None
        finally:
            cursor.close()

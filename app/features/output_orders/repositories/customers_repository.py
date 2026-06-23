from app.utils.logger import get_logger

logger = get_logger("customers.repository")


class CustomersRepository:

    # Relacionar un cliente con una orden de salida
    @staticmethod
    def create_customer(client_id: int, out_order_id: int, connection):
        cursor = connection.cursor()

        query = """
        INSERT INTO CUSTOMERS (user_id, out_order_id) VALUES (%s, %s)
        """

        try:
            cursor.execute(query, (client_id, out_order_id))

            return None, True, "Cliente relacionado con la orden de salida correctamente"

        except Exception as e:
            logger.error("Error en create_customer: %s", e, exc_info=True)
            return "Error al intentar relacionar el cliente con la orden de salida", False, None

        finally:
            cursor.close()

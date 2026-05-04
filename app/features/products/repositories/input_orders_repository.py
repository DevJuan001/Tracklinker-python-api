from app.utils.logger import get_logger
from app.features.products.models.input_order_model import InputOrder, CreateInputOrder

logger = get_logger("input_orders.repository")


class InputOrdersRepository:

    @staticmethod
    def find_all_input_orders(connection):
        cursor = connection.cursor()

        query = "SELECT input_order_id, input_order_bill FROM INPUT_ORDERS"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            data = [
                InputOrder(
                    id=item[0],
                    bill=item[1]
                )
                for item in result
            ]
            return None, data
        except Exception as e:
            logger.error(
                "Error en find_all_input_orders: %s",
                e,
                exc_info=True
            )
            return "Error al obtener las ordenes de entrada", None
        finally:
            cursor.close()

    @staticmethod
    def create_input_order(input_order_data: CreateInputOrder, connection):
        cursor = connection.cursor()

        try:
            cursor.execute("""
            INSERT INTO INPUT_ORDERS(
                input_order_bill,
                supplier_id
            ) VALUES (%s, %s)
            """, (
                input_order_data["input_order_bill"],
                input_order_data["supplier_id"]
            ))

            return None, True, "Orden de entrada creada correctamente"
        except Exception as e:
            logger.error("Error en create_input_order: %s", e, exc_info=True)
            return "Error al intentar crear la orden de entrada", False, None
        finally:
            cursor.close()

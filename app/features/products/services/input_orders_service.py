from app.utils.logger import get_logger
from app.core.database import get_connection
from app.features.products.models.input_order_model import CreateInputOrder
from app.features.products.repositories.input_orders_repository import InputOrdersRepository

logger = get_logger("input_orders.service")


class InputOrdersService:
    @staticmethod
    def get_all_input_orders():
        connection = get_connection()

        try:
            error, products = InputOrdersRepository.find_all_input_orders(
                connection
            )
            if error:
                return "Error al intentar obtener las ordenes de entrada", None

            return None, products
        except Exception as e:
            connection.rollback()
            logger.error("Error en get_all_input_orders: %s", e, exc_info=True)
            return "Error al intentar obtener las ordenes de entrada", None

    @staticmethod
    def create_input_order(input_order_data: CreateInputOrder):
        data = input_order_data.model_dump()

        connection = get_connection()

        try:
            error, success, message = InputOrdersRepository.create_input_order(
                data, connection
            )
            if error:
                return "Error al intentar crear la orden de entrada", False, None

            connection.commit()

            return None, True, "Orden de entrada creada correctamente"
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_input_order: %s", e, exc_info=True)
            return "Error al intentar crear la orden de entrada", None

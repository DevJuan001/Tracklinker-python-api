

from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.products.models.schemas.input_orders_schemas import CreateInputOrderSchema
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
                raise ServiceError(error)

            return None, products

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_all_input_orders: %s", e, exc_info=True)
            return "Error al intentar obtener las ordenes de entrada", None

    @staticmethod
    def create_input_order(input_order_data: CreateInputOrderSchema):
        data = input_order_data.model_dump()

        connection = get_connection()

        try:
            error, success, message = InputOrdersRepository.create_input_order(
                data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Orden de entrada creada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en create_input_order: %s", e, exc_info=True)
            return "Error al intentar crear la orden de entrada", None

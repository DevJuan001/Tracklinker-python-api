from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.output_orders.models.output_orders_model import OutputOrdersFilters
from app.features.output_orders.repositories.output_orders_repository import OutputOrdersRepository
from app.features.output_orders.repositories.output_details_repository import OutputDetailsRepository

logger = get_logger("output_orders.service")


class OutputOrdersService:
    @staticmethod
    def get_all_output_orders(filters: OutputOrdersFilters):
        connection = get_connection()

        try:
            error, output_orders = OutputOrdersRepository.find_all_output_orders(
                filters, connection
            )

            if error:
                raise ServiceError(error)

            return None, output_orders
        except ServiceError as e:
            return e.message, False, None

        finally:
            connection.close()

    @staticmethod
    def get_output_order_by_id():
        connection = get_connection()

    @staticmethod
    def create_output_order():
        connection = get_connection()

    @staticmethod
    def update_output_order():
        connection = get_connection()

    @staticmethod
    def delete_output_order():
        connection = get_connection()

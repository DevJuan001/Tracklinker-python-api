from app.features.products.repositories.product_serials_repository import ProductSerialsRepository
from app.features.products.routes import products_routes
from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.output_orders.models.output_orders_model import CreateOutputOrder, OutputOrdersFilters, UpdateOutputOrder
from app.features.output_orders.models.output_details_model import CreateOutputDetails, UpdateOutputDetails
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
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_output_orders: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las ordenes de salida", None
        finally:
            connection.close()

    @staticmethod
    def get_output_order_by_id(output_order_id: int):
        connection = get_connection()

        try:
            error, output_orders = OutputOrdersRepository.find_output_order_by_id(
                output_order_id, connection
            )

            if error:
                raise ServiceError(error)

            return None, output_orders
        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_output_order_by_id: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener la orden de salida", None
        finally:
            connection.close()

    @staticmethod
    def create_output_order(output_order_data: CreateOutputOrder):
        data = output_order_data.model_dump()

        connection = get_connection()
        try:
            error, success, output_order_id = OutputOrdersRepository.create_output_order(
                connection
            )
            if error or not success:
                raise ServiceError(error)

            error, success, message = OutputDetailsRepository.create_output_details(
                output_order_id,
                CreateOutputDetails(
                    product_serial=data["product_serial"],
                    output_product_garanty=data["output_product_garanty"],
                    product_transformation=data["product_transformation"]
                ),
                connection
            )
            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Orden de salida creada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            logger.error("Error en create_output_order: %s", e, exc_info=True)
            return "Error al intentar crear la orden de salida", False, None
        finally:
            connection.close()

    @staticmethod
    def update_output_order(output_order_id: int, output_order_data: UpdateOutputOrder):
        data = output_order_data.model_dump(exclude_none=True)

        connection = get_connection()

        try:
            if "product_serial" in data:
                error, serial = ProductSerialsRepository.find_product_by_serial(
                    serial=data["product_serial"],
                    connection=connection
                )
                if error or not serial:
                    raise ServiceError(error)

            error, output_details = OutputDetailsRepository.find_output_details_by_output_order_id(
                output_order_id, connection
            )

            if error:
                raise ServiceError(error)

            if details_fields := {
                key: data[key]
                for key in ["product_serial", "output_product_garanty", "product_transformation"]
                if key in data
            }:
                error, success, message = OutputDetailsRepository.update_output_details(
                    output_details_id=output_details[0],
                    output_details_data=UpdateOutputDetails(
                        **details_fields
                    ),
                    connection=connection
                )
                if error or not success:
                    raise ServiceError(error)

            error, success, message = OutputOrdersRepository.update_output_order(
                output_order_id=output_order_id,
                output_order_data={
                    "output_order_status": data["output_order_status"]
                },
                connection=connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Orden de salida actualizada exitosamente"
        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            logger.error("Error en update_output_order: %s", e, exc_info=True)
            return "Error al intentar actualizar la orden de salida", False, None
        finally:
            connection.close()

    @staticmethod
    def disable_output_order(output_order_id: int):
        connection = get_connection()

        try:
            error, output_order = OutputOrdersRepository.find_output_order_by_id(
                output_order_id, connection
            )

            if error or not output_order:
                raise ServiceError(error)

            error, success, message = OutputOrdersRepository.disable_output_order(
                output_order_id,
                connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Orden de salida deshabilitada exitosamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            logger.error("Error en disable_output_order: %s", e, exc_info=True)
            return "Error al intentar deshabilitar la orden de salida", False, None

    @staticmethod
    def enable_output_order(output_order_id: int):
        connection = get_connection()

        try:
            error, output_order = OutputOrdersRepository.find_output_order_by_id(
                output_order_id, connection
            )

            if error or not output_order:
                raise ServiceError(error)

            error, success, message = OutputOrdersRepository.enable_output_order(
                output_order_id,
                connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Orden de salida habilitada exitosamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            logger.error("Error en enable_output_order: %s", e, exc_info=True)
            return "Error al intentar habilitar la orden de salida", False, None

from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.products.repositories.product_details_repository import ProductDetailsRepository
from app.features.products.models.entities.product_details_entity import CreateProductDetailsEntity, UpdateProductDetailsEntity


logger = get_logger("product_details.service")


class ProductDetailsService:
    @staticmethod
    def create_product_details(details_data: CreateProductDetailsEntity):
        data = details_data.model_dump()

        connection = get_connection()

        try:
            error, success, message = ProductDetailsRepository.create_product_details(
                data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Detalles del producto creados correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en create_product_brand: %s", e, exc_info=True)
            return "Error al intentar crear los detalles del producto", False, None

        finally:
            connection.close()

    @staticmethod
    def update_product_details(details_data: UpdateProductDetailsEntity):
        data = details_data.model_dump()

        connection = get_connection()

        try:
            error, success, message = ProductDetailsRepository.update_product_details(
                data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Detalles del producto actualizados correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error(
                "Error en update_product_details: %s",
                e,
                exc_info=True
            )
            return "Error al intentar actualizar los detalles del producto", False, None

        finally:
            connection.close()

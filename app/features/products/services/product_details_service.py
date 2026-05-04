from app.features.products.repositories.product_details_repository import ProductDetailsRepository
from app.utils.logger import get_logger
from app.core.database import get_connection
from app.features.products.models.product_details_model import CreateProductDetails


logger = get_logger("product_details.service")


class ProductDetailsService:
    @staticmethod
    def create_product_details(details_data: CreateProductDetails):
        data = details_data.model_dump()

        connection = get_connection()

        try:
            error, success, message = ProductDetailsRepository.create_product_details(
                data, connection
            )

            if error:
                return error, success, message

            connection.commit()

            return None, True, "Detalles creados correctamente"
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_product_brand: %s", e, exc_info=True)
            return "Error al intentar crear los detalles del producto", False, None
        finally:
            connection.close()

    @staticmethod
    def update_product_details(details_data: CreateProductDetails):
        data = details_data.model_dump()

        connection = get_connection()

        try:
            error, success, message = ProductDetailsRepository.update_product_details(
                data, connection
            )

            if error:
                return error, success, message

            connection.commit()

            return None, True, "Detalles actualizados correctamente"
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

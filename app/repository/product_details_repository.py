from app.core.database import get_connection
from app.models.product_details_model import ProductDetails, UpdateProductDetails
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProductDetailsRepository:
    @staticmethod
    def create_product_details(details_data: ProductDetails):
        data = details_data.model_dump()

        connection = get_connection()
        cursor = connection.cursor(buffered=True)

        try:
            cursor.execute(
                """
                INSERT INTO PRODUCT_DETAILS (
                    product_model_id
                ) VALUES (%s)
                """,
                (data["model"],)
            )

            connection.commit()

            product_details_id = cursor.lastrowid

            return None, True, "Detalles del producto creado correctamente", product_details_id
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_products_details: %s",
                         e, exc_info=True)
            return "Error al crear los detalles del producto", False, None, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_product_details(details_data: UpdateProductDetails, cursor):
        data = details_data.model_dump()

        try:
            cursor.execute(
                """
                UPDATE PRODUCT_DETAILS SET
                    product_model_id = %s
                WHERE product_details_id = %s
                """,
                (data["model"], data["product_details_id"])
            )

            return None, True, "Detalles del producto actualizados correctamente"
        except Exception as e:
            logger.error("Error en update_products_details: %s",
                         e, exc_info=True)
            return "Error al actualizar los detalles", False, None

from app.utils.logger import get_logger
from app.features.products.models.product_details_model import CreateProductDetails, UpdateProductDetails

logger = get_logger("product_details.repository")


class ProductDetailsRepository:
    @staticmethod
    def create_product_details(details_data: CreateProductDetails, connection):
        cursor = connection.cursor()

        data = details_data.model_dump()

        try:
            cursor.execute(
                """
                INSERT INTO PRODUCT_DETAILS (
                    product_model_id
                ) VALUES (%s)
                """,
                (data["model"],)
            )

            product_details_id = cursor.lastrowid

            return None, True, "Detalles del producto creado correctamente", product_details_id
        except Exception as e:
            logger.error(
                "Error en create_products_details: %s",
                e,
                exc_info=True
            )
            return "Error al intentar crear los detalles del producto", False, None, None
        finally:
            cursor.close()

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
            logger.error(
                "Error en update_products_details: %s",
                e,
                exc_info=True
            )
            return "Error al actualizar los detalles", False, None
        finally:
            cursor.close()

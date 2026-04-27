from app.core.database import get_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProductModelsRepository:
    @staticmethod
    def find_all_product_models():
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT DISTINCT
                pb.product_brand_id,
                pm.product_model_id,
                pm.product_model_name
            FROM PRODUCT_DETAILS as pd
            INNER JOIN PRODUCT_MODELS as pm
                ON pd.product_model_id = pm.product_model_id
            INNER JOIN PRODUCT_BRANDS as pb
                ON pm.product_brand_id = pb.product_brand_id
            """)

            data = [
                {
                    "brand": item[0],
                    "id": item[1],
                    "model": item[2]
                }
                for item in cursor.fetchall()
            ]

            return None, data
        except Exception as e:
            logger.error("Error en find_all_product_models: %s",
                         e, exc_info=True)
            return "Error al intentar obtener los modelos", None

    @staticmethod
    def create_product_model(model_data):
        data = model_data.model_dump()

        connection = get_connection()
        cursor = connection.cursor(buffered=True)

        try:
            cursor.execute(
                """
                INSERT INTO PRODUCT_MODELS (
                    product_brand_id,
                    product_model_description
                ) VALUES (%s, %s)
                """,
                (data["brand"], data["model"])
            )
            connection.commit()

            return None, True, "Detalles del producto creado correctamente"
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_product_model: %s",
                         e, exc_info=True)
            return "Error al crear el producto", False, None
        finally:
            cursor.close()
            connection.close()

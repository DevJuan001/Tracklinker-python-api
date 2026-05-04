from app.utils.logger import get_logger
from app.core.database import get_connection
from app.features.products.models.product_models_model import CreateProductModel, ProductModel

logger = get_logger("product_models.repository")


class ProductModelsRepository:
    @staticmethod
    def find_all_product_models(connection):
        cursor = connection.cursor()

        try:
            cursor.execute("""
            SELECT DISTINCT
                pb.product_brand_id,
                pm.product_model_id,
                pm.product_model_name
            FROM PRODUCT_MODELS as pm
            LEFT JOIN PRODUCT_DETAILS as pd
                ON pd.product_model_id = pm.product_model_id
            INNER JOIN PRODUCT_BRANDS as pb
                ON pm.product_brand_id = pb.product_brand_id
            """)

            data = [
                ProductModel(
                    brand=item[0],
                    id=item[1],
                    model=item[2]
                )
                for item in cursor.fetchall()
            ]

            return None, data
        except Exception as e:
            logger.error(
                "Error en find_all_product_models: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los modelos", None
        finally:
            cursor.close()

    @staticmethod
    def create_product_model(model_data: CreateProductModel, connection):
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO PRODUCT_MODELS (
                    product_brand_id,
                    product_model_name,
                    product_model_description
                ) VALUES (%s, %s, %s)
                """,
                (
                    model_data["brand_id"],
                    model_data["model"],
                    model_data["description"]
                )
            )

            return None, True, "Modelo creado correctamente"
        except Exception as e:
            logger.error(
                "Error en create_product_model: %s",
                e,
                exc_info=True
            )
            return "Error al intentar crear el modelo", False, None
        finally:
            cursor.close()

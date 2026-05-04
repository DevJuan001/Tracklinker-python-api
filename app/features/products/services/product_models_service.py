from app.core.database import get_connection
from app.features.products.models.product_models_model import CreateProductModel
from app.features.products.repositories.product_models_repository import ProductModelsRepository
from app.utils.logger import get_logger


logger = get_logger("product_models.service")


class ProductModelsService:
    @staticmethod
    def get_all_product_models():
        connection = get_connection()

        try:
            error, models = ProductModelsRepository.find_all_product_models(
                connection
            )

            if error:
                return error, None

            return None, models
        except Exception as e:
            logger.error(
                "Error en find_all_product_models: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los modelos", None
        finally:
            connection.close()

    @staticmethod
    def create_product_model(model_data: CreateProductModel):
        data = model_data.model_dump()

        connection = get_connection()

        try:
            error, success, message = ProductModelsRepository.create_product_model(
                data, connection
            )

            if error:
                return error, False, None

            connection.commit()
            return None, success, message
        except Exception as e:
            connection.rollback()
            logger.error(
                "Error en create_porduct_model: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener crear el modelo", False, None
        finally:
            connection.close()

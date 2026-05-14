

from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.products.models.schemas.product_models_schemas import CreateProductModelSchema
from app.features.products.repositories.product_models_repository import ProductModelsRepository


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
                raise ServiceError(error)

            return None, models

        except ServiceError as e:
            return e.message, None

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
    def create_product_model(model_data: CreateProductModelSchema):
        data = model_data.model_dump()

        connection = get_connection()

        try:
            error, success, message = ProductModelsRepository.create_product_model(
                data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, success, message

        except ServiceError as e:
            return e.message, False, None

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

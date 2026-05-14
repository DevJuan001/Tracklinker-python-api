

from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.products.models.schemas.product_brands_schemas import CreateProductBrandSchema
from app.features.products.repositories.product_brands_repository import ProductBrandsRepository


logger = get_logger("product_brands.service")


class ProductBrandsService:
    @staticmethod
    def get_all_product_brands():
        connection = get_connection()

        try:
            error, brands = ProductBrandsRepository.find_all_product_brands(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, brands

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_product_brands: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las marcas", False, None

        finally:
            connection.close()

    @staticmethod
    def create_product_brand(brand_data: CreateProductBrandSchema):
        data = brand_data.model_dump()

        connection = get_connection()

        try:
            error, success, message = ProductBrandsRepository.create_product_brand(
                data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Marca creada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en create_product_brand: %s", e, exc_info=True)
            return "Error al intentar crear la marca", False, None

        finally:
            connection.close()

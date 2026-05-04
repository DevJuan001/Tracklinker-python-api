from app.features.products.models.product_brand_model import CreateProductBrand
from app.utils.logger import get_logger
from app.core.database import get_connection
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
                return error, None

            return None, brands
        except Exception as e:
            connection.rollback()
            logger.error("Error en get_all_product_brands: %s", e, exc_info=True)
            return "Error al intentar obtener las marcas", False, None
        finally:
            connection.close()


    @staticmethod
    def create_product_brand(brand_data: CreateProductBrand):
        data = brand_data.model_dump()

        connection = get_connection()

        try:
            error, success, message = ProductBrandsRepository.create_product_brand(
                data, connection
            )

            if error:
                return error, success, message

            connection.commit()

            return None, True, "Marca creada correctamente"
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_product_brand: %s", e, exc_info=True)
            return "Error al intentar crear la marca", False, None
        finally:
            connection.close()

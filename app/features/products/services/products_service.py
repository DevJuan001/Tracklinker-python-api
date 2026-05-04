from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.products.repositories.products_repository import ProductsRepository
from app.features.products.repositories.product_details_repository import ProductDetailsRepository
from app.features.products.repositories.product_serials_repository import ProductSerialsRepository
from app.features.products.models.product_model import ProductsFilter, UpdateProduct, CreateProduct
from app.features.products.models.product_serial_model import CreateProductSerial, UpdateProductSerial
from app.features.products.models.product_details_model import CreateProductDetails, UpdateProductDetails

logger = get_logger("products.service")


class ProductsService:
    @staticmethod
    def get_all_products(filters: ProductsFilter):
        connection = get_connection()

        try:
            error, products = ProductsRepository.find_all_products(
                filters, connection
            )
            if error:
                return "Error al intentar obtener los productos", None

            return None, products
        except Exception as e:
            logger.error("Error en get_all_products: %s", e, exc_info=True)
            return "Error al intentar obtener los productos", None
        finally:
            connection.close()

    @staticmethod
    def get_all_products_status():
        connection = get_connection()

        try:
            error, products = ProductsRepository.find_all_product_status(
                connection
            )
            if error:
                return "Error al intentar obtener los estados", None

            return None, products
        except Exception as e:
            logger.error(
                "Error en get_all_products_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los estados", None
        finally:
            connection.close()

    @staticmethod
    def create_product(product_data: CreateProduct):
        data = product_data.model_dump()

        connection = get_connection()

        try:
            error, success, message, product_details_id = ProductDetailsRepository.create_product_details(
                CreateProductDetails(
                    model=data["model"],
                ), connection)

            if error is not None or not success:
                raise ServiceError(error)

            error, success, message, product_id = ProductsRepository.create_product(
                data, product_details_id, connection
            )

            error, success, message = ProductSerialsRepository.create_product_serial(
                CreateProductSerial(
                    serial=data["serial"],
                    product_id=product_id,
                    input_order=data["input_order"],
                    warranty_time=data["warranty_time"]
                ), connection)

            if error is not None or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Producto creado correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en create_product: %s", e, exc_info=True)
            return "Error al intentar crear el producto", False, None
        finally:
            connection.close()

    @staticmethod
    def update_product(product_data: UpdateProduct):
        data = product_data.model_dump(exclude_none=True)

        connection = get_connection()

        try:
            # Verificar que existe el producto
            product = ProductsRepository.find_product_by_id(
                data["id"], connection
            )

            if not product:
                return "Producto no encontrado", False, None

            # Actualizar details si vino brand o model
            if details_fields := {
                key: data[key]
                for key in ["brand", "model"]
                if key in data
            }:
                error, success, message = ProductDetailsRepository.update_product_details(
                    UpdateProductDetails(
                        product_details_id=data["product_details_id"], **details_fields),
                    connection
                )
                if error or not success:
                    raise ServiceError(error)

             # Actualizar serial si vino alguno de estos campos
            if serial_fields := {
                key: data[key]
                for key in ["serial", "input_order", "warranty_time"]
                if key in data
            }:
                error, success, message = ProductSerialsRepository.update_product_serial(
                    UpdateProductSerial(id=data["id"], **serial_fields),
                    connection
                )
                if error or not success:
                    raise ServiceError(error)

            error, success, message = ProductsRepository.update_product(
                data, connection
            )

            connection.commit()
            return error, success, message

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            logger.error("Error en update_product: %s", e, exc_info=True)
            return "Error al intentar actualizar el producto", False, None
        finally:
            connection.close()

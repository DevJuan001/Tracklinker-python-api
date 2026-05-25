
from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.products.repositories.products_repository import ProductsRepository
from app.features.warranties.repositories.warranties_repository import WarrantiesRepository
from app.features.products.repositories.product_serials_repository import ProductSerialsRepository
from app.features.products.repositories.product_details_repository import ProductDetailsRepository
from app.features.products.models.schemas.product_serials_schemas import CreateProductSerialSchema, UpdateProductSerialSchema
from app.features.products.models.entities.product_details_entity import CreateProductDetailsEntity, UpdateProductDetailsEntity
from app.features.products.models.schemas.products_schemas import CreateProductSchema, ProductsFilterSchema, UpdateProductSchema, UpdateProductStatusSchema


logger = get_logger("products.service")


class ProductsService:
    @staticmethod
    def get_all_products(filters: ProductsFilterSchema):
        connection = get_connection()

        try:
            error, products = ProductsRepository.find_all_products(
                filters, connection
            )
            if error:
                raise ServiceError(error)

            return None, products

        except ServiceError as e:
            return e.message, None

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
                raise ServiceError(error)

            return None, products

        except ServiceError as e:
            return e.message, None

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
    def create_product(product_data: CreateProductSchema):
        data = product_data.model_dump()

        connection = get_connection()

        try:
            for serial in data["product_serials"]:
                error, success, message, product_details_id = ProductDetailsRepository.create_product_details(
                    CreateProductDetailsEntity(
                        model_id=data["model_id"],
                    ), connection)

                if error is not None or not success:
                    raise ServiceError(error)

                error, success, message, product_id = ProductsRepository.create_product(
                    data, product_details_id, connection
                )

                if error is not None or not success:
                    raise ServiceError(error)

                error, success, message = ProductSerialsRepository.create_product_serial(
                    CreateProductSerialSchema(
                        product_serial=serial,
                        product_id=product_id,
                        input_order_id=data["input_order_id"],
                        warranty_time=data["warranty_time"]
                    ),
                    connection
                )

                if error is not None or not success:
                    raise ServiceError(error)

                connection.commit()

            return None, True, "Producto creado correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en create_product: %s", e, exc_info=True)
            return "Error al intentar crear el producto", False, None

        finally:
            connection.close()

    @staticmethod
    def update_product(product_data: UpdateProductSchema):
        data = product_data.model_dump(exclude_none=True)

        connection = get_connection()

        try:
            # Verificar que existe el producto
            product = ProductsRepository.find_product_by_id(
                data["id"], connection
            )

            if not product:
                raise ServiceError("Producto no encontrado")

            # Actualizar details si vino brand o model
            if details_fields := {
                key: data[key]
                for key in ["model_id"]
                if key in data
            }:
                error, success, message = ProductDetailsRepository.update_product_details(
                    UpdateProductDetailsEntity(
                        product_details_id=data["product_details_id"], **details_fields
                    ),
                    connection
                )
                if error or not success:
                    raise ServiceError(error)

            # Actualizar serial si vino alguno de estos campos
            if serial_fields := {
                key: data[key]
                for key in ["product_serial", "input_order_id", "warranty_time"]
                if key in data
            }:
                error, success, message = ProductSerialsRepository.update_product_serial(
                    UpdateProductSerialSchema(id=data["id"], **serial_fields),
                    connection
                )
                if error or not success:
                    raise ServiceError(error)

            error, success, message = ProductsRepository.update_product(
                data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Producto actualizado correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en update_product: %s", e, exc_info=True)
            return "Error al intentar actualizar el producto", False, None

        finally:
            connection.close()

    @staticmethod
    def update_product_status(product_data: UpdateProductStatusSchema):
        data = product_data.model_dump()

        connection = get_connection()

        try:

            product = ProductsRepository.find_product_by_id(
                data["product_id"], connection
            )

            if not product:
                return "Producto no encontrado", False, None

            if product[0] == 1 and data["status"] in (3, 4):
                return "No puedes vender o crear una garantía con un producto deshabilitado", False, None

            if data["status"] == 1:
                active_warranty_id = WarrantiesRepository.find_active_warranty_by_serial(
                    data["product_serial"], connection
                )

                if active_warranty_id:
                    raise ServiceError(
                        "No puedes deshabilitar un producto con una garantía vigente"
                    )

            error, success, message = ProductsRepository.update_product_status(
                data["product_id"], data["status"], connection
            )

            if error:
                raise ServiceError(error)

            connection.commit()
            return error, success, message

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error(
                "Error en update_product_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar actualizar el estado producto", False, None

        finally:
            connection.close()

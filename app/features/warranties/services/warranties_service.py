from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.products.repositories.products_repository import ProductsRepository
from app.features.output_orders.models.output_details_model import CreateOutputDetails
from app.features.output_orders.services.output_orders_service import OutputOrdersService
from app.features.warranties.repositories.warranties_repository import WarrantiesRepository
from app.features.warranties.repositories.technicians_repository import TechniciansRepository
from app.features.products.repositories.product_serials_repository import ProductSerialsRepository
from app.features.warranties.models.warranties_model import WarrantyUpdate, WarrantiesFilter, CreateWarranty

logger = get_logger("warranties.service")


class WarrantiesService:

    @staticmethod
    def get_all_warranties(filters: WarrantiesFilter):
        connection = get_connection()

        try:
            error, warranties = WarrantiesRepository.find_all_warranties(
                filters, connection
            )
            if error:
                return "Error al intentar obtener las garantias", None

            return None, warranties
        except Exception as e:
            connection.rollback()
            logger.error("Error en get_all_warranties: %s", e, exc_info=True)
            return "Error al intentar obtener la garantias", None

    @staticmethod
    def get_warranty_by_id(warranty_incidents_id: int):
        connection = get_connection()

        try:
            error, warranty = WarrantiesRepository.find_warranty_by_id(
                warranty_incidents_id, connection
            )
            if error:
                return "Error al intentar obtener la garantía", None

            return None, warranty
        except Exception as e:
            connection.rollback()
            logger.error("Error en get_warranty_by_id: %s", e, exc_info=True)
            return "Error al intentar obtener la garantía", None

    @staticmethod
    def create_warranty(warranty_data: CreateWarranty, user_id: int):
        data = warranty_data.model_dump()

        connection = get_connection()

        try:
            # Verificar que el serial existe
            error, product = ProductSerialsRepository.find_product_by_serial(
                serial=data["product_serial"], connection=connection
            )
            if error or not product:
                raise ServiceError(
                    "Este serial no existe, rectifica que el serial este bien escrito e intentalo nuevamente"
                )

            # Validamos que el producto no este deshabilitado
            if product[1] == 1:
                raise ServiceError(
                    "No puedes crear una garantía con un producto deshabilitado"
                )

            # Verificar que el producto no tenga una garantía activa
            existing = WarrantiesRepository.find_active_warranty_by_serial(
                data["product_serial"], connection
            )

            if existing:
                raise ServiceError("El producto ya tiene una garantía activa")

            # Crear la orden de salida del producto
            error, success, message = OutputOrdersService.create_output_order(
                CreateOutputDetails(
                    product_serial=data["product_serial"],
                    out_product_garanty="2040-01-01",
                    product_transformation="No necesita",
                )
            )
            if error:
                raise ServiceError(error)

            # Actualizar estado del producto y lo ponemos en garantía
            error, success, message = ProductsRepository.update_product_status(
                product[0], 4, connection
            )
            if error:
                raise ServiceError(error)

            error, success, message = WarrantiesRepository.create_warranty(
                data, user_id, connection
            )
            if error:
                raise ServiceError(error)

            connection.commit()

            return None, success, message

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en create_warranty: %s", e, exc_info=True)
            return "Error al intentar crear la garantía", False, None
        finally:
            connection.close()

    @staticmethod
    def update_warranty(warranty_incidents_id: int, user_id: int, warranty_data: WarrantyUpdate):
        data = warranty_data.model_dump(exclude_none=True)
        connection = get_connection()

        WARRANTY_STATUS_PRODUCT_MAP = {
            1: 2,
            2: 4,
            3: 4,
            4: 2,
        }

        try:
            # Buscamos si existe la garantía
            warranty = WarrantiesRepository.find_warranty_by_id(
                warranty_incidents_id, connection
            )
            if not warranty:
                return "Garantía no encontrada", False, None

            if not data:
                return "No hay campos para actualizar", False, None

            new_status = data.get("status")
            current_status = warranty["warranty_status"]

            if new_status == 3 and current_status == 2:
                error, success, message = TechniciansRepository.assign_technician(
                    warranty_incidents_id, user_id, connection
                )
                if error:
                    raise ServiceError(error)

            elif new_status == 1 and current_status in (2, 3, 4):
                error, success, message = TechniciansRepository.unassign_technician(
                    warranty_incidents_id, connection
                )
                if error:
                    raise ServiceError(error)

            if new_status in WARRANTY_STATUS_PRODUCT_MAP:
                product_serial = data.get("product_serial")

                if not product_serial:
                    raise ServiceError(
                        "Serial requerido para cambiarle el estado"
                    )

                product_id = ProductSerialsRepository.find_product_id_by_serial(
                    product_serial, connection
                )

                if not product_id:
                    raise ServiceError("Serial no encontrado")

                new_product_status = WARRANTY_STATUS_PRODUCT_MAP[new_status]
                error, success, message = ProductsRepository.update_product_status(
                    product_id, new_product_status, connection
                )

                if error:
                    raise ServiceError(error)

            error, success, message = WarrantiesRepository.update_warranty(
                warranty_incidents_id=warranty_incidents_id, warranty_data=data, connection=connection
            )
            if error:
                raise ServiceError(error)

            connection.commit()
            return None, success, message

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en update_warranty: %s", e, exc_info=True)
            return "Error al intentar actualizar la garantía", False, None
        finally:
            connection.close()

from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.products.repositories.products_repository import ProductsRepository
from app.features.output_orders.models.output_details_model import CreateOutputDetails
from app.features.warranties.repositories.warranties_repository import WarrantiesRepository
from app.features.warranties.repositories.technicians_repository import TechniciansRepository
from app.features.products.repositories.product_serials_repository import ProductSerialsRepository
from app.features.output_orders.repositories.output_orders_repository import OutputOrdersRepository
from app.features.output_orders.repositories.output_details_repository import OutputDetailsRepository
from app.features.warranties.models.warranties_schemas import CreateWarrantySchema, UpdateWarrantySchema, WarrantiesFilterSchema

logger = get_logger("warranties.service")


class WarrantiesService:

    @staticmethod
    def get_all_warranties(filters: WarrantiesFilterSchema):
        connection = get_connection()

        try:
            error, warranties = WarrantiesRepository.find_all_warranties(
                filters, connection
            )

            if error:
                raise ServiceError(error)

            return None, warranties

        except ServiceError as e:
            return e.message, None

        except Exception as e:
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
                raise ServiceError(error)

            return None, warranty

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_warranty_by_id: %s", e, exc_info=True)
            return "Error al intentar obtener la garantía mediante el id", None

    @staticmethod
    def create_warranty(warranty_data: CreateWarrantySchema, user_id: int):
        data = warranty_data.model_dump()

        connection = get_connection()

        try:
            # Verificamos que el serial esta registrado
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
                    "No puedes crear una garantía con un producto deshabilitado, activa o habilita este producto e intentalo nuevamente"
                )

            # Verificamos que el producto no tenga una garantía activa
            existing = WarrantiesRepository.find_active_warranty_by_serial(
                data["product_serial"], connection
            )

            if existing:
                raise ServiceError(
                    "El producto ya cuenta con una garantía activa, debes completar o deshabilitar esa garantía  e intentarlo nuevamente"
                )

            # Creamos la orden de salida del producto
            error, success, output_order_id = OutputOrdersRepository.create_output_order(
                connection
            )

            if error or not success:
                raise ServiceError(error)

            # Creamos los detalles de la orden de salida
            error, success, message = OutputDetailsRepository.create_output_details(
                output_order_id,
                CreateOutputDetails(
                    product_serial=data["product_serial"],
                    output_product_garanty=data["output_product_garanty"],
                ),
                connection
            )

            if error or not success:
                raise ServiceError(
                    error or "Error al intentar crear los detalles de la orden de salida"
                )

            # Actualizamos el estado del producto y lo ponemos en garantía
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
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en create_warranty: %s", e, exc_info=True)
            return "Error al intentar crear la garantía", False, None

        finally:
            connection.close()

    @staticmethod
    def update_warranty(warranty_incidents_id: int, user_id: int, warranty_data: UpdateWarrantySchema):
        data = warranty_data.model_dump(exclude_none=True)

        connection = get_connection()

        WARRANTY_STATUS_PRODUCT_MAP = {
            1: 2,
            2: 4,
            3: 4,
            4: 2,
        }

        try:
            # Verificamos que el serial existe
            if "product_serial" in data:
                error, product = ProductSerialsRepository.find_product_by_serial(
                    data["product_serial"],
                    connection
                )
                if error or not product:
                    raise ServiceError(error)

            # Validamos que exista esa garantía
            warranty = WarrantiesRepository.find_warranty_by_id(
                warranty_incidents_id, connection
            )

            if not warranty:
                raise ServiceError("Garantía no encontrada")

            if not data:
                raise ServiceError("No hay campos para actualizar")

            # Obtenemos el nuevo estado que se le va a asignar a la garantía
            new_status = data.get("status")

            # Obtenemos el estado actual de la garantía
            current_status = warranty[1]

            # Aqui verificamos si el estado actual es 1 = "Deshabilitada" y el nuevo está entre
            # 3 = "En proceso" o 4 = "Completada"
            if current_status == 1 and new_status in (3, 4):
                # Asignamos esa garantía al técnico que le dio empezar
                error, success, message = TechniciansRepository.assign_technician(
                    warranty_incidents_id, user_id, connection
                )

                if error:
                    raise ServiceError(error)

            # Aqui Verificamos si el estado actual es 2 = "Pendiente o sin empezar" y el nuevo estado es igual a 3 = "En proceso"
            if current_status == 2 and new_status == 3:

                # Asignamos esa garantía al técnico que le dio empezar
                error, success, message = TechniciansRepository.assign_technician(
                    warranty_incidents_id, user_id, connection
                )

                if error:
                    raise ServiceError(error)

            # Aqui validamos que si el nuevo estado es 1 = "Deshabilitada" y el estado actual está entre
            # 2 = "Pendiente o sin comenzar", 3 = "En proceso" o 4 = "Completada"
            if new_status == 1 and current_status in (2, 3, 4):
                # Desasignamos esa garantía al tecnico que la empezo
                error, success, message = TechniciansRepository.unassign_technician(
                    warranty_incidents_id,
                    connection
                )

                if error:
                    raise ServiceError(error)

            if new_status in WARRANTY_STATUS_PRODUCT_MAP:
                product_serial = data.get("product_serial")

                if not product_serial:
                    raise ServiceError(
                        "Serial requerido para cambiarle el estado"
                    )

                # Verificamos que el serial este registrado
                error, product = ProductSerialsRepository.find_product_by_serial(
                    product_serial,
                    connection
                )

                if not product:
                    raise ServiceError("Serial no encontrado")

                # Aqui usamos el objeto con el cual mapeamos cual sera el nuevo estado del producto
                new_product_status = WARRANTY_STATUS_PRODUCT_MAP[new_status]

                # Actualizamos el estado del producto
                error, success, message = ProductsRepository.update_product_status(
                    product[0],
                    new_product_status,
                    connection
                )

                if error or not success:
                    raise ServiceError(error)

            # Actualizamos la información de la garantía
            error, success, message = WarrantiesRepository.update_warranty(
                warranty_incidents_id=warranty_incidents_id,
                warranty_data=data,
                connection=connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, success, message

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en update_warranty: %s", e, exc_info=True)
            return "Error al intentar actualizar la garantía", False, None

        finally:
            connection.close()


from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.suppliers.repositories.suppliers_repository import SuppliersRepository
from app.features.suppliers.models.suppliers_schema import CreateSupplierSchema, FilterSuppliersSchema, UpdateSupplierSchema


logger = get_logger("suppliers.service")


class SuppliersService():

    @staticmethod
    def get_all_suppliers(filters: FilterSuppliersSchema):
        connection = get_connection()

        try:
            error, suppliers = SuppliersRepository.find_all_suppliers(
                filters, connection
            )

            if error:
                raise ServiceError(error)

            return None, suppliers

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_all_suppliers: %s", e, exc_info=True)
            return "Error al intentar obtener los proveedores", None

        finally:
            connection.close()

    @staticmethod
    def get_supplier_by_id(supplier_id: int):
        connection = get_connection()

        try:
            error, supplier = SuppliersRepository.find_supplier_by_id(
                supplier_id, connection
            )

            if error:
                raise ServiceError(error)

            return None, supplier

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_supplier_by_id: %s", e, exc_info=True)
            return "Error al intentar obtener el proveedor mediante el id", None

        finally:
            connection.close()

    @staticmethod
    def create_supplier(supplier_data: CreateSupplierSchema):
        data = supplier_data.model_dump()

        connection = get_connection()

        try:
            error, supplier, = SuppliersRepository.find_supplier_by_name(
                data["name"], connection
            )

            if error:
                raise ServiceError(error)

            if supplier:
                raise ServiceError(
                    "Ya existe un proveedor con este nombre, cambia el valor del campo e intentalo nuevamente"
                )

            error, success, message = SuppliersRepository.create_supplier(
                supplier_data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Proveedor creado correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en create_supplier: %s", e, exc_info=True)
            return "Error al intentar crear el proveedor", False, None

        finally:
            connection.close()

    @staticmethod
    def update_supplier(supplier_id: int, supplier_data: UpdateSupplierSchema):
        data = supplier_data.model_dump()

        connection = get_connection()

        try:
            error, supplier, = SuppliersRepository.find_supplier_by_name(
                data["name"], connection
            )

            if error:
                raise ServiceError(error)

            if supplier:
                raise ServiceError(
                    "Ya existe un proveedor con este nombre, cambia el valor del campo e intentalo nuevamente"
                )

            error, success, message = SuppliersRepository.update_supplier(
                supplier_id, supplier_data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Proveedor actualizado correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en update_supplier: %s", e, exc_info=True)
            return "Error al intentar actualizar el proveedor", False, None

        finally:
            connection.close()

    @staticmethod
    def disable_supplier(supplier_id: int):
        connection = get_connection()

        try:
            # Verificar que si existe ese proveedor
            error, supplier = SuppliersRepository.find_supplier_by_id(
                supplier_id, connection
            )

            if error:
                raise ServiceError(error)

            if not supplier:
                raise ServiceError("Este proveedor no existe")

            error, success, message = SuppliersRepository.disable_supplier(
                supplier_id, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Proveedor deshabilitado correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en disable_supplier: %s", e, exc_info=True)
            return "Error al intentar deshabilitar el proveedor", False, None

        finally:
            connection.close()

    @staticmethod
    def enable_supplier(supplier_id: int):
        connection = get_connection()

        try:
            # Verificar que si existe ese proveedor
            error, supplier = SuppliersRepository.find_supplier_by_id(
                supplier_id, connection
            )

            if error:
                raise ServiceError(error)

            if not supplier:
                raise ServiceError("Este proveedor no existe")

            error, success, message = SuppliersRepository.enable_supplier(
                supplier_id, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Proveedor habilitado correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en enable_supplier: %s", e, exc_info=True)
            return "Error al intentar habilitar el proveedor", False, None

        finally:
            connection.close()

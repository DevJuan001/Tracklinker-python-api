

from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.dashboard.repositories.dashboard_repository import DashboardRepository
from app.utils.logger import get_logger


logger = get_logger("dashboard.service")


class DashboardService:
    @staticmethod
    def get_all_and_new_products_ammount():
        connection = get_connection()

        try:
            error, data = DashboardRepository.find_all_and_new_products_ammount(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_and_new_products_ammount: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener la cantidad de productos actual", None
        finally:
            connection.close()

    @staticmethod
    def get_all_monthly_supplier_inputs():
        connection = get_connection()

        try:
            error, data = DashboardRepository.find_all_suppliers_inputs(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_monthly_supplier_inputs: %s",
                e,
                exc_info=True

            )
            return "Error al intentar obtener las ordenes de entrada mensuales por proveedor", None
        
        finally:
            connection.close()

    @staticmethod
    def get_all_outputs_by_month():
        connection = get_connection()

        try:
            error, data = DashboardRepository.find_all_outputs_by_month(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_outputs: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las salida", None
        finally:
            connection.close()

    @staticmethod
    def get_all_warranties_group_by_status():
        connection = get_connection()

        try:
            error, data = DashboardRepository.find_all_warranties_group_by_status(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_warranties_by_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las garantias agrupadas por los estados", None
        finally:
            connection.close()

    @staticmethod
    def get_all_and_new_users():
        connection = get_connection()

        try:
            error, data = DashboardRepository.find_all_and_new_users(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_and_new_users: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los usuarios nuevos y totales", None
        finally:
            connection.close()

    @staticmethod
    def get_stock_by_brand():
        connection = get_connection()

        try:
            error, data = DashboardRepository.find_stock_by_brand(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_stock_by_brand: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener la cantidad de productos por marca", None
        finally:
            connection.close()

    @staticmethod
    def get_output_orders_amount():
        connection = get_connection()

        try:
            error, data = DashboardRepository.find_output_orders_amount(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_output_orders_amount(: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener la cantidad de ordenes de salida", None
        finally:
            connection.close()

    @staticmethod
    def get_categories_amount():
        connection = get_connection()

        try:
            error, data = DashboardRepository.find_categories_amount(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_categories_amount: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener la cantidad de categorias", None
        finally:
            connection.close()

    @staticmethod
    def get_subcategories_with_stock():
        connection = get_connection()

        try:
            error, data = DashboardRepository.find_subcategories_with_stock(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_subcategories_with_stock: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener la subcategorias con el stock", None
        finally:
            connection.close()

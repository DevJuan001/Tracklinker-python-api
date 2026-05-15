from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.users.repositories.users_repository import UsersRepository
from app.features.products.repositories.products_repository import ProductsRepository
from app.features.suppliers.repositories.suppliers_repository import SuppliersRepository
from app.features.categories.repositories.categories_repository import CategoriesRepository
from app.features.warranties.repositories.warranties_repository import WarrantiesRepository
from app.features.output_orders.repositories.output_orders_repository import OutputOrdersRepository
from app.features.subcategories.repositories.subcategories_repository import SubcategoriesRepository

logger = get_logger("reports.service")


class ReportsService:

    #   ------------ REPORTES DE USUARIOS ------------
    @staticmethod
    def get_recent_users():
        connection = get_connection()

        try:
            error, users = UsersRepository.find_recent_users(connection)

            if error:
                raise ServiceError(error)

            return None, users

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_recent_users: %s", e, exc_info=True)
            return "Error al intentar obtener los usuarios recientes", None

        finally:
            connection.close()

    @staticmethod
    def get_users_by_rol(period: str):
        connection = get_connection()

        try:
            error, users = UsersRepository.find_users_by_rol(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, users

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_users_by_rol: %s", e, exc_info=True)
            return "Error al intentar obtener los usuarios por rol", None

        finally:
            connection.close()

    @staticmethod
    def get_users_growth(period: str):
        connection = get_connection()

        try:
            error, data = UsersRepository.find_users_growth(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_users_growth: %s", e, exc_info=True)
            return "Error al intentar obtener el crecimiento de usuarios", None

        finally:
            connection.close()

    @staticmethod
    def get_users_by_status():
        connection = get_connection()

        try:
            error, data = UsersRepository.find_users_by_status(connection)

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_users_by_status: %s", e, exc_info=True)
            return "Error al intentar obtener los usuarios agrupados por estado", None

        finally:
            connection.close()

#   ------------ REPORTES DE PRODUCTOS ------------
    @staticmethod
    def get_recent_products():
        connection = get_connection()

        try:
            error, products = ProductsRepository.find_recent_products(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, products

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_recent_products: %s", e, exc_info=True)
            return "Error al intentar obtener los productos agregados recientemente", None

        finally:
            connection.close()

    @staticmethod
    def get_products_growth(period: str):
        connection = get_connection()

        try:
            error, data = ProductsRepository.find_products_growth(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_products_growth: %s", e, exc_info=True)
            return "Error al intentar obtener el crecimiento de los productos", None

        finally:
            connection.close()

    @staticmethod
    def get_products_by_brand(period: str):
        connection = get_connection()

        try:
            error, data = ProductsRepository.find_products_by_brand(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_products_by_brand: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los productos agrupados por marca", None

        finally:
            connection.close()

    @staticmethod
    def get_products_by_status():
        connection = get_connection()

        try:
            error, data = ProductsRepository.find_products_by_status(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_products_by_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los productos agrupados por estado", None

        finally:
            connection.close()


#   ------------ REPORTES DE CATEGORIAS ------------

    @staticmethod
    def get_recent_categories():
        connection = get_connection()

        try:
            error, categories = CategoriesRepository.find_recent_categories(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, categories

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_products_by_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las categorias agregadas recientemente", None

        finally:
            connection.close()

    @staticmethod
    def get_categories_growth(period: str):
        connection = get_connection()

        try:
            error, data = CategoriesRepository.find_categories_growth(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_categories_growth: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el crecimiento de categorias", None

        finally:
            connection.close()

    @staticmethod
    def get_categories_by_brand(period: str):
        connection = get_connection()

        try:
            error, data = CategoriesRepository.find_categories_by_brand(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_categories_growth: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el crecimiento de categorias", None

        finally:
            connection.close()

    @staticmethod
    def get_categories_by_status():
        connection = get_connection()

        try:
            error, data = CategoriesRepository.find_categories_by_status(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_categories_growth: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el crecimiento de categorias", None

        finally:
            connection.close()

#   ------------ REPORTES DE SUBCATEGORIAS ------------

    @staticmethod
    def get_recent_subcategories():
        connection = get_connection()

        try:
            error, subcategories = SubcategoriesRepository.find_recent_subcategories(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, subcategories

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_recent_subcategories: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las subcategorias agregadas recientemente", None

        finally:
            connection.close()

    @staticmethod
    def get_subcategories_growth(period: str):
        connection = get_connection()

        try:
            error, data = SubcategoriesRepository.find_subcategories_growth(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_subcategories_growth: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el crecimiento de las subcategorias", None

        finally:
            connection.close()

    @staticmethod
    def get_subcategories_by_category(period: str):
        connection = get_connection()

        try:
            error, data = SubcategoriesRepository.find_subcategories_by_category(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_subcategories_by_category: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las subcategorias agrupadas con categorias", None

        finally:
            connection.close()

    @staticmethod
    def get_subcategories_by_status():
        connection = get_connection()

        try:
            error, data = SubcategoriesRepository.find_subcategories_by_status(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_subcategories_by_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las subcategorias agrupadas por estado", None

        finally:
            connection.close()

#   ------------ REPORTES DE GARANTÍAS ------------
    @staticmethod
    def get_recent_warranties():
        connection = get_connection()

        try:
            error, warranties = WarrantiesRepository.find_recent_warranties(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, warranties

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_recent_warranties: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las garantias agregadas recientemente", None

        finally:
            connection.close()

    @staticmethod
    def get_warranties_growth(period: str):
        connection = get_connection()

        try:
            error, data = WarrantiesRepository.find_warranties_growth(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_warranties_growth: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el crecimiento de garantías", None

        finally:
            connection.close()

    @staticmethod
    def get_warranties_by_brand(period: str):
        connection = get_connection()

        try:
            error, data = WarrantiesRepository.find_warranties_by_brand(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_warranties_by_brand: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las garantías agrupadas por marcas", None

        finally:
            connection.close()

    @staticmethod
    def get_warranties_by_status():
        connection = get_connection()

        try:
            error, data = WarrantiesRepository.find_warranties_by_status(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_warranties_by_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las garantías agrupadas por estado", None

        finally:
            connection.close()

#   ------------ REPORTES DE PROVEEDORES ------------
    @staticmethod
    def get_recent_suppliers():
        connection = get_connection()

        try:
            error, suppliers = SuppliersRepository.find_recent_suppliers(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, suppliers

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_recent_suppliers: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los proveedores agregados recientemente", None

        finally:
            connection.close()

    @staticmethod
    def get_suppliers_growth(period: str):
        connection = get_connection()

        try:
            error, data = SuppliersRepository.find_suppliers_growth(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_suppliers_growth: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el crecimiento de proveedores", None

        finally:
            connection.close()

    @staticmethod
    def get_suppliers_by_brand(period: str):
        connection = get_connection()

        try:
            error, data = SuppliersRepository.find_suppliers_by_brand(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_suppliers_by_brand: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los proveedores agrupados por marcas", None

        finally:
            connection.close()

    @staticmethod
    def get_suppliers_by_status():
        connection = get_connection()

        try:
            error, data = SuppliersRepository.find_suppliers_by_status(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_suppliers_by_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los proveedores agrupados por estado", None

        finally:
            connection.close()


#   ------------ REPORTES DE ORDENES DE SALIDA ------------


    @staticmethod
    def get_recent_outputs():
        connection = get_connection()

        try:
            error, outputs = OutputOrdersRepository.find_recent_outputs(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, outputs

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_recent_output: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las ordenes de salida creadas recientemente", None

        finally:
            connection.close()

    @staticmethod
    def get_outputs_growth(period: str):
        connection = get_connection()

        try:
            error, data = OutputOrdersRepository.find_outputs_growth(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_outputs_growth: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el crecimiento de las ordenes de salida", None

        finally:
            connection.close()

    @staticmethod
    def get_outputs_by_brand(period: str):
        connection = get_connection()

        try:
            error, data = OutputOrdersRepository.find_outputs_by_brand(
                period, connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_outputs_by_brand: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las ordenes de salida agrupadas por marcas", None

        finally:
            connection.close()

    @staticmethod
    def get_outputs_by_status():
        connection = get_connection()

        try:
            error, data = OutputOrdersRepository.find_outputs_by_status(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, data

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_outputs_by_status: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las ordenes de salida agrupadas por estado", None

        finally:
            connection.close()

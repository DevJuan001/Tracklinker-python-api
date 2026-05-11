from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.subcategories.models.subcategories_schemas import CreateSubcategorySchema, SubcategoriesFiltersSchema, UpdateSubcategorySchema
from app.features.subcategories.repositories.subcategories_repository import SubcategoriesRepository
from app.utils.logger import get_logger

logger = get_logger("subcategories.service")


class SubcategoriesService:

    @staticmethod
    def get_all_subcategories(filters: SubcategoriesFiltersSchema):
        connection = get_connection()

        try:
            error, subcategories = SubcategoriesRepository.find_all_subcategories(
                filters, connection
            )

            if error:
                raise ServiceError(error)

            return None, subcategories

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_subcategories: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las subcategorias", None

    @staticmethod
    def get_subcategory_by_id(subcategory_id: int):
        connection = get_connection()

        try:
            error, subcategory = SubcategoriesRepository.find_subcategory_by_id(
                subcategory_id, connection
            )

            if error:
                raise ServiceError(error)

            return None, subcategory

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_subcategory_by_id: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las subcategorias", None

    @staticmethod
    def get_active_categories():
        connection = get_connection()

        try:
            error, categories = SubcategoriesRepository.find_active_categories(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, categories

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_active_categories: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las subcategorias", None

    @staticmethod
    def create_subcategory(subcategory_data: CreateSubcategorySchema):
        connection = get_connection()

        try:
            error, success, message = SubcategoriesRepository.create_subcategory(
                subcategory_data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Subcategoria creada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            logger.error(
                "Error en create_subcategory: %s",
                e,
                exc_info=True
            )
            return "Error al intentar crear la subcategoria", False, None

    @staticmethod
    def update_subcategory(subcategory_id: int, subcategory_data: UpdateSubcategorySchema):
        connection = get_connection()

        try:
            error, success, message = SubcategoriesRepository.update_subcategory(
                subcategory_id, subcategory_data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Subcategoria actualizada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            logger.error(
                "Error en update_subcategory: %s",
                e,
                exc_info=True
            )
            return "Error al intentar actualizar la subcategoria", False, None

    @staticmethod
    def disable_subcategory(subcategory_id: int):
        connection = get_connection()

        try:
            error, success, message = SubcategoriesRepository.disable_subcategory(
                subcategory_id, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Subcategoria deshabilitada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            logger.error(
                "Error en disable_subcategory: %s",
                e,
                exc_info=True
            )
            return "Error al intentar deshabilitar la subcategoria", False, None

    @staticmethod
    def enable_subcategory(subcategory_id: int):
        connection = get_connection()

        try:
            error, success, message = SubcategoriesRepository.enable_subcategory(
                subcategory_id, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Subcategoria habilitada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            logger.error(
                "Error en  enable_subcategory: %s",
                e,
                exc_info=True
            )
            return "Error al intentar habilitar la subcategoria", False, None

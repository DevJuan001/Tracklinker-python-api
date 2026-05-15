from app.core.exception import ServiceError
from app.utils.logger import get_logger
from app.core.database import get_connection
from app.features.categories.models.categories_schemas import CategoriesFiltersSchema, CreateCategorySchema, UpdateCategorySchema
from app.features.categories.repositories.categories_repository import CategoriesRepository


logger = get_logger("categories.service")


class CategoriesService:
    @staticmethod
    def get_all_categories(filters: CategoriesFiltersSchema):
        connection = get_connection()

        try:
            error, categories = CategoriesRepository.find_all_categories(
                filters, connection
            )

            if error:
                raise ServiceError(error)

            return None, categories

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_all_categories: %s", e, exc_info=True)
            return "Error al intentar obtener las categorias", None

        finally:
            connection.close()

    @staticmethod
    def get_category_by_id(category_id: int):
        connection = get_connection()

        try:
            error, category = CategoriesRepository.find_category_by_id(
                category_id, connection
            )

            if error:
                raise ServiceError(error)

            return None, category

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error("Error en get_category_by_id %s", e, exc_info=True)
            return "Error al intentar obtener la categoría", None

        finally:
            connection.close()

    @staticmethod
    def create_category(category_data: CreateCategorySchema):
        data = category_data.model_dump()

        connection = get_connection()

        try:
            # Verificar si existe una categoría con ese nombre
            if "name" in data:
                error, existing_category = CategoriesRepository.find_category_by_name(
                    data["name"], connection
                )

                if error:
                    raise ServiceError(error)

                if existing_category:
                    raise ServiceError(
                        "Ya existe una categoría con este nombre, usa otro nombre e intenta crearla nuevamente"
                    )

            error, success, message = CategoriesRepository.create_category(
                category_data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Categoria creada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en create_category %s", e, exc_info=True)
            return "Error al intentar crear la categoría", False, None

        finally:
            connection.close()

    @staticmethod
    def update_category(category_id: int, category_data: UpdateCategorySchema):
        connection = get_connection()

        try:
            # Verificar si existe la categoría
            error, category = CategoriesRepository.find_category_by_id(
                category_id, connection
            )

            if error:
                raise ServiceError(error)

            if not category:
                raise ServiceError("Categoria no encontrada")

            error, success, message = CategoriesRepository.update_category(
                category_id, category_data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Categoria actualizada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en update_category %s", e, exc_info=True)
            return "Error al intentar actualizar la categoría", False, None

        finally:
            connection.close()

    @staticmethod
    def disable_category(category_id: int):
        connection = get_connection()

        try:
            # Verificar si existe la categoría
            error, category = CategoriesRepository.find_category_by_id(
                category_id, connection
            )

            if error:
                raise ServiceError(error)

            if not category:
                raise ServiceError("Categoria no encontrada")

            error, success, message = CategoriesRepository.disable_category(
                category_id, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Categoria deshabilitada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en disable_category %s", e, exc_info=True)
            return "Error al intentar deshabilitar la categoría", False, None

        finally:
            connection.close()

    @staticmethod
    def enable_category(category_id: int):
        connection = get_connection()

        try:
            # Verificar si existe la categoría
            error, category = CategoriesRepository.find_category_by_id(
                category_id, connection
            )

            if error:
                raise ServiceError(error)

            if not category:
                raise ServiceError("Categoria no encontrada")

            error, success, message = CategoriesRepository.enable_category(
                category_id, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Categoria habilitada correctamente"

        except ServiceError as e:
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error("Error en enable_category %s", e, exc_info=True)
            return "Error al intentar habilitar la categoría", False, None

        finally:
            connection.close()

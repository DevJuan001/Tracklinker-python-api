from app.utils.logger import get_logger
from app.core.database import get_connection
from app.features.categories.repositories.categories_repository import CategoriesRepository
from app.features.categories.models.categories_model import CategoriesFilters, CreateCategory, UpdateCategory


logger = get_logger("categories.service")


class CategoriesService:
    @staticmethod
    def get_all_categories(filters: CategoriesFilters):
        connection = get_connection()

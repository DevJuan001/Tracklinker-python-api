from pydantic import BaseModel

from app.utils.base_schema import BaseSchema


class SubcategoryResponse(BaseModel):
    category_id: int
    category_name: str
    subcategory_id: int
    subcategory_name: str
    subcategory_date: str
    subcategory_status: int


class ActiveCategoryResponse(BaseModel):
    category_id: int
    category_name: str


class RecentSubcategoryResponse(BaseSchema):
    name: str
    category: str
    date: str
    status: int


class SubcategoriesByCategoryResponse(BaseModel):
    category: str
    subcategories: int


class SubcategoriesByStatusResponse(BaseModel):
    recent_subcategories: int
    total_subcategories: int
    inactive_subcategories: int
    active_subcategories: int


class SubcategoriesGrowthResponse(BaseSchema):
    date: str
    subcategories: int


class SubcategoryByName(BaseModel):
    id: int

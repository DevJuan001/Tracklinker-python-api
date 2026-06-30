from pydantic import BaseModel

from app.utils.base_schema import BaseSchema


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    date: str
    status: int


class RecentCategoryResponse(BaseModel):
    name: str
    date: str
    description: str
    status: int


class ActiveCategoryResponse(BaseModel):
    category_id: int
    category_name: str


class CategoryByStatusResponse(BaseModel):
    recent_categories: int
    total_categories: int
    inactive_categories: int
    active_categories: int


class GrowthCategoryResponse(BaseSchema):
    date: str
    categories: int

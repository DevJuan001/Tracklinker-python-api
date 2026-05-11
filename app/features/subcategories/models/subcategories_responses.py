from pydantic import BaseModel


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
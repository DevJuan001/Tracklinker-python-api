from fastapi import APIRouter, Depends
from app.middlewares.roles_middleware import require_roles
from app.controllers.category_controller import CategoryController
from app.models.category_model import CategoryCreate, CategoryUpdate

router = APIRouter(
    prefix="/api/categories",
    tags=["Categorías"]
)

@router.get("/")
def get_all_categories(
    name_order: str = None,
    start_date: str = None,
    end_date: str = None,
    status: int = None,
):
    return CategoryController.get_all_categories(
        name_order,
        start_date,
        end_date,
        status,
    )

@router.get("/{category_id}")
def get_category_by_id(category_id: int):
    return CategoryController.get_category_by_id(category_id)

@router.post("/create")
def create_category(category_data: CategoryCreate):
    return CategoryController.create_category(category_data)

@router.put("/update/{category_id}")
def update_category(category_id: int, category_data: CategoryUpdate):
    return CategoryController.update_category(category_id, category_data)

@router.put("/disable/{category_id}")
def disable_category(category_id: int):
    return CategoryController.disable_category(category_id)

@router.put("/enable/{category_id}")
def enable_category(category_id: int):
    return CategoryController.enable_category(category_id)
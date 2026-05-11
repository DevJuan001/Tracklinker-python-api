from pydantic import BaseModel


class ProductsAmountResponse(BaseModel):
    products: int
    new_products: int


class SupplierInputResponse(BaseModel):
    supplier_name: str
    orders: int


class OutputByMonthResponse(BaseModel):
    month: str
    output_orders: int


class WarrantyByStatusResponse(BaseModel):
    status: int
    total: int


class UsersAmountResponse(BaseModel):
    users: int
    new_users: int


class StockByBrandResponse(BaseModel):
    brand: str
    products: int


class OutputOrdersAmountResponse(BaseModel):
    orders: int
    new_orders: int


class CategoriesAmountResponse(BaseModel):
    categories: int
    new_categories: int


class SubcategoryStockResponse(BaseModel):
    subcategory: str
    stock: int

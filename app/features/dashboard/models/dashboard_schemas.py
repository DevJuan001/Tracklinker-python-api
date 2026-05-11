from pydantic import BaseModel


class ProductsAmountSchema(BaseModel):
    products: int
    new_products: int


class SupplierInputSchema(BaseModel):
    supplier_name: str
    orders: int


class OutputByMonthSchema(BaseModel):
    month: str
    output_orders: int


class WarrantyByStatusSchema(BaseModel):
    status: str
    total: int


class UsersAmountSchema(BaseModel):
    users: int
    new_users: int


class StockByBrandSchema(BaseModel):
    brand: str
    products: int


class OutputOrdersAmountSchema(BaseModel):
    orders: int
    new_orders: int


class CategoriesAmountSchema(BaseModel):
    categories: int
    new_categories: int


class SubcategoryStockSchema(BaseModel):
    subcategory: str
    stock: int

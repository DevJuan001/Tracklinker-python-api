from app.core.database import get_connection
from app.models.product_brand_model import ProductBrand
from app.models.product_brand_model import ProductBrand
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProductBrandsRepository:
    @staticmethod
    def find_all_product_brands():
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            GROUP_CONCAT(DISTINCT p.subcategory_id) as subcategories,
            pb.product_brand_id,
            pb.product_brand_name
        FROM PRODUCT_BRANDS as pb
        INNER JOIN PRODUCT_MODELS as pm
            ON pb.product_brand_id = pm.product_brand_id  
        INNER JOIN PRODUCT_DETAILS as pd 
            ON pm.product_model_id = pd.product_model_id
        INNER JOIN PRODUCTS as p
            ON pd.product_details_id = p.product_details_id
        GROUP BY pb.product_brand_id, pb.product_brand_name
        ORDER BY pb.product_brand_name ASC
        """

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            data = [
                {
                    "subcategories": item[0],
                    "id": item[1],
                    "name": item[2]
                }
                for item in result
            ]
            return None, data
        except Exception as e:
            logger.error("Error en find_all_product_brands: %s",
                         e, exc_info=True)
            return "Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create_product_brand(brand_data: ProductBrand):
        data = brand_data.model_dump()
        connection = get_connection()
        cursor = connection.cursor(buffered=True)
        try:
            cursor.execute(
                "SELECT product_brand_id FROM PRODUCT_BRANDS WHERE product_brand_name = %s",
                (data["product_brand_name"],)
            )

            exist_model = cursor.fetchone()

            if exist_model:
                cursor.close()
                connection.close()
                return f"Esta marca ya esta registrada", False, None

            cursor.execute("INSERT INTO PRODUCT_BRANDS (product_brand_name) VALUES (%s)",
                           (data["product_brand_name"],))
            connection.commit()

            return None, True, f"Marca creada correctamente"
        except Exception as e:
            logger.error("Error en find_all_product_brands: %s",
                         e, exc_info=True)
            return "Error al crear la marca", False, None

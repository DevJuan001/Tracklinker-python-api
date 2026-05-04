from app.utils.logger import get_logger
from app.features.products.models.product_brand_model import ProductBrand, CreateProductBrand

logger = get_logger("product_brands.repository")


class ProductBrandsRepository:
    @staticmethod
    def find_all_product_brands(connection):
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
                ProductBrand(
                    subcategories=item[0],
                    id=item[1],
                    name=item[2]
                )
                for item in result
            ]
            return None, data
        except Exception as e:
            logger.error(
                "Error en find_all_product_brands: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las marcas", None
        finally:
            cursor.close()

    @staticmethod
    def create_product_brand(data: CreateProductBrand, connection):
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT product_brand_id FROM PRODUCT_BRANDS WHERE product_brand_name = %s",
                (data["name"],)
            )

            exist_brand = cursor.fetchone()

            if exist_brand:
                return "Esta marca ya esta registrada", False, None

            cursor.execute(
                "INSERT INTO PRODUCT_BRANDS (product_brand_name) VALUES (%s)", (data["name"],))

            connection.commit()

            return None, True, "Marca creada correctamente"
        except Exception as e:
            logger.error(
                "Error en find_all_product_brands: %s",
                e,
                exc_info=True
            )
            return "Error al crear la marca", False, None
        finally:
            cursor.close()

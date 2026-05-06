from datetime import datetime
from app.utils.logger import get_logger
from dateutil.relativedelta import relativedelta
from app.features.products.models.product_serial_model import CreateProductSerial, UpdateProductSerial

logger = get_logger("product_serials.repository")


class ProductSerialsRepository:

    @staticmethod
    def find_product_by_serial(serial: str, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT
                ps.product_id,
                p.product_status
            FROM PRODUCT_SERIALS AS ps
            INNER JOIN PRODUCTS as p
                ON ps.product_id = p.product_id
            WHERE product_serial = %s
            """, (serial,))

            product = cursor.fetchone()

            if not product:
                return "Serial no encontrado"

            return product
        except Exception as e:
            logger.error(
                "Error en find_product_id_by_serial: %s",
                e,
                exc_info=True
            )
            return "Error al buscar el serial"

    @staticmethod
    def create_product_serial(serial_data: CreateProductSerial, connection):
        data = serial_data.model_dump()

        cursor = connection.cursor()
        try:
            warranty_time = None

            if data["warranty_time"] is not None:
                warranty_time = datetime.now(
                ) + relativedelta(months=data["warranty_time"])

            cursor.execute("""
            SELECT product_id FROM PRODUCT_SERIALS WHERE product_serial = %s 
            """, (data["product_serial"],))

            if cursor.fetchone():
                return "Este serial ya esta registrado", False, None

            cursor.execute("""
            INSERT INTO PRODUCT_SERIALS(
                product_serial,
                product_id,
                input_order_id,
                product_garanty_input
            ) VALUES (%s, %s, %s, %s)
            """, (
                data["product_serial"],
                data["product_id"],
                data["input_order_id"],
                warranty_time
            ))

            connection.commit()

            return None, True, "Serial del producto creado correctamente"
        except Exception as e:
            logger.error(
                "Error en create_product_serial: %s",
                e,
                exc_info=True
            )
            return "Error al crear el serial del producto", False, None
        finally:
            cursor.close()

    @staticmethod
    def update_product_serial(serial_data: UpdateProductSerial, connection):
        SERIAL_FIELD_MAP = {
            "product_serial": "product_serial",
            "input_order_id": "input_order_id",
            "warranty_time": "product_garanty_input",
        }

        cursor = connection.cursor()

        data = serial_data.model_dump(exclude_none=True)
        data.pop("id", None)

        if not data:
            return None, True, None

        # Mapea los nombres del request a los nombres reales de la tabla
        mapped = {SERIAL_FIELD_MAP[k]: v for k, v in data.items()}

        columns = ", ".join(f"{col} = %s" for col in mapped.keys())
        values = list(mapped.values()) + [serial_data.id]

        if not data:
            return None, True, None

        try:
            cursor.execute(
                f"UPDATE PRODUCT_SERIALS SET {columns} WHERE product_id = %s",
                values
            )

            return None, True, "Serial del producto actualizado correctamente"
        except Exception as e:
            logger.error("Error en update_product_serial: %s",
                         e, exc_info=True)
            return "Error al actualizar el serial del producto", False, None

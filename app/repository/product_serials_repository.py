from app.models.product_serial_model import ProductSerial, UpdateProductSerial
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.core.database import get_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProductSerialsRepository:

    @staticmethod
    def create_product_serial(serial_data: ProductSerial):
        data = serial_data.model_dump()
        connection = get_connection()
        cursor = connection.cursor()
        try:
            warranty_time = None

            if data["warranty_time"] is not None:
                warranty_time = datetime.now(
                ) + relativedelta(months=data["warranty_time"])

            cursor.execute("""
            SELECT product_id FROM PRODUCT_SERIALS WHERE product_serial = %s 
            """, (data["serial"],))

            if cursor.fetchone():
                cursor.close()
                connection.close()
                return f"Este serial ya esta registrado", False, None

            cursor.execute("""
            INSERT INTO PRODUCT_SERIALS(
                product_serial,
                product_id,
                input_order_id,
                product_garanty_input
            ) VALUES (%s, %s, %s, %s)
            """,
                           (
                               data["serial"],
                               data["product_id"],
                               data["input_order"],
                               warranty_time
                           ))

            connection.commit()

            return None, True, "Serial del producto creado correctamente"
        except Exception as e:
            logger.error("Error en create_product_serial: %s",
                         e, exc_info=True)
            return "Error al crear el serial del producto", False, None

    @staticmethod
    def update_product_serial(serial_data: UpdateProductSerial, cursor):
        SERIAL_FIELD_MAP = {
            "serial":       "product_serial",
            "input_order":  "input_order_id",
            "warranty_time": "product_garanty_input",
        }

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

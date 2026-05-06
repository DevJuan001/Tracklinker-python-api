from typing import Any
from app.core.database import get_connection
from app.utils.logger import get_logger
from app.features.output_orders.models.output_details_model import CreateOutputDetails, UpdateOutputDetails
from app.features.output_orders.repositories.output_orders_repository import OutputOrdersRepository

logger = get_logger("output_details.repository")


class OutputDetailsRepository:
    @staticmethod
    def find_output_details_by_output_order_id(output_order_id: int, connection):
        cursor = connection.cursor()

        query = """
        SELECT
            od.output_details_id,
            od.product_serial,
            od.out_product_garanty,
            od.product_transformation,
            oo.out_order_date
        FROM OUTPUT_DETAILS as od
        INNER JOIN OUTPUT_ORDERS as oo
            ON od.out_order_id = oo.out_order_id
        WHERE oo.out_order_id = %s"""

        try:
            cursor.execute(query, (output_order_id,))

            output_details = cursor.fetchone()

            if not output_details:
                return "Detalles de la orden de salida no encontrados", False, None

            return None, output_details
        except Exception as e:
            logger.error(
                "Error en find_output_details_by_output_order_id: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los de detalles de la orden de salida mediante el id de la orden de salida", None, None

    @staticmethod
    def find_output_details_by_product_serial(product_serial: str, connection):
        cursor = connection.cursor()

        query = """
        SELECT
            od.out_order_id,
            oo.out_order_date
        FROM OUTPUT_DETAILS as od
        INNER JOIN OUTPUT_ORDERS as oo
            ON od.out_order_id = oo.out_order_id
        WHERE od.product_serial = %s"""

        try:
            cursor.execute(query, (product_serial,))

            output_order = cursor.fetchone()

            if not output_order:
                return None, None, None

            return None, output_order["out_order_id"], output_order["out_order_date"]
        except Exception as e:
            logger.error(
                "Error en find_output_details_by_product_serial: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los de detalles de la orden de salida mediante el serial del producto", None, None

    @staticmethod
    def create_output_details(output_order_id: int, output_details_data: CreateOutputDetails, connection):
        data = output_details_data.model_dump()

        cursor = connection.cursor()

        # Petición a la base de datos
        query = """
        INSERT INTO OUTPUT_DETAILS (
            out_order_id,
            product_serial,
            out_product_garanty,
            product_transformation
        ) VALUES (%s, %s, %s, %s)"""

        try:
            cursor.execute(query, (
                output_order_id,
                data["product_serial"],
                data["output_product_garanty"],
                data["product_transformation"]
            ))

            return None, True, "Detalles de la orden de salida creados correctamente"

        except Exception as e:
            logger.error(
                "Error en create_output_details: %s",
                e,
                exc_info=True
            )
            return "Error al intentar crear los detalles de la orden de salida", False, None
        finally:
            cursor.close()

    @staticmethod
    def update_output_details(output_details_id: int, output_details_data: UpdateOutputDetails, connection):
        DETAILS_FIELD_MAP = {
            "product_serial": "product_serial",
            "output_order_id": "out_order_id",
            "output_product_garanty": "out_product_garanty",
            "product_transformation": "product_transformation"
        }
        data = output_details_data.model_dump(exclude_none=True)

        cursor = connection.cursor()

        try:
            # Mapea los nombres del request a los nombres reales de la tabla
            mapped = {
                DETAILS_FIELD_MAP[key]: value
                for key, value in data.items()
            }

            columns = ", ".join(f"{col} = %s" for col in mapped.keys())
            values = list[Any](mapped.values()) + [output_details_id]

            cursor.execute(
                f"UPDATE OUTPUT_DETAILS SET {columns} WHERE output_details_id = %s",
                values
            )

            return None, True, "Detalle de salida actualizados correctamente"
        except Exception as e:
            logger.error(
                "Error en update_output_details: %s",
                e,
                exc_info=True
            )
            return "Error al intentar actualizar los detalles de la orden de salida", False, None
        finally:
            cursor.close()

from app.core.database import get_connection
from app.models.output_details_model import OutputDetails
from app.repository.output_orders_repository import OutputOrdersRepository
from app.models.output_orders_model import OutputOrder


class OutputDetailsRepository:

    # Obtener todos los detalles de salida
    @staticmethod
    def find_all_outpuDetails():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT * FROM get_output_products ORDER BY out_order_id DESC
        """
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return None, results
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", None
        finally:
            cursor.close()
            connection.close()

    # Obtener detalle de salida por Id

    @staticmethod
    def find_by_id(output_details_id: int):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
         SELECT * FROM OUTPUT_DETAILS WHERE OUTPUT_DETAILS_ID = %s 
        """
        try:
            cursor.execute(query, (output_details_id,))
            result = cursor.fetchall()
            return None, result
        except Exception as e:
            f"Error al ejecutar la consulta: {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_by_product_serial(product_serial: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

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
        except Exception:
            return "Error al ejecutar la consulta", None, None

    @staticmethod
    def create(output_details_data: OutputDetails):
        data = output_details_data.model_dump()

        connection = get_connection()
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
            error, success, out_order_id = OutputOrdersRepository.create()

            if error is not None or not success:
                return error, False, None
            
            cursor.execute(query, (
                out_order_id,
                data["product_serial"],
                data["out_product_garanty"],
                data["product_transformation"]
                ))
            connection.commit()
            return None, True, "Orden de salida creada correctamente"
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", False, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update(output_details_id: int, outputDetails_data: dict):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        UPDATE OUTPUT_DETAILS SET
            product_serial = %s,
            out_product_garanty = %s,
            product_transformation = %s
        WHERE output_details_id = %s"""

        try:
            cursor.execute(
                "SELECT product_serial FROM OUTPUT_DETAILS WHERE output_details_id = %s",
                (output_details_id,)
            )
            current = cursor.fetchone()

            if not current:
                return "Detalle de salida no encontrado.", False, None

            new_serial = outputDetails_data["product_serial"]
            current_serial = current["product_serial"]

            if new_serial != current_serial:
                cursor.execute(
                    "SELECT output_details_id FROM OUTPUT_DETAILS WHERE product_serial = %s",
                    (new_serial,)
                )
            existing = cursor.fetchone()

            if existing:
                return f"El serial '{new_serial}' ya está asignado a otro producto.", False, None
            
            cursor.execute(query, (
                new_serial,
                outputDetails_data["out_product_garanty"],
                outputDetails_data["product_transformation"],
                output_details_id
            ))
            connection.commit()

            error, success, message = OutputOrdersRepository.update(
                output_order_id = outputDetails_data["out_order_id"],
                output_order_data= {"out_order_status": outputDetails_data["out_order_status"]})
            
            if error:
                return error, success, message

            return None, True, "Detalle de salida actualizada correctamente"
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", False, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def disable(out_order_id: int):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT out_order_id FROM OUTPUT_ORDERS WHERE out_order_id = %s", (out_order_id,))
        
        output = cursor.fetchone()
        if not output:
            cursor.close()
            connection.close()
            return "Detalle de salida no encontrado", False, None

        query = "UPDATE OUTPUT_ORDERS SET out_order_status = 1 WHERE out_order_id = %s"

        try:
            cursor.execute(query, (out_order_id,))
            connection.commit()
            return None, True, "Detalle de salida deshabilitado correctamente"
        except Exception as e:
            return f"Error la intentar ejecutar la consulta {e}", False, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def enable(out_order_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT out_order_id FROM OUTPUT_ORDERS WHERE out_order_id = %s", (out_order_id,))
        
        output = cursor.fetchone()
        if not output:
            cursor.close()
            connection.close()
            return "Detalle de salida no encontrado", False, None

        query = "UPDATE OUTPUT_ORDERS SET out_order_status = 2 WHERE out_order_id = %s"

        try:
            cursor.execute(query, (out_order_id,))
            connection.commit()
            return None, True, "Detalle de salida habilitado correctamente"
        except Exception as e:
            return f"Error la intentar ejecutar la consulta {e}", False, None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_transformations_by_date_range(start_date: str, end_date: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT * FROM output_details
        WHERE transformation_date BETWEEN %s AND %s
        """
        try:
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            return None, results
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_deleted_transformations_by_date_range(start_date: str, end_date: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT * FROM output_details
        WHERE deleted_at IS NOT NULL
        AND deleted_at BETWEEN %s AND %s
        ORDER BY deleted_at DESC
        """
        try:
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            return None, results
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_all_transformations():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT * FROM output_details ORDER BY output_details_id DESC
        """
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return None, results
        except Exception as e:
            return f"Error al ejecutar la consulta: {e}", None
        finally:
            cursor.close()
            connection.close()

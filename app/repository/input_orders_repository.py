from app.core.database import get_connection
from app.models.input_order_model import InputOrder


class InputOrdersRepository:

    @staticmethod
    def find_all_input_orders():
        connection = get_connection()
        cursor = connection.cursor()

        query = "SELECT input_order_id, input_order_bill FROM INPUT_ORDERS"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            data = [
                {
                    "id": item[0],
                    "bill": item[1]
                }
                for item in result
            ]
            return None, data
        except Exception:
            return f"Error al ejecutar la consulta", None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create_input_order(input_order_data: InputOrder):
        data = input_order_data.model_dump()
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("""
            INSERT INTO INPUT_ORDERS(
                input_order_bill,
                supplier_id
            ) VALUES (%s, %s)
            """, (data["input_order_bill"], data["supplier_id"]))
            connection.commit()
            return None, True, f"Orden de entrada creada correctamente"
        except Exception:
            return f"Error al crear la orden de entrada", False, None

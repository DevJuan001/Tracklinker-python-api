import bcrypt
from pydantic import EmailStr
from app.utils.logger import get_logger
from app.core.exception import ServiceError
from app.core.database import get_connection
from app.tasks.email_tasks import send_welcome_client_email, send_welcome_email
from app.core.security import generate_temporal_password, verify_password
from app.features.users.repositories.roles_repository import RolesRepository
from app.features.users.repositories.users_repository import UsersRepository
from app.features.users.repositories.cities_repository import CitiesRepository
from app.features.users.models.users_schemas import CreateClientSchema, UpdatePasswordSchema, UsersFiltersSchema, CreateUserSchema, UpdateUserSchema

logger = get_logger("users.service")


class UsersService:
    @staticmethod
    def get_all_users(filters: UsersFiltersSchema):
        connection = get_connection()

        try:
            error, users = UsersRepository.find_all_users(
                filters, connection
            )

            if error:
                raise ServiceError(error)

            return None, users

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_users: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los usuarios", None

        finally:
            connection.close()

    @staticmethod
    def get_active_clients():
        connection = get_connection()

        try:
            error, clients = UsersRepository.find_active_clients(
                connection
            )

            if error:
                raise ServiceError(error)

            return None, clients

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_active_clients: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los clientes activos", None

        finally:
            connection.close()

    @staticmethod
    def get_user_by_id(user_id: int):
        connection = get_connection()

        try:
            error, user = UsersRepository.find_user_by_id(
                user_id, connection
            )

            if error or not user:
                raise ServiceError(error)

            return None, user

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_user_by_id: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el usuario mediante el id", None

    @staticmethod
    def get_user_by_email(email: EmailStr):
        connection = get_connection()

        try:
            error, user = UsersRepository.find_user_by_email(
                email, connection
            )

            if error or not user:
                raise ServiceError(error)

            return None, user

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_user_by_email: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener el usuario mediante el correo", None

    @staticmethod
    def get_all_roles():
        connection = get_connection()

        try:
            error, roles = RolesRepository.find_all_roles(
                connection
            )

            if error or not roles:
                raise ServiceError(error)

            return None, roles

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_roles: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener los roles", None

    @staticmethod
    def get_all_cities():
        connection = get_connection()

        try:
            error, cities = CitiesRepository.find_all_cities(
                connection
            )

            if error or not cities:
                raise ServiceError(error)

            return None, cities

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            logger.error(
                "Error en get_all_cities: %s",
                e,
                exc_info=True
            )
            return "Error al intentar obtener las ciudades", None

    @staticmethod
    async def create_user(user_data: CreateUserSchema):
        data = user_data.model_dump()

        connection = get_connection()

        try:
            # Verificar que no este registrado ya un usuario con el correo que viene
            error, user = UsersRepository.find_user_by_email(
                email=data["email"],
                connection=connection
            )

            if error:
                raise ServiceError(error)

            if user:
                raise ServiceError(
                    "Este correo ya esta registrado, intenta ingresar otro correo e intentalo nuevamente"
                )

            temporal_password = generate_temporal_password()

            # Hashear la contraseña
            password = temporal_password.encode("utf-8")
            hash_password = bcrypt.hashpw(
                password, bcrypt.gensalt(rounds=12)
            ).decode("utf-8")

            error, success, message = UsersRepository.create_user(
                user_data=user_data,
                hash_password=hash_password,
                connection=connection
            )

            if error or not success:
                raise ServiceError(error)

            if success:
                send_welcome_email.delay(
                    user_name=data["name"],
                    user_first_surname=data["first_surname"],
                    user_email=data["email"],
                    password=temporal_password
                )

            connection.commit()

            return None, True, "Usuario Creado Correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error(
                "Error en create_user: %s",
                e,
                exc_info=True
            )
            return "Error al intentar crear el usuario", False, None

    @staticmethod
    async def create_client(client_data: CreateClientSchema):
        data = client_data.model_dump()

        connection = get_connection()

        try:
            error, user = UsersRepository.find_user_by_email(
                email=data["email"],
                connection=connection
            )

            if error:
                raise ServiceError(error)

            if user:
                raise ServiceError(
                    "Este correo ya esta registrado, intenta ingresar otro correo e intentalo nuevamente"
                )

            error, success, message = UsersRepository.create_client(
                client_data=client_data,
                connection=connection
            )

            if error or not success:
                raise ServiceError(error)

            if success:
                send_welcome_client_email.delay(
                    user_name=data["name"],
                    user_first_surname=data["first_surname"],
                    user_email=data["email"]
                )

            connection.commit()

            return None, True, "Cliente Creado Correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error(
                "Error en create_client: %s",
                e,
                exc_info=True
            )
            return "Error al intentar crear el cliente", False, None

        finally:
            connection.close()

    @staticmethod
    def update_user(user_id: int, user_data: UpdateUserSchema):
        data = user_data.model_dump(exclude_none=True)
        connection = get_connection()

        try:
            # Verificar si existe el usuario
            error, user = UsersRepository.find_user_by_id(
                user_id, connection
            )

            if not user:
                raise ServiceError(error)

            # Verificar si el correo ya esta siendo usado y no duplicarlo
            if "email" in data:
                error, existing_user = UsersRepository.find_user_by_email(
                    data["email"], connection
                )

                if existing_user and (existing_user[1] != user_id):
                    raise ServiceError(
                        "El correo ya está registrado, ingresa un correo diferente e intentalo nuevamente"
                    )

            error, success, message = UsersRepository.update_user(
                user_id, user_data, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Usuario Actualizado Correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error(
                "Error en update_user: %s",
                e,
                exc_info=True
            )
            return "Error al intentar actualizar el usuario", False, None

        finally:
            connection.close()

    @staticmethod
    def update_user_password(password_data: UpdatePasswordSchema, user_id: int):
        data = password_data.model_dump()

        connection = get_connection()

        if data["new_password"] != data["repeat_password"]:
            raise ServiceError("Las contraseñas no coiniciden")

        try:
            # Buscamos la contraseña del usuario con ese id
            error, user = UsersRepository.find_user_password_by_id(
                user_id, connection
            )

            if error or not user:
                raise ServiceError(error)

            # Validamos que la contraseña antigua sea igual a la que esta registrada
            verify_password(
                str(user[0]), data["old_password"]
            )

            error, success, message = UsersRepository.update_user_password(
                user_id, data["new_password"], connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Contraseña actualizada correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error(
                "Error en update_user_password: %s",
                e,
                exc_info=True
            )
            return "Error al intentar actualizar la contraseña", False, None

        finally:
            connection.close()

    @staticmethod
    def disable_user(user_id: int):
        connection = get_connection()

        try:
            # Validar que el usuario exista
            error, user = UsersRepository.find_user_by_id(
                user_id, connection
            )

            if error or not user:
                raise ServiceError(error)

            error, success, message = UsersRepository.disable_user(
                user_id, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Usuario deshabilitado correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error(
                "Error en disable_user: %s",
                e,
                exc_info=True
            )
            return "Error al intentar deshabilitar el usuario", False, None

    @staticmethod
    def enable_user(user_id: int):
        connection = get_connection()

        try:
            # Validar que el usuario exista
            error, user = UsersRepository.find_user_by_id(
                user_id, connection
            )

            if error or not user:
                raise ServiceError(error)

            error, success, message = UsersRepository.enable_user(
                user_id, connection
            )

            if error or not success:
                raise ServiceError(error)

            connection.commit()

            return None, True, "Usuario habilitado correctamente"

        except ServiceError as e:
            connection.rollback()
            return e.message, False, None

        except Exception as e:
            connection.rollback()
            logger.error(
                "Error en enable_user: %s",
                e,
                exc_info=True
            )
            return "Error al intentar habilitar el usuario", False, None

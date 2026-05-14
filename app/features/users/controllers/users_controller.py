from fastapi import HTTPException
from app.features.users.services.users_service import UsersService
from app.features.users.models.users_schemas import CreateUserSchema, UpdateCurrentUserSchema, UpdatePasswordSchema, UpdateUserSchema, UsersFiltersSchema


class UsersController:

    @staticmethod
    def get_all_users(filters: UsersFiltersSchema):
        error, users = UsersService.get_all_users(filters)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": users
        }

    @staticmethod
    def get_user_by_id(user_id: int):
        error, user = UsersService.get_user_by_id(user_id)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": user
        }

    @staticmethod
    def get_current_user(payload: dict):
        error, user = UsersService.get_user_by_id(int(payload["user_id"]))

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": user
        }

    @staticmethod
    def get_user_by_email(email: str):
        error, user = UsersService.get_user_by_email(email)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": user
        }

    @staticmethod
    def get_all_roles():
        error, data = UsersService.get_all_roles()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": data
        }

    @staticmethod
    def get_all_cities():
        error, cities = UsersService.get_all_cities()

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "data": cities
        }

    @staticmethod
    async def create_user(user_data: CreateUserSchema):
        error, success, message = await UsersService.create_user(
            user_data
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_user(user_id: int, user_data: UpdateUserSchema):
        error, success, message = UsersService.update_user(
            user_id, user_data
        )

        if error:
            raise HTTPException(status_code=400, detail=error)

        return {
            "success": success,
            "message": message,
        }

    @staticmethod
    def update_current_user(user_data: UpdateCurrentUserSchema, payload: dict):
        error, success, message = UsersService.update_user(
            payload["user_id"], user_data
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_user_password(password_data: UpdatePasswordSchema, payload: dict):
        error, success, message = UsersService.update_user_password(
            password_data, payload["user_id"]
        )

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def disable_user(user_id: int):
        error, success, message = UsersService.disable_user(user_id)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def enable_user(user_id: int):
        error, success, message = UsersService.enable_user(user_id)

        if error:
            raise HTTPException(status_code=404, detail=error)

        return {
            "success": success,
            "message": message
        }

from datetime import timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.repository.user_repository import UserRepository
from app.models.user_model import User
from app.core.mail import config
from fastapi_mail import FastMail, MessageSchema
from app.core.security import create_access_token, generate_temporal_password
from app.core.config import settings


class UserController:

    @staticmethod
    def login(form_data: OAuth2PasswordRequestForm = Depends()):
        error, email = UserRepository.find_by_email(form_data.email)

        expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
        token = create_access_token(
            {"sub": form_data.email}, expires_delta=expires)

        if error:
            raise HTTPException(status_code=404, detail=error)

        if email:
            raise

        return {
            "token": token
        }

    @staticmethod
    def get_all_users(
        role_order: int = None,
        name_order: str = None,
        start_date: str = None,
        end_date: str = None,
        status: int = None,
    ):
        error, users = UserRepository.find_all_users(
            role_order,
            name_order,
            start_date,
            end_date,
            status,
        )
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": users
        }

    @staticmethod
    def get_user_by_id(user_id: int):
        error, user = UserRepository.find_user_by_id(user_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": user
        }

    @staticmethod
    def get_all_cities():
        error, cities = UserRepository.find_all_cities()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": cities
        }

    @staticmethod
    async def create_user(user_data: User):
        data = user_data.model_dump()
        temporal_password = generate_temporal_password()

        error, success, message = UserRepository.create(
            user_data, temporal_password)

        if error:
            raise HTTPException(status_code=400, detail=error)

        if success == True:
            emailMessage = MessageSchema(
                subject="Bienvenido a Tracklinker",
                recipients=[data["email"]],
                template_body={
                    "name": data["name"],
                    "surname": data["first_surname"],
                    "email": data["email"],
                    "password": temporal_password
                },
                subtype="html",
            )
            fm = FastMail(config)
            await fm.send_message(emailMessage, template_name="welcome_mail.html")

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def update_user(user_id: int, user_data: dict):
        error, success, message = UserRepository.update(user_id, user_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {
            "success": success,
            "message": message,
        }

    @staticmethod
    def disable_user(user_id: int):
        error, success, message = UserRepository.disable(user_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def enable_user(user_id: int):
        error, success, message = UserRepository.enable(user_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def get_all_roles():
        error, data = UserRepository.find_all_roles()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {
            "data": data
        }

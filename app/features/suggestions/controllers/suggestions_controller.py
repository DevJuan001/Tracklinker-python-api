from app.core.mail import fm
from app.core.config import settings
from fastapi import HTTPException
from fastapi_mail import MessageSchema
from app.features.users.services.users_service import UsersService


class SuggestionsController:
    @staticmethod
    async def send_suggestion_mail(suggestion: str, payload: dict):

        error, user = UsersService.get_user_by_id(payload["user_id"])

        if error:
            raise HTTPException(status_code=404, detail=error)

        message = MessageSchema(
            subject="Sugerencia o error",
            recipients=[settings.MAIL_FROM],
            template_body={"email": user[0].email, "suggestion": suggestion},
            subtype="html",
        )

        await fm.send_message(message, template_name="suggestion_mail.html")

        return {
            "success": True,
            "message": "Correo enviado correctamente"
        }

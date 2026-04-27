from app.core.mail import config
from app.core.config import settings
from fastapi_mail import FastMail, MessageSchema
from fastapi import HTTPException
from app.repository.user_repository import UserRepository


class SuggestionsController:
    @staticmethod
    async def send_suggestion_mail(suggestion: str, payload: dict):

        error, user = UserRepository.find_by_id(int(payload["user_id"]))

        data = user[0]

        if error:
            raise HTTPException(status_code=404, detail=error)

        message = MessageSchema(
            subject="Sugerencia o error",
            recipients=[settings.MAIL_FROM],
            template_body={"email": data["email"], "suggestion": suggestion},
            subtype="html",
        )

        fm = FastMail(config)
        await fm.send_message(message, template_name="suggestion_mail.html")

        return {
            "success": True,
            "message": "Correo enviado correctamente"
        }

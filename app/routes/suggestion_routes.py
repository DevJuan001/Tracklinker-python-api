from fastapi import APIRouter, Depends, Body
from app.middlewares.jwt_middleware import verify_jwt
from app.models.suggestion_model import SuggestionModel
from app.controllers.suggestions_controller import SuggestionsController

router = APIRouter(
    prefix="/api/suggestions",
    tags=["Suggestions"]
)

# Endpoint para enviar un correo con la sugerencia
@router.post("/send")
async def login(body: SuggestionModel, payload: dict = Depends(verify_jwt)):
    return await SuggestionsController.send_suggestion_mail(body.suggestion, payload)

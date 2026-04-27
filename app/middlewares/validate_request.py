from fastapi import Request
from starlette.responses import JSONResponse

# funcion para validar si la peticion fua cancelada
async def validate_request(request: Request):
    if request.is_disconnected():
        return JSONResponse(
            status_code=499,
            content={
                "success": False,
                "message": "Solicitud cancelada o abortada"
            }
        )
    return None

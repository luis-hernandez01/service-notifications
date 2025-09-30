from fastapi import APIRouter, HTTPException, Depends
from src.models.smtp_model_basic import EmailRequest
from src.services.send_services import O365EmailService
from sqlalchemy.orm import Session
from src.config.config import get_session

sendemail_routes = APIRouter(tags=["Envio correo basico"])


@sendemail_routes.post("/send-email")
async def send_email(request: EmailRequest, db: Session = Depends(get_session)):
    # Endpoint para enviar un correo usando O365.
    try:
        result = await O365EmailService(db, request).send(request)
        return {"message": "Correo enviado correctamente", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
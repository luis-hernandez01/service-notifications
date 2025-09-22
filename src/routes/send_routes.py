from fastapi import APIRouter, HTTPException, Depends
from src.models.smtp_model import EmailRequest
from src.services.send_services import O365EmailService, SmtpEmailService
from sqlalchemy.orm import Session
from src.config.config import get_session

sendemail_routes = APIRouter()


@sendemail_routes.post("/send-email")
async def send_email(request: EmailRequest, db: Session = Depends(get_session)):
    # Endpoint para enviar un correo usando O365.
    try:
        result = await O365EmailService(db).send(request)
        return {"message": "Correo enviado correctamente", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



@sendemail_routes.post("/sendemail-smtp")
async def send_emailsmtp(request: EmailRequest, db: Session = Depends(get_session)):
    # Endpoint para enviar un correo usando SMTP.
    try:
        result = await SmtpEmailService(db).send(request)
        return {"message": "Correo enviado correctamente", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando correo: {str(e)}")
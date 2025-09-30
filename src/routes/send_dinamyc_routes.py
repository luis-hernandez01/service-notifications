# from fastapi import APIRouter, HTTPException, Depends
# from src.models.smtp_model import EmailRequest
# from src.services.send_dinamyc_services import SendDinamycO365Service
# from sqlalchemy.orm import Session
# from src.config.config import get_session

# send_router = APIRouter()

# @send_router.post("/send")
# async def send_email(request: EmailRequest, db: Session = Depends(get_session)):
#     # Endpoint para enviar un correo usando O365.
#     try:
#         result = await SendDinamycO365Service(db, request).send(request)
#         return {"message": "Correo enviado correctamente", "detail": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




from fastapi import APIRouter, Depends, UploadFile, Form, File
from sqlalchemy.orm import Session
from src.config.config import get_session
from src.services.send_dinamyc_services import SendDinamycO365Service
from src.models.smtp_model import EmailRequest

send_router = APIRouter(tags=["Envio correo avanzado"])

@send_router.post("/send-email-form")
async def send_email_form(
    form: EmailRequest = Depends(),
    db: Session = Depends(get_session),
):
    service = SendDinamycO365Service(db, form)
    result = await service.send(form)
    return {"message": "Correo procesado", "detail": result}

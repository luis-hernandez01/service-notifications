from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.config import get_session
from src.models.smtp_model import EmailRequest
from src.security.auth import verify_jwt_token
from src.services.send_dinamyc_services import SendDinamycO365Service

router = APIRouter(tags=["Envio correo avanzado"])


@router.post("/send-email-form")
async def send_email_form(
    form: EmailRequest = Depends(),
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: str = Depends(verify_jwt_token),
):
    service = SendDinamycO365Service(db, form, tokenpayload=tokenpayload["token"])
    result = await service.send(form)
    return {"message": "Correo procesado", "detail": result}

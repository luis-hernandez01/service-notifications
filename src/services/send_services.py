# Servicio de envío de correos electrónicos vía SMTP (asíncrono).

from email.mime.text import MIMEText
from aiosmtplib import SMTP
from src.interfaces.email_service import IEmailService
from src.models.smtp_model import EmailRequest
from src.config.config import settings
from fastapi.responses import JSONResponse

class SmtpEmailService(IEmailService):
# Implementación de envío de correos vía SMTP (asincronico)

    async def send(self, req: EmailRequest) -> None:
        try:
            msg = MIMEText(req.body, "html" if req.is_html else "plain")
            msg["From"] = settings.EMAIL_FROM
            msg["To"] = req.to
            msg["Subject"] = req.subject

            async with SMTP(hostname=settings.SMTP_SERVER, port=settings.SMTP_PORT) as smtp:
                # await smtp.starttls()  # seguridad TLS
                await smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
                await smtp.send_message(msg)
                
                # response = JSONResponse(
                #     content={
                #     "status": "success",
                #     "message": f"Correo enviado a {req.to}",
                #     "to": req.to,
                #     "subject": req.subject,
                #     },
                # status_code=200,
                # )
                # print(response.body.decode())
                
                # Respuesta exitosa
                return JSONResponse(
                    content={
                        "status": "success",
                        "message": f"Correo enviado a {req.to}",
                        "subject": req.subject,
                        },
                    status_code=200,
            )
                
        except Exception as e:
            # Manejo de errores durante el envío
            return JSONResponse(
                content={
                    "status": "error",
                    "message": str(e),
                    "to": req.to,
                    "subject": req.subject,
                },
                status_code=500,
            )
            





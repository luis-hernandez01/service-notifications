# Módulo de rutas para el envío de correos electrónicos vía SMTP.
# exponemos el endpoint para enviar correos de forma asíncrona

# dependencias y paqueterias utilizadas en el desarrollo del modulo de notificaciones
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from src.services.send_services import SmtpEmailService
from src.models.smtp_model import EmailRequest
import asyncio
from fastapi.responses import JSONResponse

# inicializacion del roter 
sendemail_routes = APIRouter()

# Este endpoint permite enviar correos electrónicos mediante el servicio SMTP.
# La tarea de envío se ejecuta en segundo plano utilizando `BackgroundTasks`,
# lo cual asegura una respuesta rápida al cliente sin necesidad de esperar
# que el correo se envíe completamente.

@sendemail_routes.post("/sendSMTP")
async def send_email(req: EmailRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(SmtpEmailService().send, req)
    
    # Retorna confirmación inmediata al cliente sobre el envio del correo
    return JSONResponse(
        content={
            "status": "success",
            "message": "Correo en proceso de envío",
            "to": req.to,
            "subject": req.subject,
        },
        status_code=202, # Codigo http 202 = Accepted (procesamiento en curso)
    )
from O365 import Account
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import aiosmtplib
from pathlib import Path
from sqlalchemy.orm import Session
from src.models.smtp_model import EmailRequest
from src.models.plantilla_model import Plantillas
from src.config.config import settings

import asyncio


class O365EmailService:
    # Servicio para enviar correos usando O365 con Application Permissions (async-safe).
    

    def __init__(self, db: Session):
        self.db = db
        credentials = (settings.CLIENT_ID, settings.CLIENT_SECRET)
        self.account = Account(
            credentials=credentials,
            auth_flow_type="credentials",  # App permissions
            tenant_id=settings.TENANT_ID
        )

        # Autenticación obligatoria (bloqueante, la envolvemos en hilo)
        if not self.account.is_authenticated:
            if not self.account.authenticate():
                raise Exception("Error de autenticación con O365")

    async def send(self, req: EmailRequest) -> dict:
        # se envia correo de manera asincronica
        usernames = settings.USERNAME
        mailbox = self.account.mailbox(usernames)

        # Las operaciones O365 son bloqueantes → moverlas a hilo
        def build_and_send():
            message = mailbox.new_message()

            dataplantilla = self.db.query(Plantillas).filter(
                Plantillas.identifying_name == req.identifying_name
            ).first()

            # Destinatarios
            message.to.add(req.to)
            if req.cc:
                for cc in req.cc:
                    message.cc.add(cc)
            if req.bcc:
                for bcc in req.bcc:
                    message.bcc.add(bcc)

            # Contenido
            message.subject = req.subject
            message.body = dataplantilla.content_html if dataplantilla else req.body_html
            message.body_type = "HTML"

            # Adjuntos
            if req.adjuntos:
                for adj in req.adjuntos:
                    path = Path(adj)
                    if path.exists():
                        message.attachments.add(path)
                    else:
                        print(f"Adjunto no encontrado: {adj}, ignorando...")

            # Imágenes embebidas
            if req.imagenes_embed:
                for cid, img_path in req.imagenes_embed.items():
                    path = Path(img_path)
                    if path.exists():
                        attachment = message.attachments.add(path)
                        if attachment:
                            attachment.is_inline = True
                            attachment.content_id = cid
                    else:
                        print(f"Imagen no encontrada: {img_path}, ignorando...")

            # Enviar correo (bloqueante)
            message.send()

        # Ejecutar en thread para no bloquear el event loop
        await asyncio.to_thread(build_and_send)

        return {"status": "Enviado", "A": req.to}














class SmtpEmailService:
    """
    Servicio para enviar correos usando SMTP clásico (asincrónico con aiosmtplib).
    """

    def __init__(self, db: Session):
        self.db = db
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD

    async def send(self, req: EmailRequest) -> dict:
        # Construir mensaje MIME
        msg = MIMEMultipart("related")
        msg["From"] = self.user
        msg["To"] = req.to
        msg["Subject"] = req.subject

        if req.cc:
            msg["Cc"] = ", ".join(req.cc)
        if req.bcc:
            msg["Bcc"] = ", ".join(req.bcc)

        # Plantilla en DB
        dataplantilla = self.db.query(Plantillas).filter(
            Plantillas.identifying_name == req.identifying_name
        ).first()

        body_html = dataplantilla.content_html if dataplantilla else req.body_html

        # Parte HTML
        alternative = MIMEMultipart("alternative")
        alternative.attach(MIMEText(body_html, "html"))
        msg.attach(alternative)

        # Adjuntos
        if req.adjuntos:
            for adj in req.adjuntos:
                path = Path(adj)
                if path.exists():
                    with open(path, "rb") as f:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename={path.name}")
                        msg.attach(part)
                else:
                    print(f"Adjunto no encontrado: {adj}, ignorando...")

        # Imágenes embebidas
        if req.imagenes_embed:
            for cid, img_path in req.imagenes_embed.items():
                path = Path(img_path)
                if path.exists():
                    with open(path, "rb") as f:
                        img = MIMEImage(f.read())
                        img.add_header("Content-ID", f"<{cid}>")
                        img.add_header("Content-Disposition", "inline", filename=path.name)
                        msg.attach(img)
                else:
                    print(f"Imagen no encontrada: {img_path}, ignorando...")

        # Enviar correo vía SMTP
        try:
            await aiosmtplib.send(
                msg,
                hostname=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                start_tls=True
            )
            return {"status": "Enviado", "to": req.to}
        except Exception as e:
            return {"status": "Error", "error": str(e)}

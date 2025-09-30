from fastapi import HTTPException
from O365 import Account
from pathlib import Path
from sqlalchemy.orm import Session
import asyncio, re
from datetime import datetime
from src.models.smtp_model import EmailRequest
from src.models.plantilla_model import Plantillas
from src.models.credenciales_model import CredencialesCorreo
from src.models.logs_envio import LogsEnvio
import shutil


class SendDinamycO365Service:
    def __init__(self, db: Session, req: EmailRequest):
        self.db = db

        data = self.db.query(Plantillas).filter(
            Plantillas.identifying_name == req.identifying_name
        ).first()
        
        if not data:
            raise HTTPException(status_code=404, detail=f"No se encontraron credenciales con identificador '{req.identifying_name}'")

        creds = self.db.query(CredencialesCorreo).filter(
            CredencialesCorreo.id == data.credenciales_id
        ).first()

        if not creds:
            raise HTTPException(status_code=404, detail=f"No se encontraron credenciales con identificador '{data.credenciales_id}'")

        credentials = (creds.client_id, creds.client_secret)

        self.account = Account(
            credentials=credentials,
            auth_flow_type="credentials",
            tenant_id=creds.tenant_id
        )

        if not self.account.is_authenticated:
            if not self.account.authenticate():
                raise HTTPException(status_code=401, detail=f"Error de autenticación con O365")
            

        self.username = creds.username

    def validar_email(self, email: str) -> bool:
        """Valida sintaxis de email"""
        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(patron, email) is not None

    async def send(self, req: EmailRequest) -> dict:
        mailbox = self.account.mailbox(self.username)

        def build_and_send():
            try:
                message = mailbox.new_message()
                
                def render_template(template: str, variables: dict) -> str:
                    """Reemplaza {{etiqueta}} con todo el contenido del JSON convertido a HTML"""
                    if not isinstance(variables, dict):
                        return template.replace("{{etiqueta}}", str(variables))

                    # Convertimos el dict en un bloque HTML (tabla simple)
                    rows = "".join(
                        f"<li><strong>{k}:</strong>{v}</li>" for k, v in variables.items()
                    )
                    html_table = f"{rows}"

                    return template.replace("{{etiqueta}}", html_table)



                dataplantilla = self.db.query(Plantillas).filter(
                    Plantillas.identifying_name == req.identifying_name
                ).first()
                contenido_html = dataplantilla.content_html if dataplantilla else req.body_html
                #  Si body_html es un dict, lo inyectamos
                if isinstance(req.body_html, dict) and dataplantilla:
                    contenido_html = render_template(dataplantilla.content_html, req.body_html)

                # Validar destinatarios
                if not self.validar_email(req.to):
                    raise HTTPException(status_code=500, detail=f"Correo inválido en TO: {req.to}")
                message.to.add(req.to)

                if req.cc:
                    for cc in req.cc:
                        if not cc:
                            continue
                        if not self.validar_email(cc):
                            raise HTTPException(status_code=500, detail=f"Correo inválido en CC: {cc}")
                        message.cc.add(cc)


                if req.bcc:
                    for bcc in req.bcc:
                        if not bcc:  # 👈 evita procesar valores vacíos
                            continue
                        if not self.validar_email(bcc):
                            raise HTTPException(status_code=500, detail=f"Correo inválido en BCC: {bcc}")
                        message.bcc.add(bcc)


                # Contenido
                message.subject = req.subject
                message.body = contenido_html
                message.body_type = "HTML"
                
                UPLOAD_DIR = Path("uploads/adjuntos")

                # Crear carpeta por fecha para organizar los adjuntos
                today_dir = UPLOAD_DIR / datetime.today().strftime("%Y-%m-%d")
                today_dir.mkdir(parents=True, exist_ok=True)
                
                # Adjuntos (ya son UploadFile)
                adjuntos_guardados = []
                if req.adjuntos:
                    for adj in req.adjuntos:
                        destino = today_dir / adj.filename
                        with open(destino, "wb") as buffer:
                            shutil.copyfileobj(adj.file, buffer)

                        # adjuntar al correo
                        message.attachments.add(str(destino))
                        adjuntos_guardados.append(str(destino))

                # Imágenes embed
                imagenes_guardadas = []
                if req.imagenes_embed:
                    for img in req.imagenes_embed:
                        destino = today_dir / img.filename
                        with open(destino, "wb") as buffer:
                            shutil.copyfileobj(img.file, buffer)

                        attachment = message.attachments.add(str(destino))
                        if attachment:
                            attachment.is_inline = True
                            # usamos filename como cid
                            attachment.content_id = img.filename
                            imagenes_guardadas.append(f"{img.filename}:{destino}")

                # Enviar
                message.send()

                # Log de éxito
                log = LogsEnvio(
                    destinatario=req.to,
                    cc=";".join(req.cc) if req.cc else None,
                    bcc=";".join(req.bcc) if req.bcc else None,
                    adjuntos=";".join(adjuntos_guardados) if adjuntos_guardados else None,  # usamos rutas guardadas
                    num_adjuntos=len(adjuntos_guardados),
                    imagenes=";".join(imagenes_guardadas) if imagenes_guardadas else None,
                    num_imagenes=len(imagenes_guardadas),
                    asunto=req.subject,
                    contenido=contenido_html,
                    estado="ENVIADO",
                    fecha_envio=datetime.utcnow(),
                    identificador=req.identifying_name,
                    detalle="Correo enviado correctamente"
                )

                self.db.add(log)
                self.db.commit()

            except Exception as e:
                # Log de error (incluye errores de sintaxis)
                log = LogsEnvio(
                    destinatario=req.to,
                    cc=";".join(req.cc) if req.cc else None,
                    bcc=";".join(req.bcc) if req.bcc else None,
                    adjuntos=";".join([adj.filename for adj in req.adjuntos]) if req.adjuntos else None,  # 👈 filenames
                    num_adjuntos=len(req.adjuntos) if req.adjuntos else 0,
                    imagenes=";".join([img.filename for img in req.imagenes_embed]) if req.imagenes_embed else None,
                    num_imagenes=len(req.imagenes_embed) if req.imagenes_embed else 0,
                    asunto=req.subject,
                    contenido=req.body_html,
                    estado="ERROR",
                    fecha_envio=datetime.utcnow(),
                    identificador=req.identifying_name,
                    detalle=str(e)
                )

                self.db.add(log)
                self.db.commit()
                raise

        await asyncio.to_thread(build_and_send)
        return {"status": "Procesado", "A": req.to}

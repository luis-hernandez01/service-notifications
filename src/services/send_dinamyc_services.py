import asyncio
import re
import shutil
import smtplib
from datetime import datetime
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.credenciales_model import CredencialesCorreo
from src.models.logs_envio import LogsEnvio
from src.models.plantilla_model import Plantillas
from src.models.smtp_model import EmailRequest
from src.config.config import URL_API_STORAGE


class SendDinamycO365Service:
    def __init__(self, db: Session, req: EmailRequest, tokenpayload):
        self.db = db
        self.token  = tokenpayload
        # self.token = tokenpayload.get("token") if tokenpayload else None

        # Buscar plantilla
        plantilla = (
            db.query(Plantillas)
            .filter(Plantillas.identifying_name == req.identifying_name)
            .first()
        )
        if not plantilla:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró la plantilla '{req.identifying_name}'",
            )

        # Buscar credenciales asociadas
        creds = (
            db.query(CredencialesCorreo)
            .filter(CredencialesCorreo.id == plantilla.credenciales_id)
            .first()
        )
        if not creds:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron credenciales con ID '{plantilla.credenciales_id}'",
            )

        # Configuración SMTP
        self.host = creds.client_id 
        self.port = creds.client_secret 
        self.user = creds.username
        self.password = creds.tenant_id
        self.plantilla = plantilla

    def validar_email(self, email: str) -> bool:
        """Valida sintaxis de email"""
        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(patron, email) is not None

    async def send(self, req: EmailRequest) -> dict:
        """Envía correo usando SMTP y registra log"""
        async def build_and_send():
            try:
                # Construcción del correo
                msg = MIMEMultipart()
                msg["From"] = self.user
                msg["To"] = req.to
                msg["Subject"] = req.subject

                # Validación básica
                if not self.validar_email(req.to):
                    raise HTTPException(status_code=400, detail=f"Correo inválido en TO: {req.to}")

                if req.cc:
                    valid_cc = [c for c in req.cc if c and self.validar_email(c)]
                    msg["Cc"] = ", ".join(valid_cc)
                else:
                    valid_cc = []

                if req.bcc:
                    valid_bcc = [b for b in req.bcc if b and self.validar_email(b)]
                else:
                    valid_bcc = []

                # Renderizado de plantilla dinámica
                contenido_html = self.plantilla.content_html or req.body_html

                if isinstance(req.body_html, dict):
                    contenido_html = self.render_template(self.plantilla.content_html, req.body_html)

                msg.attach(MIMEText(contenido_html, "html", "utf-8"))
                
                
                FILES_SERVICE_URL = URL_API_STORAGE

                UPLOAD_DIR = Path("uploads/adjuntos")
                today_dir = UPLOAD_DIR / datetime.today().strftime("%Y-%m-%d")
                today_dir.mkdir(parents=True, exist_ok=True)

                adjuntos_guardados = []

                if req.adjuntos:
                    timeout = httpx.Timeout(30.0, connect=10.0)  # evita cierres abruptos
                    limits = httpx.Limits(max_keepalive_connections=0, max_connections=10)
                    try:
                        async with httpx.AsyncClient(verify=False, timeout=timeout, limits=limits) as client:
                            for adj in req.adjuntos:
                                # Leemos los bytes del archivo adjunto
                                file_bytes = await adj.read()

                                # Armamos el payload para el servicio externo
                                files = {
                                    "file": (adj.filename, file_bytes, adj.content_type),
                                    "container": (None, "files"),
                                }
                                

                                # Enviamos el archivo al servicio de almacenamiento externo
                                response = await client.post(
                                    FILES_SERVICE_URL,
                                    files=files,
                                    headers={"Authorization": f"Bearer {self.token}"} if self.token else {}
                                )

                                # Verificamos el resultado
                                if response.status_code not in (200, 201, 202):
                                    raise HTTPException(
                                        status_code=response.status_code,
                                        detail=f"Error al subir {adj.filename}: {response.text}",
                                    )


                                data = response.json()
                                ruta_remota = data.get("ruta")

                                # Guardamos la ruta remota si la hay
                                if ruta_remota:
                                    adjuntos_guardados.append(ruta_remota)

                                # Además, guardamos una copia local
                                destino = today_dir / adj.filename
                                with open(destino, "wb") as buffer:
                                    buffer.write(file_bytes)

                                # También registramos la ruta local
                                adjuntos_guardados.append(str(destino))
                            
                            # 📎 Adjuntar archivos locales al correo
                        for ruta in adjuntos_guardados:
                            ruta_path = Path(ruta)
                            if ruta_path.exists():
                                with open(ruta_path, "rb") as f:
                                    part = MIMEApplication(f.read(), Name=ruta_path.name)
                                part["Content-Disposition"] = f'attachment; filename="{ruta_path.name}"'
                                msg.attach(part)
                    except httpx.TransportError as e:
                        # Captura cualquier error SSL o conexión caída
                        raise HTTPException(
                            status_code=500,
                            detail=f"Error de conexión al subir archivos: {str(e)}"
                        )

                    finally:
                        #  Esperar pequeño retardo antes de cerrar el cliente HTTP
                        await asyncio.sleep(0.1)


                            
                            
                            

                # Envío SMTP
                with smtplib.SMTP(self.host, self.port) as server:
                    server.starttls()
                    server.login(self.user, self.password)
                    server.send_message(msg, from_addr=self.user, to_addrs=[req.to] + valid_cc + valid_bcc)

                # Log de éxito
                log = LogsEnvio(
                    destinatario=req.to,
                    cc=";".join(valid_cc) if valid_cc else None,
                    bcc=";".join(valid_bcc) if valid_bcc else None,
                    adjuntos=";".join(adjuntos_guardados) if adjuntos_guardados else None,
                    num_adjuntos=len(adjuntos_guardados),
                    asunto=req.subject,
                    contenido=contenido_html,
                    estado="ENVIADO",
                    fecha_envio=datetime.utcnow(),
                    identificador=req.identifying_name,
                    detalle="Correo enviado correctamente",
                )
                self.db.add(log)
                self.db.commit()

            except Exception as e:
                log = LogsEnvio(
                    destinatario=req.to,
                    asunto=req.subject,
                    contenido=str(req.body_html),
                    estado="ERROR",
                    fecha_envio=datetime.utcnow(),
                    identificador=req.identifying_name,
                    detalle=str(e),
                )
                self.db.add(log)
                self.db.commit()
                raise

        await build_and_send()
        return {"status": "Procesado", "to": req.to}

    def render_template(self, template: str, variables: dict) -> str:
        """Renderiza plantilla HTML reemplazando {{campo}} o {{etiqueta}}"""
        def dict_to_html(data: dict) -> str:
            html = "<ul>"
            for k, v in data.items():
                if isinstance(v, dict):
                    html += f"<li><strong>{k}:</strong> {dict_to_html(v)}</li>"
                else:
                    html += f"<li><strong>{k}:</strong> {v}</li>"
            html += "</ul>"
            return html

        def replace_var(match):
            expr = match.group(1).strip()
            if expr == "etiqueta":
                return dict_to_html(variables)
            return str(variables.get(expr, f"{{{{{expr}}}}}"))

        return re.sub(r"{{\s*(.*?)\s*}}", replace_var, template)

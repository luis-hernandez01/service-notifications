import json
from typing import List, Optional
from fastapi import File, Form, UploadFile

class EmailRequest:
    def __init__(
        self,
        identifying_name: str = Form(..., description="Identificador de plantilla"),
        to: str = Form(..., description="Destinatario principal"),
        subject: str = Form(..., description="Asunto del correo"),
        body_html: str = Form(..., description="Cuerpo del correo (JSON string)"),
        cc: Optional[List[str]] = Form(None, description="Lista de correos en copia"),
        bcc: Optional[List[str]] = Form(
            None, description="Lista de correos en copia oculta"
        ),
        # Adjuntos (archivos normales)
        adjuntos: Optional[List[UploadFile]] = File(None),
        # Imágenes embebidas (archivos que se referencian con cid)
        # imagenes_embed: Optional[List[UploadFile]] = File(None),
    ):
        self.identifying_name = identifying_name
        self.to = to
        self.subject = subject
        # body_html viene como string JSON → lo convertimos a dict
        try:
            self.body_html = json.loads(body_html)
        except Exception:
            self.body_html = {"raw": body_html}  # fallback si no es JSON válido
        self.cc = cc or []
        self.bcc = bcc or []
        self.adjuntos = adjuntos or []
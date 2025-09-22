from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict


class EmailRequest(BaseModel):
#    DTO para la petición de envío de correo.
#     Compatible con FastAPI y validación automática de Pydantic.

    subject: str = Field(..., description="Asunto del correo")
    body_html: str = Field(..., description="Cuerpo del correo en formato HTML")
    to: EmailStr = Field(..., description="Destinatario principal del correo")
    identifying_name: str = Field(..., description="Identificador de plantillas")
    cc: Optional[List[EmailStr]] = Field(
        default=None, description="Lista de destinatarios en copia"
    )
    bcc: Optional[List[EmailStr]] = Field(
        default=None, description="Lista de destinatarios en copia oculta"
    )
    adjuntos: Optional[List[str]] = Field(
        default=None,
        description="Lista de rutas absolutas o relativas de archivos adjuntos",
        example=["/path/to/file.pdf", "docs/manual.docx"],
    )
    imagenes_embed: Optional[Dict[str, str]] = Field(
        default=None,
        description="Diccionario con imágenes a embeber en el cuerpo del correo. "
                    "Clave = Content-ID (cid), Valor = ruta al archivo de imagen.",
        example={"logo123": "static/images/logo.png"},
    )

    class Config:
        json_schema_extra = {
            "example": {
                "identifying_name": "plantilla-notificacion",
                "subject": "Prueba de correo",
                "body_html": "<h1>Hola</h1><p>Este es un correo de prueba con imagen embedida: <img src='cid:logo123'></p>",
                "to": "usuario@dominio.com",
                "cc": ["otro@dominio.com"],
                "bcc": ["oculto@dominio.com"],
                "adjuntos": ["archivos/reporte.pdf"],
                "imagenes_embed": {"logo123": "static/images/logo.png"}
            }
        }


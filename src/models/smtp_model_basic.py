from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class EmailRequest(BaseModel):
    #    DTO para la petición de envío de correo.
    #     Compatible con FastAPI y validación automática de Pydantic.
    subject: str = Field(..., description="Asunto del correo")
    body_html: Optional[Dict[str, str]] = Field(
        ..., description="Cuerpo del correo en formato HTML"
    )
    to: str = Field(..., description="Destinatario principal del correo")
    identifying_name: str = Field(..., description="Identificador de plantillas")
    cc: Optional[List[str]] = Field(
        default=None, description="Lista de destinatarios en copia"
    )
    bcc: Optional[List[str]] = Field(
        default=None, description="Lista de destinatarios en copia oculta"
    )
    adjuntos: Optional[List[str]] = Field(
        default=None,
        description="Lista de rutas absolutas o relativas de archivos adjuntos",
        json_schema_extra={"logo123": "static/images/logo.png"},
    )
    imagenes_embed: Optional[Dict[str, str]] = Field(
        default=None,
        description="Diccionario con imágenes a embeber en el cuerpo del correo."
        "Clave = Content-ID (cid), Valor = ruta al archivo de imagen.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "identifying_name": "plantilla-notificacion",
                "subject": "Prueba de correo",
                "body_html": {
                    "titulo": "Hola",
                    "usuario": "Juan",
                    "mensaje": "Este es un correo de prueba con parámetros dinámicos",
                    "imagen": "cid:logo123",
                    "otp": "1234",
                    "enlace_recuperacion": "https://www.invias.gov.co/",
                },
                "to": "usuario@dominio.com",
                "cc": ["otro@dominio.com"],
                "bcc": ["oculto@dominio.com"],
            }
        }
    )

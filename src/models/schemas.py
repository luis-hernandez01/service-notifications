"""
Modelos de datos y esquemas Pydantic.

@autor: Fabio Garcia
@fecha: Septiembre 2025
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class FileInfo(BaseModel):
    """
    Modelo para la información de un archivo almacenado en Azure Storage.
    
    Attributes:
        name: Nombre del archivo
        size: Tamaño del archivo en bytes
        content_type: Tipo de contenido MIME del archivo
        url: URL para acceder al archivo
        created_on: Fecha y hora de creación del archivo
    """
    name: str
    size: int
    content_type: str
    url: str
    created_on: str

class FileUploadResponse(BaseModel):
    """
    Respuesta para la operación de carga de archivos.
    
    Attributes:
        file_name: Nombre del archivo cargado
        file_size: Tamaño del archivo en bytes
        content_type: Tipo de contenido MIME del archivo
        url: URL para acceder al archivo
    """
    file_name: str
    file_size: int
    content_type: str
    url: str

class FileListResponse(BaseModel):
    """
    Respuesta para la operación de listado de archivos.
    
    Attributes:
        files: Lista de archivos disponibles
        count: Número total de archivos
    """
    files: List[FileInfo]
    count: int = Field(..., description="Número total de archivos")

class ErrorResponse(BaseModel):
    """
    Modelo para respuestas de error.
    
    Attributes:
        error: Mensaje de error
        detail: Detalles adicionales sobre el error (opcional)
    """
    error: str
    detail: Optional[str] = None


class SuccessResponse(BaseModel):
    """
    Modelo para respuestas exitosas.
    
    Attributes:
        message: Mensaje de éxito
        data: Datos adicionales sobre la respuesta (opcional)
    """
    message: str
    data: Optional[dict] = None


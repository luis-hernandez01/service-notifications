"""
Endpoints para la gestión de archivos en Azure Storage.

@autor: Fabio Garcia
@fecha: Septiembre 2025
"""
from typing import Optional
import os
import tempfile
import aiofiles
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from starlette import status

from ...models.schemas import FileUploadResponse, FileListResponse, ErrorResponse, SuccessResponse
from ...services.storage_service import StorageService
from ...utils.exceptions import StorageError

from src.security.auth import verify_jwt_token

router = APIRouter()

@router.post(
    "/upload",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Error en la solicitud"},
        403: {"model": ErrorResponse, "description": "API Key inválida o no proporcionada"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def upload_file(
    api_key: str = Depends(verify_jwt_token),
    file: UploadFile = File(..., description="Archivo a cargar"),
    container: str = Form("files", description="Nombre del contenedor en Azure Storage")
):
    """
    Carga un archivo a Azure Storage.
    
    Args:
        file: Archivo a cargar
        container: Nombre del contenedor en Azure Storage (por defecto "files")
        api_key: API Key para autenticación (proporcionada en el header X-API-Key)
        
    Returns:
        FileUploadResponse: Información del archivo cargado
    """
    try:
        # Verificar que se ha proporcionado un archivo
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se ha proporcionado ningún archivo"
            )
        
        # Obtener el contenido del archivo
        content = await file.read()
        
        # Cargar el archivo a Azure Storage
        result = await StorageService.upload_file(
            content,
            file.filename,
            file.content_type or "application/octet-stream",
            container
        )
        
        return result
        
    except StorageError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )

@router.get(
    "/download/{container}/{file_name}",
    responses={
        403: {"model": ErrorResponse, "description": "API Key inválida o no proporcionada"},
        404: {"model": ErrorResponse, "description": "Archivo no encontrado"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def download_file(container: str, 
                        file_name: str,
                        api_key: str = Depends(verify_jwt_token)
                        ):
    """
    Descarga un archivo desde Azure Storage.
    
    Args:
        file_name: Nombre del archivo a descargar
        container: Nombre del contenedor en Azure Storage
        api_key: API Key para autenticación (proporcionada en el header X-API-Key)
        
    Returns:
        StreamingResponse: Stream del contenido del archivo
    """
    try:
        # Descargar el archivo desde Azure Storage
        download_stream, content_type, size = await StorageService.download_file(file_name, container)

        # Crear respuesta de streaming
        return StreamingResponse(
            download_stream.chunks(),
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={file_name}",
                "Content-Length": str(size)
            }
        )
        
    except StorageError as e:
        if "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )

@router.get(
    "/list",
    response_model=FileListResponse,
    responses={
        403: {"model": ErrorResponse, "description": "API Key inválida o no proporcionada"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def list_files(
    prefix: Optional[str] = Query(None, description="Prefijo para filtrar archivos"),
    container: str = Query("files", description="Nombre del contenedor en Azure Storage"),
    api_key: str = Depends(verify_jwt_token)
):
    """
    Lista los archivos disponibles en Azure Storage.
    
    Args:
        prefix: Prefijo opcional para filtrar archivos
        container: Nombre del contenedor en Azure Storage   
        api_key: API Key para autenticación (proporcionada en el header X-API-Key)
        
    Returns:
        FileListResponse: Lista de archivos disponibles
    """
    try:
        # Listar archivos desde Azure Storage
        files = await StorageService.list_files(prefix, container)
        
        # Crear respuesta
        return FileListResponse(
            files=files,
            count=len(files)
        )
        
    except StorageError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )

@router.delete(
    "/{container}/{file_name}",
    response_model=SuccessResponse,
    responses={
        403: {"model": ErrorResponse, "description": "API Key inválida o no proporcionada"},
        404: {"model": ErrorResponse, "description": "Archivo no encontrado"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def delete_file(container: str, 
                    file_name: str,
                    api_key: str = Depends(verify_jwt_token)
                    ):
    """
    Elimina un archivo de Azure Storage.
    
    Args:
        file_name: Nombre del archivo a eliminar
        container: Nombre del contenedor en Azure Storage   
        api_key: API Key para autenticación (proporcionada en el header X-API-Key)
        
    Returns:
        None
    """
    try:
        # Eliminar el archivo de Azure Storage
        result = await StorageService.delete_file(file_name, container)
        return result
        
    except StorageError as e:
        if "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )


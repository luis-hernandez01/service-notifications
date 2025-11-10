"""
Servicio para gestionar operaciones con Azure Blob Storage.

@autor: Fabio Garcia
@fecha: Septiembre 2025
"""
from typing import List, Optional, BinaryIO
import aiofiles
import os
import uuid
from datetime import datetime
from azure.storage.blob.aio import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError

from ..config.azure_config import AzureStorageConfig
from ..config.settings import settings
from ..models.schemas import FileInfo, FileUploadResponse, SuccessResponse
from ..utils.exceptions import StorageError

class StorageService:
    """
    Servicio para gestionar operaciones con Azure Blob Storage.
    
    Este servicio proporciona métodos asíncronos para cargar, descargar,
    listar y eliminar archivos en Azure Blob Storage.
    """
    
    @staticmethod
    async def upload_file(file_content: BinaryIO, file_name: str, content_type: str, container: str = None) -> FileUploadResponse:
        """
        Carga un archivo a Azure Blob Storage.
        
        Args:
            file_content: Contenido del archivo a cargar
            file_name: Nombre del archivo
            content_type: Tipo de contenido MIME del archivo
            container: Nombre del contenedor donde se cargará el archivo
            
        Returns:
            FileUploadResponse: Información del archivo cargado
            
        Raises:
            StorageError: Si ocurre un error durante la carga
        """
        try:
            # Asegurar que el contenedor existe
            container_name = await AzureStorageConfig.ensure_container_exists(container)
            if not container_name:
                raise StorageError("El contenedor especificado no existe o no se pudo crear.")
            
            # Generar un nombre único para evitar colisiones
            unique_name = f"{uuid.uuid4().hex}_{file_name}"
            
            # Obtener cliente de servicio
            blob_service_client = await AzureStorageConfig.get_blob_service_client()
            
            # Obtener cliente de contenedor
            container_client = blob_service_client.get_container_client(container_name)
            
            # Obtener cliente de blob
            blob_client = container_client.get_blob_client(unique_name)
            
            # Cargar el archivo
            await blob_client.upload_blob(
                file_content,
                content_type=content_type,
                overwrite=True
            )
            
            # Obtener propiedades del blob
            properties = await blob_client.get_blob_properties()
            
            # Construir URL del blob
            blob_url = blob_client.url
            
            # Crear y devolver respuesta
            return FileUploadResponse(
                file_name=unique_name,
                file_size=properties.size,
                content_type=properties.content_settings.content_type,
                url=blob_url
            )
            
        except Exception as e:
            raise StorageError(f"Error al cargar el archivo: {str(e)}")
    
    @staticmethod
    async def download_file(file_name: str, container: str = None) -> tuple:
        """
        Descarga un archivo desde Azure Blob Storage.
        
        Args:
            file_name: Nombre del archivo a descargar
            
        Returns:
            tuple: (stream de datos, tipo de contenido, tamaño)
            
        Raises:
            StorageError: Si el archivo no existe o hay un error durante la descarga
        """
        try:
            # Obtener cliente de servicio
            blob_service_client = await AzureStorageConfig.get_blob_service_client()
            
            # Obtener cliente de contenedor
            container_name = container or settings.azure_storage_container_name
            container_client = blob_service_client.get_container_client(
                container_name
            )
            
            # Obtener cliente de blob
            blob_client = container_client.get_blob_client(file_name)
            
            # Verificar si el blob existe
            if not await blob_client.exists():
                raise StorageError(f"El archivo \'{file_name}\' no existe")
            
            # Obtener propiedades del blob
            properties = await blob_client.get_blob_properties()
            
            # Descargar el blob
            download_stream = await blob_client.download_blob()
            
            # Devolver stream, tipo de contenido y tamaño
            return (
                download_stream,
                properties.content_settings.content_type,
                properties.size
            )
            
        except ResourceNotFoundError:
            raise StorageError(f"El archivo \'{file_name}\' no existe")
        except Exception as e:
            raise StorageError(f"Error al descargar el archivo: {str(e)}")
    
    @staticmethod
    async def list_files(prefix: Optional[str] = None, container: str = None) -> List[FileInfo]:
        """
        Lista los archivos disponibles en Azure Blob Storage.
        
        Args:
            prefix: Prefijo opcional para filtrar archivos
            
        Returns:
            List[FileInfo]: Lista de información de archivos
            
        Raises:
            StorageError: Si ocurre un error durante el listado
        """
        try:
            # Obtener cliente de servicio
            blob_service_client = await AzureStorageConfig.get_blob_service_client()
            
            # Obtener cliente de contenedor
            container_name = container or settings.azure_storage_container_name
            container_client = blob_service_client.get_container_client(
                container_name
            )
            
            # Listar blobs
            blob_list = []
            async for blob in container_client.list_blobs(name_starts_with=prefix):
                # Obtener cliente de blob para construir URL
                blob_client = container_client.get_blob_client(blob.name)
                
                # Crear objeto FileInfo
                blob_list.append(FileInfo(
                    name=blob.name,
                    size=blob.size,
                    content_type=blob.content_settings.content_type or "application/octet-stream",
                    url=blob_client.url,
                    created_on=blob.creation_time.isoformat() if blob.creation_time else datetime.now().isoformat()
                ))
            
            return blob_list
            
        except Exception as e:
            raise StorageError(f"Error al listar archivos: {str(e)}")
    
    @staticmethod
    async def delete_file(file_name: str, container: str = None) -> SuccessResponse:
        """
        Elimina un archivo de Azure Blob Storage.
        
        Args:
            file_name: Nombre del archivo a eliminar
            container: Nombre del contenedor en Azure Storage (por defecto "files")

        Returns:
            SuccessResponse: Respuesta de éxito

        Raises:
            StorageError: Si el archivo no existe o hay un error durante la eliminación
        """
        try:
            # Obtener cliente de servicio
            blob_service_client = await AzureStorageConfig.get_blob_service_client()
            
            # Obtener cliente de contenedor
            container_name = container or settings.azure_storage_container_name
            container_client = blob_service_client.get_container_client(
                container_name
            )
            
            # Obtener cliente de blob
            blob_client = container_client.get_blob_client(file_name)
            
            # Verificar si el blob existe
            if not await blob_client.exists():
                raise StorageError(f"El archivo \'{file_name}\' no existe")
            
            # Eliminar el blob
            await blob_client.delete_blob()
            
            #Crear y devolver respuesta
            return SuccessResponse(
                message="Archivo eliminado exitosamente",
                data={
                    "file_name": file_name,
                    "container": container_name
                }
            )

        except ResourceNotFoundError:
            raise StorageError(f"El archivo \'{file_name}\' no existe")
        except Exception as e:
            raise StorageError(f"Error al eliminar el archivo: {str(e)}")


"""
Configuración para la conexión con Azure Blob Storage.

@autor: Fabio Garcia
@fecha: Septiembre 2025
"""
from azure.storage.blob.aio import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from ..config.settings import settings

class AzureStorageConfig:
    """
    Configuración para la conexión con Azure Blob Storage.
    
    Esta clase proporciona métodos para crear clientes de Azure Storage
    y gestionar la conexión con el servicio.
    """
    
    @staticmethod
    async def get_blob_service_client():
        """
        Crea y devuelve un cliente asíncrono para Azure Blob Storage.
        
        Returns:
            BlobServiceClient: Cliente asíncrono para Azure Blob Storage.
        """
        # Priorizar el uso de connection string si está disponible
        if settings.azure_storage_connection_string:
            return BlobServiceClient.from_connection_string(
                settings.azure_storage_connection_string
            )
        
        # Alternativa: usar cuenta y clave
        elif settings.azure_storage_account_name and settings.azure_storage_account_key:
            account_url = f"https://{settings.azure_storage_account_name}.blob.core.windows.net"
            return BlobServiceClient(
                account_url=account_url,
                credential=settings.azure_storage_account_key
            )
        
        # Si no hay credenciales, lanzar excepción
        else:
            raise ValueError(
                "No se ha proporcionado configuración válida para Azure Storage. "
                "Debe configurar AZURE_STORAGE_CONNECTION_STRING o "
                "AZURE_STORAGE_ACCOUNT_NAME y AZURE_STORAGE_ACCOUNT_KEY."
            )
    
    @staticmethod
    async def ensure_container_exists(container_name=None):
        """
        Asegura que el contenedor especificado existe, creándolo si es necesario.
        
        Args:
            container_name (str, optional): Nombre del contenedor. 
                Si no se proporciona, se usa el valor por defecto de la configuración.
                
        Returns:
            str: Nombre del contenedor.
        """
        container_name = container_name or settings.azure_storage_container_name
        
        # Obtener cliente de servicio
        blob_service_client = await AzureStorageConfig.get_blob_service_client()
        
        # Obtener cliente de contenedor
        container_client = blob_service_client.get_container_client(container_name)
        
        try:
            # Intentar crear el contenedor si no existe
            await container_client.create_container()
        except ResourceExistsError:
            # El contenedor ya existe, lo cual está bien
            pass
        
        return container_name

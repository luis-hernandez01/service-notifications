"""
Configuración general de la aplicación.

@autor: Fabio Garcia
@fecha: Septiembre 2025
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuración general de la aplicación.
    
    Attributes:
        app_name: Nombre de la aplicación
        debug: Modo de depuración
        api_prefix: Prefijo para todas las rutas de la API
        api_key: Clave de API para autenticación
    """
    app_name: str = "Azure Storage App"
    debug: bool = False
    api_prefix: str = "/api"
    
    # Configuración de seguridad
    api_key: str = "123"
    
    # Configuración para Azure Storage
    azure_storage_connection_string: str = ""
    azure_storage_account_name: str = ""
    azure_storage_account_key: str = ""
    azure_storage_container_name: str = "files"
    
    # configuracion_bd
    postgres_host: str
    postgres_port: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    secret_key: str
    algorithm: str
    url_api_storage: str

    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_prefix = ""

# Instancia global de configuración
settings = Settings()


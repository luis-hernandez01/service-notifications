"""
Utilidades de autenticación.

@autor: Fabio Garcia
@fecha: Septiembre 2025
"""
from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from ..config.settings import settings

# Definir el header para la API Key
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    """
    Dependencia para validar la API Key en los headers de las peticiones.
    
    Args:
        api_key_header: Valor del header X-API-Key
        
    Returns:
        str: API Key validada
        
    Raises:
        HTTPException: Si la API Key no es válida o no está presente
    """
    # Verificar si la API Key está presente
    # y si coincide con la configurada en settings
    if not api_key_header:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="API Key no proporcionada. Incluya el header 'X-API-Key'."
        )
    
    if api_key_header != settings.api_key:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="API Key inválida"
        )
    
    return api_key_header


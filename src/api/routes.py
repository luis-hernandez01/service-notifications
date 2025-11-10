"""
Router principal de la API.

@autor: Fabio Garcia
@fecha: Septiembre 2025
"""
from fastapi import APIRouter
from .endpoints import files
from .endpoints import send_routes
from .endpoints import send_dinamyc_routes
from .endpoints import crud_templates_routes
from .endpoints import crud_credentials_routes


# Crear router principal
api_router = APIRouter()

# Incluir routers de endpoints
api_router.include_router(files.router, prefix="/v1/files", tags=["files"])

api_router.include_router(send_routes.router)
api_router.include_router(send_dinamyc_routes.router)

api_router.include_router(crud_templates_routes.router)
api_router.include_router(crud_credentials_routes.router)

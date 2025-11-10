"""
Punto de entrada de la aplicación FastAPI.

@autor: Fabio Garcia
@fecha: Septiembre 2025
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os

from scalar_fastapi import get_scalar_api_reference

from .config.settings import settings
from .api.routes import api_router
from .utils.exceptions import StorageError
from src.config.config import Base, engine

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API asíncrona para gestionar la descarga y carga de archivos a Azure Storage",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

for base, eng in zip(Base, engine):
    print(f"🛠️ Creando tablas en schema: {base.metadata.schema}")
    base.metadata.create_all(bind=eng)
    
# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router de API
app.include_router(api_router, prefix=settings.api_prefix)

# Manejador de excepciones personalizado
@app.exception_handler(StorageError)
async def storage_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)},
    )

# Ruta de salud
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

# Ruta para documentación con Scalar
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Azure Storage App - API Documentation",
        scalar_proxy_url="https://proxy.scalar.com",
    )

# Punto de entrada para ejecución directa
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=10000,
        reload=settings.debug
    )

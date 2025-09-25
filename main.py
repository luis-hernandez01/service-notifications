# Aplicación principal o de raiz del servicio de notificaciones.

# Este servicio expone el endpoint construidos con FastAPI.
# Incluyendo la configuración de CORS para permitir la comunicación con otras aplicaciones del front
# y el registro de rutas relacionadas con el envío de correos electrónicos.


# dependencias usadas para este archivo raiz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.send_routes import sendemail_routes
from src.routes.send_dinamyc_routes import send_router


from src.config.config import Base, engine

Base.metadata.create_all(bind=engine)

# Inicialización de la aplicación FastAPI
app = FastAPI(title="SMTP Service", version="1.0.0")

# from pathlib import Path

# Incorrecto:
# path = Path("file:///C:/Users/User/Pictures/Captura.PNG")

# Correcto:
# path = Path("C:/Users/User/Pictures/Captura.PNG")

# Verificar si existe
# print(path.exists())  # True si el archivo está allí



# configuracion de CORS
# permite que aplicaciones externas (por ejemplo, un frontend en Angular o React) 
# puedan comunicarse con esta API.
# CORS: ajusta a tus orígenes reales
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],        # Tdos los servicios que envien una peticion tendran permisos 
allow_credentials=True,     # Permitir envío de cookies/autenticación
allow_methods=["*"],        # se le esta dando permisos a todos los metodos existentes
allow_headers=["*"],           # Headers personalizados permitidos
)


# registrando mis rutas existentes para el envio de correos SMTP
# Aquí se incluyen las rutas definidas en la carpeta 'routes'.
app.include_router(sendemail_routes)
app.include_router(send_router)
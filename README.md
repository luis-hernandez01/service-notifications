# Azure Notification-services App
Aplicación en Python que permite administrar notificaciones (CRUD) almacenadas en una base de datos y enviar correos electrónicos a través del servicio de Microsoft O365. Las plantillas HTML se gestionan desde la base de datos y se utilizan para generar mensajes dinámicos y profesionales.

## Tecnologías utilizadas

- **FastAPI** – Framework moderno y rápido para APIs
- **SQLAlchemy** – ORM para gestión de modelos y relaciones
- **PostgreSQL** – Motor de base de datos
- **O365** – Servicio de envío de correos corporativos
- **Pydantic** – Validación de datos
- **Uvicorn** – Servidor ASGI para producción
- **Swagger UI** – Documentación interactiva automática

## Requisitos

- Python 3.7+
- Cuenta de Azure
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clone el repositorio:

```bash
git clone <url-del-repositorio>
cd services-notifications
```

2. Cree un entorno virtual e instale las dependencias:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure las variables de entorno:

Cree un archivo `.env` en la raíz del proyecto basado en `.env.example` y configure sus credenciales de Azure Storage:

```
# Crear archivo .env
# conexion a base datos postgres 
POSTGRES_HOST=localhost
POSTGRES_PORT=PORT
POSTGRES_DB=name_BD
POSTGRES_USER=name_user
POSTGRES_PASSWORD= PASS
```

## Ejecución

Para iniciar la aplicación en modo desarrollo:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en `http://localhost:8000` y la documentación en `http://localhost:8000/docs`.



## Uso de la API

La API requiere una `X-API-Key` en la cabecera de cada solicitud para la autenticación.


# Azure Storage App

Aplicación en Python con APIs asíncronas para gestionar la descarga y carga de archivos a Azure Storage.

## Características

- APIs asíncronas implementadas con FastAPI
- Operaciones completas para gestión de archivos en Azure Storage:
  - Carga de archivos
  - Descarga de archivos
  - Listado de archivos
  - Eliminación de archivos
- Arquitectura modular y escalable
- Documentación completa de la API con Swagger/OpenAPI
- Manejo de errores robusto

## Requisitos

- Python 3.7+
- Cuenta de Azure Storage
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clone el repositorio:

```bash
git clone <url-del-repositorio>
cd azure_storage_app
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
AZURE_STORAGE_CONNECTION_STRING=su_connection_string
# O alternativamente:
AZURE_STORAGE_ACCOUNT_NAME=su_account_name
AZURE_STORAGE_ACCOUNT_KEY=su_account_key
AZURE_STORAGE_CONTAINER_NAME=su_container_name
```

## Ejecución

Para iniciar la aplicación en modo desarrollo:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en `http://localhost:8000` y la documentación en `http://localhost:8000/docs`.

## Estructura del Proyecto

```
/home/ubuntu/azure_storage_project/
|-- .deployment
|-- .deploymentignore
|-- .env
|-- .env.example
|-- .gitignore
|-- README.md
|-- docs/
|   |-- api.md
|   |-- arquitectura.md
|   |-- documentacion.py
|   |-- Documentacion_Azure_Storage_App.docx
|   |-- guia_usuario.md
|   `-- requerimientos.md
|-- requirements.txt
|-- src/
|   |-- __init__.py
|   |-- api/
|   |   |-- __init__.py
|   |   |-- endpoints/
|   |   |   |-- __init__.py
|   |   |   `-- files.py
|   |   `-- routes.py
|   |-- config/
|   |   |-- __init__.py
|   |   |-- azure_config.py
|   |   `-- settings.py
|   |-- main.py
|   |-- models/
|   |   |-- __init__.py
|   |   `-- schemas.py
|   |-- services/
|   |   |-- __init__.py
|   |   `-- storage_service.py
|   `-- utils/
|       |-- __init__.py
|       |-- auth.py
|       `-- exceptions.py
|-- tests/
`-- todo.md
```

## Uso de la API

La API requiere una `X-API-Key` en la cabecera de cada solicitud para la autenticación.

### Endpoints

#### Archivos

- **`POST /api/v1/files/upload`**: Carga un archivo.
  - **Parámetros de formulario**: `file` (el archivo a cargar), `container` (opcional, nombre del contenedor).
  - **Respuesta exitosa (201)**: `FileUploadResponse` con información del archivo cargado.

- **`GET /api/v1/files/download/{container}/{file_name}`**: Descarga un archivo.
  - **Parámetros de ruta**: `container` (nombre del contenedor), `file_name` (nombre del archivo).
  - **Respuesta exitosa (200)**: El contenido del archivo como `StreamingResponse`.

- **`GET /api/v1/files/list`**: Lista los archivos en un contenedor.
  - **Parámetros de consulta**: `prefix` (opcional, para filtrar por prefijo), `container` (opcional, nombre del contenedor).
  - **Respuesta exitosa (200)**: `FileListResponse` con la lista de archivos.

- **`DELETE /api/v1/files/{container}/{file_name}`**: Elimina un archivo.
  - **Parámetros de ruta**: `container` (nombre del contenedor), `file_name` (nombre del archivo).
  - **Respuesta exitosa (200)**: `SuccessResponse` con un mensaje de confirmación.

### Salud

- **`GET /health`**: Verifica el estado de la aplicación.
  - **Respuesta exitosa (200)**: `{"status": "ok"}`.

## Documentación

La documentación de la API está disponible en los siguientes endpoints:

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **Scalar**: `/scalar`

Para más detalles, consulte la documentación completa en la carpeta `docs/`:

- [Diseño de Arquitectura](docs/arquitectura.md)
- [Documentación de la API](docs/api.md)
- [Guía de Usuario](docs/guia_usuario.md)

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.


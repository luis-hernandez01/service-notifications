# Guía de Usuario - Azure Storage App

Esta guía proporciona instrucciones detalladas para instalar, configurar y utilizar la aplicación Azure Storage App para gestionar archivos en Azure Storage.

## Índice

1. [Instalación](#instalación)
2. [Configuración](#configuración)
3. [Ejecución](#ejecución)
4. [Uso de la API](#uso-de-la-api)
5. [Ejemplos prácticos](#ejemplos-prácticos)
6. [Solución de problemas](#solución-de-problemas)

## Instalación

### Requisitos previos

Antes de comenzar, asegúrese de tener instalado:

- Python 3.7 o superior
- pip (gestor de paquetes de Python)
- Una cuenta de Azure con servicio de Azure Storage

### Pasos de instalación

1. Clone o descargue el repositorio:

```bash
git clone <url-del-repositorio>
cd azure_storage_app
```

2. Cree un entorno virtual para aislar las dependencias:

```bash
# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

3. Instale las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

### Configuración de Azure Storage

Para utilizar la aplicación, necesita configurar sus credenciales de Azure Storage. Tiene dos opciones:

#### Opción 1: Connection String

1. En el portal de Azure, vaya a su cuenta de Storage
2. En la sección "Configuración", seleccione "Claves de acceso"
3. Copie el valor de "Connection string"

#### Opción 2: Nombre de cuenta y clave

1. En el portal de Azure, vaya a su cuenta de Storage
2. En la sección "Configuración", seleccione "Claves de acceso"
3. Copie el nombre de la cuenta y una de las claves

### Configuración de la aplicación

1. Cree un archivo `.env` en la raíz del proyecto basado en el archivo `.env.example`:

```bash
cp .env.example .env
```

2. Edite el archivo `.env` con sus credenciales:

```
# Opción 1: Connection String
AZURE_STORAGE_CONNECTION_STRING=su_connection_string

# O Opción 2: Nombre de cuenta y clave
AZURE_STORAGE_ACCOUNT_NAME=su_account_name
AZURE_STORAGE_ACCOUNT_KEY=su_account_key

# Nombre del contenedor (por defecto: "files")
AZURE_STORAGE_CONTAINER_NAME=su_container_name
```

## Ejecución

### Iniciar la aplicación

Para iniciar la aplicación en modo desarrollo:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Para iniciar la aplicación en modo producción:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Verificar que la aplicación está funcionando

Abra un navegador y vaya a:

- Documentación de la API: `http://localhost:8000/docs`
- Verificación de salud: `http://localhost:8000/health`

## Uso de la API

La API proporciona endpoints para gestionar archivos en Azure Storage:

### Carga de archivos

Para cargar un archivo a Azure Storage:

1. Vaya a `http://localhost:8000/docs` en su navegador
2. Expanda el endpoint `POST /api/files/upload`
3. Haga clic en "Try it out"
4. Seleccione un archivo usando el botón "Choose File"
5. Haga clic en "Execute"

Alternativamente, puede usar cURL:

```bash
curl -X POST "http://localhost:8000/api/files/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/ruta/al/archivo.pdf"
```

### Listado de archivos

Para listar los archivos disponibles:

1. Vaya a `http://localhost:8000/docs` en su navegador
2. Expanda el endpoint `GET /api/files/list`
3. Haga clic en "Try it out"
4. Opcionalmente, especifique un prefijo para filtrar archivos
5. Haga clic en "Execute"

Alternativamente, puede usar cURL:

```bash
curl -X GET "http://localhost:8000/api/files/list" \
  -H "accept: application/json"
```

### Descarga de archivos

Para descargar un archivo:

1. Vaya a `http://localhost:8000/docs` en su navegador
2. Expanda el endpoint `GET /api/files/download/{file_name}`
3. Haga clic en "Try it out"
4. Introduzca el nombre del archivo a descargar
5. Haga clic en "Execute"

Alternativamente, puede usar cURL:

```bash
curl -X GET "http://localhost:8000/api/files/download/nombre_archivo.pdf" \
  -H "accept: application/octet-stream" \
  --output archivo_descargado.pdf
```

### Eliminación de archivos

Para eliminar un archivo:

1. Vaya a `http://localhost:8000/docs` en su navegador
2. Expanda el endpoint `DELETE /api/files/{file_name}`
3. Haga clic en "Try it out"
4. Introduzca el nombre del archivo a eliminar
5. Haga clic en "Execute"

Alternativamente, puede usar cURL:

```bash
curl -X DELETE "http://localhost:8000/api/files/nombre_archivo.pdf" \
  -H "accept: application/json"
```

## Ejemplos prácticos

### Ejemplo 1: Carga y descarga de un archivo

```bash
# Cargar un archivo
curl -X POST "http://localhost:8000/api/files/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/ruta/al/documento.pdf"

# La respuesta incluirá el nombre del archivo en Azure Storage, por ejemplo:
# {"file_name":"a1b2c3d4_documento.pdf","file_size":12345,"content_type":"application/pdf","url":"https://..."}

# Descargar el archivo usando el nombre devuelto
curl -X GET "http://localhost:8000/api/files/download/a1b2c3d4_documento.pdf" \
  -H "accept: application/octet-stream" \
  --output documento_descargado.pdf
```

### Ejemplo 2: Listar y eliminar archivos

```bash
# Listar todos los archivos
curl -X GET "http://localhost:8000/api/files/list" \
  -H "accept: application/json"

# Listar archivos con un prefijo específico
curl -X GET "http://localhost:8000/api/files/list?prefix=documento" \
  -H "accept: application/json"

# Eliminar un archivo específico
curl -X DELETE "http://localhost:8000/api/files/a1b2c3d4_documento.pdf" \
  -H "accept: application/json"
```

## Solución de problemas

### Problemas comunes

1. **Error de conexión a Azure Storage**:
   - Verifique que las credenciales en el archivo `.env` sean correctas
   - Asegúrese de que su cuenta de Azure Storage esté activa
   - Compruebe que tiene permisos suficientes para las operaciones

2. **Error al iniciar la aplicación**:
   - Verifique que todas las dependencias estén instaladas: `pip install -r requirements.txt`
   - Asegúrese de que el puerto 8000 no esté en uso por otra aplicación

3. **Error al cargar archivos grandes**:
   - La API tiene un límite de tamaño para la carga de archivos
   - Para archivos muy grandes, considere dividirlos o ajustar la configuración de FastAPI

### Logs y depuración

Para obtener más información sobre los errores, puede iniciar la aplicación en modo debug:

```bash
# Edite el archivo .env y establezca:
# DEBUG=True

# Luego inicie la aplicación:
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Contacto y soporte

Si encuentra problemas que no puede resolver, por favor contacte al equipo de soporte o abra un issue en el repositorio del proyecto.

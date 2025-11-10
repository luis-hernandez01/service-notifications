# Documentación de la API - Azure Storage App

Esta documentación describe los endpoints disponibles en la API de Azure Storage App, sus parámetros y respuestas.

## Base URL

```
http://localhost:8000/api
```

## Endpoints

### Carga de Archivos

**Endpoint:** `POST /files/upload`

**Descripción:** Carga un archivo a Azure Storage.

**Parámetros:**
- `file` (form-data): Archivo a cargar

**Respuesta exitosa (201 Created):**
```json
{
  "file_name": "a1b2c3d4_ejemplo.pdf",
  "file_size": 12345,
  "content_type": "application/pdf",
  "url": "https://cuenta.blob.core.windows.net/contenedor/a1b2c3d4_ejemplo.pdf"
}
```

**Errores posibles:**
- `400 Bad Request`: No se ha proporcionado ningún archivo
- `500 Internal Server Error`: Error al cargar el archivo

### Descarga de Archivos

**Endpoint:** `GET /files/download/{file_name}`

**Descripción:** Descarga un archivo desde Azure Storage.

**Parámetros:**
- `file_name` (path): Nombre del archivo a descargar

**Respuesta exitosa:**
- Stream del contenido del archivo con los headers adecuados para descarga

**Errores posibles:**
- `404 Not Found`: El archivo no existe
- `500 Internal Server Error`: Error al descargar el archivo

### Listado de Archivos

**Endpoint:** `GET /files/list`

**Descripción:** Lista los archivos disponibles en Azure Storage.

**Parámetros:**
- `prefix` (query, opcional): Prefijo para filtrar archivos

**Respuesta exitosa:**
```json
{
  "files": [
    {
      "name": "ejemplo1.pdf",
      "size": 12345,
      "content_type": "application/pdf",
      "url": "https://cuenta.blob.core.windows.net/contenedor/ejemplo1.pdf",
      "created_on": "2025-05-26T12:30:45.123456"
    },
    {
      "name": "ejemplo2.jpg",
      "size": 67890,
      "content_type": "image/jpeg",
      "url": "https://cuenta.blob.core.windows.net/contenedor/ejemplo2.jpg",
      "created_on": "2025-05-26T12:35:12.654321"
    }
  ],
  "count": 2
}
```

**Errores posibles:**
- `500 Internal Server Error`: Error al listar archivos

### Eliminación de Archivos

**Endpoint:** `DELETE /files/{file_name}`

**Descripción:** Elimina un archivo de Azure Storage.

**Parámetros:**
- `file_name` (path): Nombre del archivo a eliminar

**Respuesta exitosa (204 No Content):**
- Sin contenido

**Errores posibles:**
- `404 Not Found`: El archivo no existe
- `500 Internal Server Error`: Error al eliminar el archivo

## Verificación de Salud

**Endpoint:** `GET /health`

**Descripción:** Verifica el estado de la aplicación.

**Respuesta exitosa:**
```json
{
  "status": "ok"
}
```

## Códigos de Error

La API utiliza los siguientes códigos de estado HTTP:

- `200 OK`: La solicitud se ha completado correctamente
- `201 Created`: El recurso se ha creado correctamente
- `204 No Content`: La solicitud se ha completado correctamente, pero no hay contenido para devolver
- `400 Bad Request`: La solicitud es incorrecta o malformada
- `404 Not Found`: El recurso solicitado no existe
- `500 Internal Server Error`: Error interno del servidor

## Formato de Respuesta de Error

Todas las respuestas de error siguen el siguiente formato:

```json
{
  "error": "Mensaje de error",
  "detail": "Detalles adicionales (opcional)"
}
```

## Ejemplos de Uso con cURL

### Carga de Archivos

```bash
curl -X POST "http://localhost:8000/api/files/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/ruta/al/archivo.pdf"
```

### Descarga de Archivos

```bash
curl -X GET "http://localhost:8000/api/files/download/nombre_archivo.pdf" \
  -H "accept: application/octet-stream" \
  --output archivo_descargado.pdf
```

### Listado de Archivos

```bash
curl -X GET "http://localhost:8000/api/files/list" \
  -H "accept: application/json"
```

### Eliminación de Archivos

```bash
curl -X DELETE "http://localhost:8000/api/files/nombre_archivo.pdf" \
  -H "accept: application/json"
```

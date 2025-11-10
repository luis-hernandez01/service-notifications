# Diseño de Arquitectura - Aplicación de Azure Storage

## Estructura del Proyecto

```
azure_storage_app/
│
├── src/                          # Código fuente de la aplicación
│   ├── __init__.py               # Inicializador del paquete
│   ├── main.py                   # Punto de entrada de la aplicación
│   ├── config/                   # Configuración de la aplicación
│   │   ├── __init__.py
│   │   ├── settings.py           # Configuración general y variables de entorno
│   │   └── azure_config.py       # Configuración específica de Azure Storage
│   │
│   ├── models/                   # Modelos de datos y esquemas
│   │   ├── __init__.py
│   │   └── schemas.py            # Esquemas Pydantic para validación de datos
│   │
│   ├── services/                 # Servicios de negocio
│   │   ├── __init__.py
│   │   └── storage_service.py    # Servicio para operaciones con Azure Storage
│   │
│   ├── api/                      # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── routes.py             # Registro de rutas
│   │   └── endpoints/            # Endpoints específicos
│   │       ├── __init__.py
│   │       └── files.py          # Endpoints para gestión de archivos
│   │
│   └── utils/                    # Utilidades y helpers
│       ├── __init__.py
│       ├── exceptions.py         # Excepciones personalizadas
│       └── helpers.py            # Funciones auxiliares
│
├── tests/                        # Pruebas unitarias y de integración
│   ├── __init__.py
│   ├── test_api.py               # Pruebas para la API
│   └── test_services.py          # Pruebas para los servicios
│
├── docs/                         # Documentación
│   ├── requerimientos.md         # Análisis de requerimientos
│   ├── arquitectura.md           # Diseño de arquitectura (este archivo)
│   ├── api.md                    # Documentación de la API
│   └── guia_usuario.md           # Guía de usuario
│
├── .env.example                  # Ejemplo de variables de entorno
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Documentación principal
```

## Descripción de Componentes

### 1. Configuración (`src/config/`)

- **settings.py**: Gestiona la configuración general de la aplicación, carga variables de entorno y define parámetros globales.
- **azure_config.py**: Contiene la configuración específica para Azure Storage, incluyendo la inicialización de clientes y la gestión de credenciales.

### 2. Modelos (`src/models/`)

- **schemas.py**: Define los esquemas Pydantic para validación de datos de entrada y salida, asegurando la integridad de los datos en la API.

### 3. Servicios (`src/services/`)

- **storage_service.py**: Implementa la lógica de negocio para interactuar con Azure Storage, encapsulando las operaciones de carga, descarga, listado y eliminación de archivos.

### 4. API (`src/api/`)

- **routes.py**: Registra y configura las rutas de la API.
- **endpoints/files.py**: Implementa los endpoints específicos para la gestión de archivos, utilizando los servicios correspondientes.

### 5. Utilidades (`src/utils/`)

- **exceptions.py**: Define excepciones personalizadas para manejar errores específicos de la aplicación.
- **helpers.py**: Proporciona funciones auxiliares reutilizables en diferentes partes de la aplicación.

## Flujo de Datos

1. Las solicitudes HTTP llegan a los endpoints definidos en `api/endpoints/`.
2. Los endpoints validan los datos de entrada utilizando los esquemas de `models/`.
3. Los endpoints llaman a los métodos correspondientes en `services/`.
4. Los servicios utilizan la configuración de `config/` para conectarse a Azure Storage.
5. Los servicios realizan las operaciones solicitadas y devuelven los resultados.
6. Los endpoints transforman los resultados en respuestas HTTP adecuadas.

## Principios de Diseño

1. **Separación de Responsabilidades**: Cada componente tiene una responsabilidad única y bien definida.
2. **Inyección de Dependencias**: Los servicios reciben sus dependencias (como configuración) en lugar de crearlas internamente.
3. **Asincronía**: Todas las operaciones de E/S se implementan de forma asíncrona para maximizar el rendimiento.
4. **Manejo de Errores Centralizado**: Las excepciones se capturan y procesan de manera consistente en toda la aplicación.
5. **Configuración Externalizada**: Los parámetros de configuración se almacenan fuera del código para facilitar su gestión.

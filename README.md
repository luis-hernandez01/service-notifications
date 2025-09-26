# 📬 API de Notificaciones – FastAPI + O365

Esta API permite administrar notificaciones (CRUD) almacenadas en una base de datos y enviar correos electrónicos a través del servicio de Microsoft O365. Las plantillas HTML se gestionan desde la base de datos y se utilizan para generar mensajes dinámicos y profesionales.

---

## 🚀 Tecnologías utilizadas

- **FastAPI** – Framework moderno y rápido para APIs
- **SQLAlchemy** – ORM para gestión de modelos y relaciones
- **PostgreSQL** – Motor de base de datos
- **O365** – Servicio de envío de correos corporativos
- **Pydantic** – Validación de datos
- **Uvicorn** – Servidor ASGI para producción
- **Swagger UI** – Documentación interactiva automática

---

## Version de python y fastapi

PYTHON 3.13.7

# conexion a base datos postgres

POSTGRES_HOST=localhost
POSTGRES_PORT=PORT
POSTGRES_DB=name_BD
POSTGRES_USER=name_user
POSTGRES_PASSWORD= PASS

# configurar las variables de entorno

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=mi_correo@gmail.com
SMTP_PASS=mi_password
EMAIL_FROM=mi_correo@gmail.com

# parametros de conexion SMTP

# smtp.office365.com

SMTP_HOST=smtp.gmail.com
SMTP_PORT= PORT
SMTP_USER= mi_correo@gmail.com
SMTP_PASSWORD= PASS

# Crear entorno virtual

python -m venv venv
source venv/bin/activate # o venv\Scripts\activate en Windows

# Instalar dependencias

pip install -r requirements.txt

# Ejecutar el servidor

uvicorn app.main:app --reload

## En ejecucion

La API estará disponible en:

- Swagger UI → http://localhost:8000/docs#/
- ReDoc → http://localhost:8000/redoc#/

---

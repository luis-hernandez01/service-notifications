# service-notifications
Desarrollo de microservicios para notificaciones por medio sel servicio SMTP
realizado en la siguiente version de python y fastapi

PYTHON 3.13.7

configurar las variables de entorno
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=mi_correo@gmail.com
SMTP_PASS=mi_password
EMAIL_FROM=mi_correo@gmail.com


para inicializacion del proyecto ejecutar lo siguiente
uvicorn main:app --reload



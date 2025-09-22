# service-notifications
Desarrollo de microservicios para notificaciones por medio sel servicio SMTP Y O365
base de datos postgres
realizado en la siguiente version de python y fastapi 

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
# ejecutar instalacion de dependencias
pip install -r requirements.txt

# para inicializacion del proyecto ejecutar lo siguiente
uvicorn main:app --reload





# service-notifications
# service-notifications

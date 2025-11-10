# from datetime import datetime

# from sqlalchemy import Column, DateTime, Integer, String, Text

# from src.config.config import Base


# class LogsEnvio(Base):
#     __tablename__ = "logs_envio"

#     id = Column(Integer, primary_key=True, index=True)
#     destinatario = Column(String(255), nullable=False)
#     cc = Column(Text, nullable=True)
#     bcc = Column(Text, nullable=True)
#     adjuntos = Column(Text, nullable=True)  # lista de paths
#     num_adjuntos = Column(Integer, default=0)  # cantidad adjuntos
#     imagenes = Column(Text, nullable=True)  # lista de imágenes
#     num_imagenes = Column(Integer, default=0)  # cantidad imágenes
#     asunto = Column(String(500), nullable=True)
#     contenido = Column(Text, nullable=True)  # HTML del correo enviado
#     estado = Column(String(50), default="PENDIENTE")  # ENVIADO | ERROR
#     fecha_envio = Column(DateTime, default=datetime.utcnow)
#     identificador = Column(String(255), nullable=True)  # relación con la plantilla
#     detalle = Column(Text, nullable=True)  # error o confirmación










from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from src.config.config import Base


def crear_modelo_logs_envio(base):
    """
    Crea dinámicamente la tabla 'logs_envio'
    para el schema asociado a la Base recibida.
    """
    schema = base.metadata.schema  # obtiene el esquema actual

    class LogsEnvio(base):
        __tablename__ = "logs_envio"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del log de envío")
        destinatario = Column(String(255), nullable=False, comment="Correo del destinatario principal")
        cc = Column(Text, nullable=True, comment="Lista de correos en copia")
        bcc = Column(Text, nullable=True, comment="Lista de correos en copia oculta")
        adjuntos = Column(Text, nullable=True, comment="Lista de rutas de archivos adjuntos")
        num_adjuntos = Column(Integer, default=0, comment="Cantidad de adjuntos enviados")
        imagenes = Column(Text, nullable=True, comment="Lista de imágenes adjuntas")
        num_imagenes = Column(Integer, default=0, comment="Cantidad de imágenes adjuntas")
        asunto = Column(String(500), nullable=True, comment="Asunto del correo enviado")
        contenido = Column(Text, nullable=True, comment="Contenido HTML del correo enviado")
        estado = Column(String(50), default="PENDIENTE", comment="Estado del envío: PENDIENTE, ENVIADO o ERROR")
        fecha_envio = Column(DateTime, default=datetime.utcnow, comment="Fecha y hora del intento de envío")
        identificador = Column(String(255), nullable=True, comment="Identificador relacionado con la plantilla")
        detalle = Column(Text, nullable=True, comment="Mensaje de error o confirmación del envío")

    # Renombrar la clase según el schema
    LogsEnvio.__name__ = f"LogsEnvio_{schema}"
    return LogsEnvio


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
LogsEnvio = crear_modelo_logs_envio(Base[0])

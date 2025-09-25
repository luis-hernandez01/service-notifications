from sqlalchemy import Column, Integer, String, DateTime, Text
from src.config.config import Base
from datetime import datetime


class LogsEnvio(Base):
    __tablename__ = "logs_envio"

    id = Column(Integer, primary_key=True, index=True)
    destinatario = Column(String(255), nullable=False)
    cc = Column(Text, nullable=True)
    bcc = Column(Text, nullable=True)
    adjuntos = Column(Text, nullable=True)      # lista de paths
    num_adjuntos = Column(Integer, default=0)   # cantidad adjuntos
    imagenes = Column(Text, nullable=True)      # lista de imágenes
    num_imagenes = Column(Integer, default=0)   # cantidad imágenes
    asunto = Column(String(500), nullable=True)
    contenido = Column(Text, nullable=True)     # HTML del correo enviado
    estado = Column(String(50), default="PENDIENTE")  # ENVIADO | ERROR
    fecha_envio = Column(DateTime, default=datetime.utcnow)
    identificador = Column(String(255), nullable=True)  # relación con la plantilla
    detalle = Column(Text, nullable=True)  # error o confirmación
    

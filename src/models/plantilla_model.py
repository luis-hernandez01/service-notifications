from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from src.config.config import Base


class Plantillas(Base):
    __tablename__ = "plantillas"
    
    
    id = Column(Integer, primary_key=True, index=True)
    identifying_name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    content_html = Column(Text, nullable=False)
    activo = Column(Integer, default=1)   # 1 es activo 2 inactivo
    # Relación con credenciales
    credenciales_id = Column(Integer, ForeignKey("credenciales_correo.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación ORM
    credencial = relationship("CredencialesCorreo", backref="plantillas")
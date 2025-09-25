from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, func
from src.config.config import Base


class CredencialesCorreo(Base):
    __tablename__ = "credenciales_correo"
    
    
    id = Column(Integer, primary_key=True, index=True)
    identificador = Column(String(255), unique=True, index=True)
    client_id = Column(String(255), nullable=False)
    client_secret = Column(String(255), nullable=False)
    tenant_id = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    activo = Column(Integer, default=1)   # 1 es activo 2 inactivo
    created_at = Column(DateTime(timezone=True), server_default=func.now())
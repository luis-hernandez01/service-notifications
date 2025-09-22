from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, func
from src.config.config import Base


class Plantillas(Base):
    __tablename__ = "plantillas"
    
    
    id = Column(Integer, primary_key=True, index=True)
    identifying_name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    content_html = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
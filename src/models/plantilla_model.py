# from sqlalchemy import Column, TIMESTAMP, ForeignKey, Integer, String, Text, Boolean
# from sqlalchemy.orm import relationship

# from src.config.config import Base
# class Plantillas(Base):
#     __tablename__ = "plantillas"

#     id = Column(Integer, primary_key=True, index=True)
#     identifying_name = Column(String(255), nullable=False)
#     description = Column(String(255), nullable=False)
#     content_html = Column(Text, nullable=False)
#     activo = Column(Boolean, default=True, nullable=False, comment="Indica si el registro está activo (true) o inactivo (false)")
#     # Relación con credenciales
#     credenciales_id = Column(
#         Integer, ForeignKey("credenciales_correo.id"), nullable=False
#     )
    
    
#     # Campos de auditoria
#     created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
#     updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
#     deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")
    
#     # Relación ORM
#     credencial = relationship("CredencialesCorreo", backref="plantillas")










from sqlalchemy import Column, TIMESTAMP, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from src.config.config import Base


def crear_modelo_plantillas(base):
    """
    Crea dinámicamente la tabla 'plantillas'
    para el schema asociado a la Base recibida.
    """
    schema = base.metadata.schema  # Se obtiene el esquema actual

    class Plantillas(base):
        __tablename__ = "plantillas"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la plantilla")
        identifying_name = Column(String(255), nullable=False, comment="Nombre identificador de la plantilla")
        description = Column(String(255), nullable=False, comment="Descripción de la plantilla")
        content_html = Column(Text, nullable=False, comment="Contenido HTML de la plantilla")
        activo = Column(Boolean, default=True, nullable=False, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Relación con credenciales_correo (ajustado dinámicamente por schema)
        credenciales_id = Column(
            Integer,
            ForeignKey(f"{schema}.credenciales_correo.id", onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False,
            comment="ID de la credencial de correo asociada"
        )

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

        # Relación ORM
        # credencial = relationship(f"CredencialesCorreo_{schema}", backref="plantillas")

    # Renombrar clase según el schema
    Plantillas.__name__ = f"Plantillas_{schema}"
    return Plantillas


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Plantillas = crear_modelo_plantillas(Base[0])

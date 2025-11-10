# from sqlalchemy import Column, TIMESTAMP, Integer, String, Boolean

# from src.config.config import Base


# class CredencialesCorreo(Base):
#     __tablename__ = "credenciales_correo"

#     id = Column(Integer, primary_key=True, index=True)
#     client_id = Column(String(255), nullable=False)
#     client_secret = Column(String(255), nullable=False)
#     tenant_id = Column(String(255), nullable=False)
#     username = Column(String(255), nullable=False)
#     activo = Column(Boolean, default=True, nullable=False, comment="Indica si el registro está activo (true) o inactivo (false)")
    
#     # Campos de auditoria
#     created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
#     updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
#     deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")








from sqlalchemy import Column, TIMESTAMP, Integer, String, Boolean

from src.config.config import Base


def crear_modelo_credenciales_correo(base):
    """
    Crea dinámicamente la tabla 'credenciales_correo'
    para el schema asociado a la Base recibida.
    """
    class CredencialesCorreo(base):
        __tablename__ = "credenciales_correo"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del registro")
        client_id = Column(String(255), nullable=False, comment="ID del cliente de la aplicación")
        client_secret = Column(String(255), nullable=False, comment="Secreto del cliente de la aplicación")
        tenant_id = Column(String(255), nullable=False, comment="ID del tenant en Azure")
        username = Column(String(255), nullable=False, comment="Usuario de la cuenta de correo asociada")
        activo = Column(Boolean, default=True, nullable=False, comment="Indica si el registro está activo (true) o inactivo (false)")
        
        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar clase según el schema
    CredencialesCorreo.__name__ = f"CredencialesCorreo_{base.metadata.schema}"
    return CredencialesCorreo


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
CredencialesCorreo = crear_modelo_credenciales_correo(Base[0])

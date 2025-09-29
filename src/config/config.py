import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# URL de conexión para PostgreSQL
DATABASE_URL = (
    f"postgresql+psycopg2://notifications:ka8z53PkKZE5uNmCAOyVA2nMbiHNpWE3@dpg-d3d8c3jipnbc73fck58g-a.frankfurt-postgres.render.com/notifications_si78"
    # f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    # f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Crear engine y sesión
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# CREDENCIALES CORREOS 
class Settings:
    # variables de entorno O365
    TENANT_ID: str = os.getenv("TENANT_ID")
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
    USERNAME: str = os.getenv("USERNAMES")
    
    # variables de entorno SMTP 
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: str = os.getenv("SMTP_PORT")
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    
settings = Settings()

# mantener la conexion a la BD siempre abierta
def get_session():
    db = SessionLocal()
    try:
        yield db   
    finally:
        db.close()


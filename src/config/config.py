import os
from typing import Generator, List, Union

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Cargar variables de entorno
load_dotenv()

# VARIABLES
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


# # JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
URL_API_STORAGE = "https://notificaciones-t70l.onrender.com/api/v1/files/upload"


# SCHEMAS DIFERENTES DENTRO DE LA MISMA BASE
SCHEMA_NAMES = ["Notificaciones"]



# # --- Configura las URLs dinámicamente ---
DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


# # --- Crear engines y sesiones dinámicamente ---

engine = [create_engine(DB_URL, echo=False, future=True) for _ in SCHEMA_NAMES]
sessions = [sessionmaker(autocommit=False, autoflush=False, bind=e) for e in engine]


Base = [declarative_base(metadata=MetaData(schema=schema)) for schema in SCHEMA_NAMES]

def get_session(
    db_index: int | None = None,
) -> Generator[Union[Session, List[Session]], None, None]:
    """
    Devuelve:
      - Una sola sesión (si se pasa db_index)
      - Una lista de sesiones (si no se pasa)
    """
    if db_index is not None:
        db = sessions[db_index]()
        try:
            yield db
        finally:
            db.close()
    else:
        dbs = [Session() for Session in sessions]
        try:
            yield dbs
        finally:
            for db in dbs:
                db.close()
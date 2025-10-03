import sys
import pytest
from types import ModuleType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# `test_module = ModuleType("src.config.config")` crea un nuevo objeto de 
# módulo llamado `test_module` con el nombre "src.config.config". 
# Este objeto de módulo puede usarse para simular el comportamiento de un módulo real en Python.
test_module = ModuleType("src.config.config")
TestBase = declarative_base()

# configura un motor de base de datos de prueba y una sesión para SQLAlchemy
# Para fines de prueba. Esto es lo que hacen `test_engine` y `TestSessionLocal`:
test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Las líneas `test_module.Base = TestBase`, `test_module.engine = test_engine` y
# `test_module.SessionLocal = TestSessionLocal` está asignando atributos al objeto `test_module`.
test_module.Base = TestBase
test_module.engine = test_engine
test_module.SessionLocal = TestSessionLocal


# `sys.modules["src.config.config"] = test_module` está asignando el objeto `test_module` al
# Diccionario `sys.modules` bajo la clave `"src.config.config"`. Esto registra efectivamente
# `test_module` como el módulo que se importará cuando se solicite el módulo `src.config.config`
# en importaciones posteriores. Esta técnica se usa comúnmente en pruebas para reemplazar módulos reales con simulacros.
# o módulos de prueba para fines de pruebas aislados.
sys.modules["src.config.config"] = test_module

# Ahora importe los módulos del modelo del proyecto para que se registren en TestBase
# Importar únicamente los módulos que definen modelos (garantiza que las clases de modelo se adjunten a TestBase)
import importlib
importlib.import_module("src.models.plantilla_model")
importlib.import_module("src.models.credenciales_model")
importlib.import_module("src.models.logs_envio")

# Crear tablas en el motor de pruebas
TestBase.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Crea un ámbito transaccional para una prueba y genera una sesión de SQLAlchemy.
Después de la prueba, la transacción se revierte para que la base de datos esté limpia para la siguiente prueba.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

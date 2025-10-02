# tests/conftest.py
import sys
import pytest
from types import ModuleType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---- Create a fake src.config.config module BEFORE importing project modules ----
test_module = ModuleType("src.config.config")
TestBase = declarative_base()
# In-memory SQLite engine for tests
test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# expose attributes that project expects from src.config.config
test_module.Base = TestBase
test_module.engine = test_engine
test_module.SessionLocal = TestSessionLocal

# Insert into sys.modules so subsequent imports of src.config.config use this test module
sys.modules["src.config.config"] = test_module

# Now import the project's model modules so they will register against TestBase
# Importing only the modules that define models (ensures model classes attach to TestBase)
import importlib
importlib.import_module("src.models.plantilla_model")
importlib.import_module("src.models.credenciales_model")
importlib.import_module("src.models.logs_envio")
# (add more model imports here if you add more tests that require them)

# Create tables in the test engine
TestBase.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Creates a transactional scope for a test and yields a SQLAlchemy session.
    After the test the transaction is rolled back so DB is clean for the next test.
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

# tests/felipe/conftest.py

import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db

# Configuração do banco de dados para testes de Felipe
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_felipe.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

# Criação das tabelas no banco de dados de teste
Base.metadata.create_all(bind=engine)

# Fixture para o cliente de teste
@pytest.fixture(scope="session")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

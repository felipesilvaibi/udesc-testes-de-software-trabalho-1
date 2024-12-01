# tests/felipe/conftest.py

from unittest import mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine):
    """Cria uma sessão de banco de dados para um teste."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")  # Alterado de "module" para "function"
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


class MockerFixture:
    """
    Classe helper para fornecer métodos `patch` e `patch.object` que gerenciam automaticamente
    os mocks, iniciando-os e parando-os após o teste.
    """

    def __init__(self):
        self.patches = []

    def patch(self, target, **kwargs):
        patcher = mock.patch(target, **kwargs)
        mocked_object = patcher.start()
        self.patches.append(patcher)
        return mocked_object

    def patch_object(self, target, attribute, **kwargs):
        patcher = mock.patch.object(target, attribute, **kwargs)
        mocked_object = patcher.start()
        self.patches.append(patcher)
        return mocked_object

    def stop_all(self):
        for patcher in self.patches:
            patcher.stop()


@pytest.fixture
def mocker_fixture():
    """
    Fixture para fornecer a funcionalidade de `MockerFixture` nos testes.
    """
    mocker = MockerFixture()
    yield mocker
    mocker.stop_all()  # Finaliza todos os patches ao final do teste

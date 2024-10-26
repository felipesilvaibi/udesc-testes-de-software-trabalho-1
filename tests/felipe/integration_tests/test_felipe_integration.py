import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="module")
def client():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    db_session.close()
    engine.dispose()

def test_register_and_login(client):
    """
    RF1 - RN1 e RF2 - RN2: Testa o registro de usuário e o login subsequente para obter o token de acesso.
    """
    # Registrar um novo usuário
    response = client.post("/users/", json={"email": "felipe@test.com", "password": "senha123"})
    assert response.status_code == 201
    assert response.json() == {"msg": "Usuário registrado com sucesso"}

    # Fazer login com o usuário registrado
    response = client.post("/users/login", data={"username": "felipe@test.com", "password": "senha123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_task(client):
    """
    RF3 - RN3: Testa a criação de uma nova tarefa autenticada.
    """
    # Fazer login
    response = client.post("/users/login", data={"username": "felipe@test.com", "password": "senha123"})
    token = response.json()["access_token"]

    # Criar uma nova tarefa
    response = client.post(
        "/tasks/",
        json={"title": "Tarefa de Integração", "description": "Teste de integração", "due_date": "2024-12-31"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Tarefa de Integração"
    assert data["description"] == "Teste de integração"
    assert data["due_date"] == "2024-12-31"
    assert data["is_completed"] == False

def test_delete_task(client):
    """
    RF5 - RN5: Testa a exclusão de uma tarefa autenticada.
    """
    # Fazer login
    response = client.post("/users/login", data={"username": "felipe@test.com", "password": "senha123"})
    token = response.json()["access_token"]

    # Criar uma nova tarefa para deletar
    response = client.post(
        "/tasks/",
        json={"title": "Tarefa para Deletar", "description": "Descrição", "due_date": "2024-12-31"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = response.json()["id"]

    # Deletar a tarefa
    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Tarefa deletada com sucesso"}

def test_list_tasks_shared(client):
    """
    RF5 - RN5: Testa a listagem de tarefas compartilhadas (se aplicável).
    """
    # Registrar outro usuário
    response = client.post("/users/", json={"email": "amigo@test.com", "password": "senha456"})
    assert response.status_code == 201
    assert response.json() == {"msg": "Usuário registrado com sucesso"}

    # Fazer login com o usuário original
    response = client.post("/users/login", data={"username": "felipe@test.com", "password": "senha123"})
    token = response.json()["access_token"]

    # Compartilhar a tarefa (assumindo que existe uma tarefa com ID 1)
    response = client.post(
        "/tasks/1/share",
        json={"user_email": "amigo@test.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Tarefa compartilhada com amigo@test.com"}

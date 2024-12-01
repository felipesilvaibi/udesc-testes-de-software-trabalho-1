from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, Task, User, get_db
from main import app

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
    response = client.post(
        "/users/", json={"email": "douglas@test.com", "password": "senha789"}
    )
    assert response.status_code == 201
    assert response.json() == {"msg": "Usuário registrado com sucesso"}

    # Fazer login com o usuário registrado
    response = client.post(
        "/users/login", data={"username": "douglas@test.com", "password": "senha789"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_edit_task(client):
    """
    RF4 - RN4: Testa a edição de uma tarefa autenticada.
    """
    # Registrar e criar uma tarefa
    user = User(email="douglas@test.com", password="senha789")
    task = Task(
        title="Tarefa Original Douglas",
        description="Descrição original",
        owner_id=user.id,
    )
    db_session = next(get_db())
    db_session.add_all([user, task])
    db_session.commit()

    # Fazer login
    response = client.post(
        "/users/login", data={"username": "douglas@test.com", "password": "senha789"}
    )
    token = response.json()["access_token"]

    # Editar a tarefa
    response = client.put(
        f"/tasks/{task.id}",
        json={"title": "Tarefa Editada Douglas", "description": "Descrição editada"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Tarefa Editada Douglas"
    assert data["description"] == "Descrição editada"


def test_mark_task_completed(client):
    """
    RF6 - RN6: Testa a marcação de uma tarefa como concluída e o registro da data de conclusão.
    """
    # Registrar e criar uma tarefa
    user = User(email="douglas@test.com", password="senha789")
    task = Task(
        title="Tarefa a Ser Concluída Douglas",
        description="Descrição",
        owner_id=user.id,
    )
    db_session = next(get_db())
    db_session.add_all([user, task])
    db_session.commit()

    # Fazer login
    response = client.post(
        "/users/login", data={"username": "douglas@test.com", "password": "senha789"}
    )
    token = response.json()["access_token"]

    # Marcar a tarefa como concluída
    response = client.post(
        f"/tasks/{task.id}/complete", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Tarefa marcada como concluída"
    assert data["completion_date"] is not None


def test_list_tasks_owner(client):
    """
    RF7 - RN7: Testa a listagem de tarefas do próprio usuário autenticado.
    """
    # Registrar e criar duas tarefas
    user = User(email="douglas@test.com", password="senha789")
    task1 = Task(
        title="Tarefa Douglas 1",
        description="Descrição 1",
        owner_id=user.id,
        is_completed=False,
    )
    task2 = Task(
        title="Tarefa Douglas 2",
        description="Descrição 2",
        owner_id=user.id,
        is_completed=True,
    )
    db_session = next(get_db())
    db_session.add_all([user, task1, task2])
    db_session.commit()

    # Fazer login
    response = client.post(
        "/users/login", data={"username": "douglas@test.com", "password": "senha789"}
    )
    token = response.json()["access_token"]

    # Listar tarefas concluídas
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        params={"status": "concluídas"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Tarefa Douglas 2"
    assert data[0]["is_completed"] == True

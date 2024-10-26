# tests/felipe/unit_tests/test_tasks.py

# Testes Unitários de Felipe para tarefas (RF3, RN3, RF4, RN4)

import pytest

def get_auth_header(client, email, password):
    response = client.post("/users/login", data={"username": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def user_token(client):
    client.post("/users/", json={"email": "user@example.com", "password": "password123"})
    return get_auth_header(client, "user@example.com", "password123")

def test_create_task_with_valid_data(client, user_token):
    # Teste para RF3 e RN3 (criação de tarefa válida)
    response = client.post("/tasks/", json={
        "title": "Task 1",
        "description": "Description 1",
        "due_date": "2023-12-31"
    }, headers=user_token)
    assert response.status_code == 201
    assert response.json()["title"] == "Task 1"

def test_create_task_with_duplicate_title(client, user_token):
    # Teste para RN3 (título duplicado)
    client.post("/tasks/", json={
        "title": "Task 2",
        "description": "Description 2",
        "due_date": "2023-12-31"
    }, headers=user_token)
    response = client.post("/tasks/", json={
        "title": "Task 2",
        "description": "Another Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Você já possui uma tarefa com este título"

def test_create_task_without_title(client, user_token):
    # Teste para RF3 (criação de tarefa sem título)
    response = client.post("/tasks/", json={
        "title": "",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    assert response.status_code == 422  # Erro de validação

def test_edit_uncompleted_task(client, user_token):
    # Teste para RF4 e RN4 (edição de tarefa não concluída)
    response = client.post("/tasks/", json={
        "title": "Task 3",
        "description": "Description 3",
        "due_date": "2023-12-31"
    }, headers=user_token)
    task_id = response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Task 3 Edited",
        "description": "Description Edited",
        "due_date": "2024-01-01"
    }, headers=user_token)
    assert response.status_code == 200
    assert response.json()["title"] == "Task 3 Edited"

def test_edit_completed_task(client, user_token):
    # Teste para RN4 (tentativa de editar tarefa concluída)
    response = client.post("/tasks/", json={
        "title": "Task 4",
        "description": "Description 4",
        "due_date": "2023-12-31"
    }, headers=user_token)
    task_id = response.json()["id"]
    # Simular a conclusão da tarefa
    client.patch(f"/tasks/{task_id}/complete", headers=user_token)
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Task 4 Edited",
        "description": "Description Edited",
        "due_date": "2024-01-01"
    }, headers=user_token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Tarefas concluídas não podem ser editadas"

def test_edit_task_with_invalid_id(client, user_token):
    # Teste para RF4 (editar tarefa que não existe)
    response = client.put("/tasks/9999", json={
        "title": "Nonexistent Task",
        "description": "Description",
        "due_date": "2024-01-01"
    }, headers=user_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

def test_create_task_without_due_date(client, user_token):
    # Teste para RF3 (criação de tarefa sem data de vencimento)
    response = client.post("/tasks/", json={
        "title": "Task without Due Date",
        "description": "Description",
        # "due_date": None  # Omitido
    }, headers=user_token)
    assert response.status_code == 422  # Erro de validação

def test_edit_task_changing_to_duplicate_title(client, user_token):
    # Teste para RN3 (editar tarefa para um título já existente)
    client.post("/tasks/", json={
        "title": "Unique Title",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    response = client.post("/tasks/", json={
        "title": "Another Title",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    task_id = response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Unique Title",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Você já possui uma tarefa com este título"

def test_create_task_unauthenticated(client):
    # Teste para RF3 (criação de tarefa sem autenticação)
    response = client.post("/tasks/", json={
        "title": "Task Unauthorized",
        "description": "Description",
        "due_date": "2023-12-31"
    })
    assert response.status_code == 401

def test_edit_task_of_another_user(client, user_token):
    # Teste para RF4 (editar tarefa de outro usuário)
    # Registrar outro usuário
    client.post("/users/", json={"email": "otheruser@example.com", "password": "password123"})
    other_user_token = get_auth_header(client, "otheruser@example.com", "password123")
    # Outro usuário cria uma tarefa
    response = client.post("/tasks/", json={
        "title": "Other User Task",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=other_user_token)
    task_id = response.json()["id"]
    # Tentativa de editar a tarefa do outro usuário
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Edited Title",
        "description": "Edited Description",
        "due_date": "2024-01-01"
    }, headers=user_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

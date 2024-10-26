# tests/felipe/integration_tests/test_integration.py

# Testes de Integração de Felipe (usando RF1, RF2, RF3, RN1, RN2, RN3)

import pytest

def test_full_registration_and_task_creation_flow(client):
    # Teste de integração para RF1, RF2, RF3
    # Registrar usuário
    response = client.post("/users/", json={"email": "integration@example.com", "password": "password123"})
    assert response.status_code == 201
    # Login
    response = client.post("/users/login", data={"username": "integration@example.com", "password": "password123"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Criar tarefa
    response = client.post("/tasks/", json={
        "title": "Integration Task",
        "description": "Integration Description",
        "due_date": "2023-12-31"
    }, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Integration Task"

def test_task_creation_requires_authentication(client):
    # Teste de integração para RF2 e RF3
    # Tentativa de criar tarefa sem autenticação
    response = client.post("/tasks/", json={
        "title": "Unauthenticated Task",
        "description": "Description",
        "due_date": "2023-12-31"
    })
    assert response.status_code == 401

def test_cannot_edit_completed_task_integration(client):
    # Teste de integração para RF4 e RN4
    # Registrar e logar usuário
    client.post("/users/", json={"email": "integration2@example.com", "password": "password123"})
    response = client.post("/users/login", data={"username": "integration2@example.com", "password": "password123"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Criar tarefa
    response = client.post("/tasks/", json={
        "title": "Task to Complete",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=headers)
    task_id = response.json()["id"]
    # Concluir tarefa
    client.patch(f"/tasks/{task_id}/complete", headers=headers)
    # Tentar editar tarefa concluída
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Edited Title",
        "description": "Edited Description",
        "due_date": "2024-01-01"
    }, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Tarefas concluídas não podem ser editadas"

def test_cannot_register_with_existing_email_integration(client):
    # Teste de integração para RF1 e RN1
    # Registrar usuário
    client.post("/users/", json={"email": "existing@example.com", "password": "password123"})
    # Tentar registrar novamente com o mesmo e-mail
    response = client.post("/users/", json={"email": "existing@example.com", "password": "newpassword123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "E-mail já cadastrado"

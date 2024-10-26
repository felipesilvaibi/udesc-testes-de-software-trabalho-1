# tests/douglas/integration_tests/test_integration.py

# Testes de Integração de Douglas (usando RF5, RF6, RF7, RF8, RN5, RN6, RN7, RN8)

import pytest

def get_auth_header(client, email, password):
    response = client.post("/users/login", data={"username": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_complete_and_delete_task_flow(client):
    # Teste de integração para RF5, RF6, RN5, RN6
    # Registrar e logar usuário
    client.post("/users/", json={"email": "integration_douglas@example.com", "password": "password123"})
    response = client.post("/users/login", data={"username": "integration_douglas@example.com", "password": "password123"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Criar tarefa
    response = client.post("/tasks/", json={
        "title": "Task to Delete",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=headers)
    task_id = response.json()["id"]
    # Concluir tarefa
    client.patch(f"/tasks/{task_id}/complete", headers=headers)
    # Tentar excluir tarefa concluída
    response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Tarefas concluídas não podem ser excluídas"

def test_sharing_task_and_access_by_shared_user(client):
    # Teste de integração para RF8 e RN8
    # Registrar usuários
    client.post("/users/", json={"email": "owner@example.com", "password": "password123"})
    client.post("/users/", json={"email": "shared@example.com", "password": "password123"})
    owner_token = get_auth_header(client, "owner@example.com", "password123")
    shared_token = get_auth_header(client, "shared@example.com", "password123")
    # Criar tarefa
    response = client.post("/tasks/", json={
        "title": "Shared Integration Task",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=owner_token)
    task_id = response.json()["id"]
    # Compartilhar tarefa
    client.post(f"/tasks/{task_id}/share", json={"user_email": "shared@example.com"}, headers=owner_token)
    # Verificar se o usuário compartilhado pode ver a tarefa
    response = client.get("/tasks", headers=shared_token)
    tasks = response.json()
    task_titles = [task["title"] for task in tasks]
    assert "Shared Integration Task" in task_titles

def test_filtering_tasks_by_status_integration(client):
    # Teste de integração para RF7 e RN7
    # Registrar e logar usuário
    client.post("/users/", json={"email": "filtering@example.com", "password": "password123"})
    response = client.post("/users/login", data={"username": "filtering@example.com", "password": "password123"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Criar tarefas
    response = client.post("/tasks/", json={
        "title": "Pending Task Integration",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=headers)
    response = client.post("/tasks/", json={
        "title": "Completed Task Integration",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=headers)
    task_id = response.json()["id"]
    # Concluir uma tarefa
    client.patch(f"/tasks/{task_id}/complete", headers=headers)
    # Listar tarefas pendentes
    response = client.get("/tasks?status=pendentes", headers=headers)
    tasks = response.json()
    for task in tasks:
        assert task["is_completed"] is False
    # Listar tarefas concluídas
    response = client.get("/tasks?status=concluídas", headers=headers)
    tasks = response.json()
    for task in tasks:
        assert task["is_completed"] is True

def test_cannot_delete_task_of_another_user_integration(client):
    # Teste de integração para RF5 e RN5
    # Registrar usuários
    client.post("/users/", json={"email": "user1@example.com", "password": "password123"})
    client.post("/users/", json={"email": "user2@example.com", "password": "password123"})
    user1_token = get_auth_header(client, "user1@example.com", "password123")
    user2_token = get_auth_header(client, "user2@example.com", "password123")
    # Usuário 1 cria tarefa
    response = client.post("/tasks/", json={
        "title": "User1 Task",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user1_token)
    task_id = response.json()["id"]
    # Usuário 2 tenta excluir tarefa de usuário 1
    response = client.delete(f"/tasks/{task_id}", headers=user2_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

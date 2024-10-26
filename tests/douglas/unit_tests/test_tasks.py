# tests/douglas/unit_tests/test_tasks.py

# Testes Unitários de Douglas para tarefas (RF5, RN5, RF6, RN6, RF7, RN7, RF8, RN8)

import pytest

def get_auth_header(client, email, password):
    response = client.post("/users/login", data={"username": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def user_token(client):
    client.post("/users/", json={"email": "douglas@example.com", "password": "password123"})
    return get_auth_header(client, "douglas@example.com", "password123")

def test_delete_uncompleted_task(client, user_token):
    # Teste para RF5 e RN5 (exclusão de tarefa não concluída)
    response = client.post("/tasks/", json={
        "title": "Task Delete",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    task_id = response.json()["id"]
    response = client.delete(f"/tasks/{task_id}", headers=user_token)
    assert response.status_code == 200
    assert response.json()["msg"] == "Tarefa excluída com sucesso"

def test_delete_completed_task(client, user_token):
    # Teste para RN5 (tentativa de excluir tarefa concluída)
    response = client.post("/tasks/", json={
        "title": "Task Complete",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    task_id = response.json()["id"]
    client.patch(f"/tasks/{task_id}/complete", headers=user_token)
    response = client.delete(f"/tasks/{task_id}", headers=user_token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Tarefas concluídas não podem ser excluídas"

def test_mark_task_as_completed(client, user_token):
    # Teste para RF6 e RN6 (marcar tarefa como concluída)
    response = client.post("/tasks/", json={
        "title": "Task to Complete",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    task_id = response.json()["id"]
    response = client.patch(f"/tasks/{task_id}/complete", headers=user_token)
    assert response.status_code == 200
    assert response.json()["is_completed"] is True
    assert response.json()["completion_date"] is not None

def test_mark_nonexistent_task_as_completed(client, user_token):
    # Teste para RF6 (marcar tarefa inexistente como concluída)
    response = client.patch(f"/tasks/9999/complete", headers=user_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

def test_list_pending_tasks(client, user_token):
    # Teste para RF7 e RN7 (listagem de tarefas pendentes)
    # Criar tarefas pendentes
    client.post("/tasks/", json={
        "title": "Pending Task 1",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    client.post("/tasks/", json={
        "title": "Pending Task 2",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    response = client.get("/tasks?status=pendentes", headers=user_token)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2
    for task in tasks:
        assert task["is_completed"] is False

def test_list_completed_tasks(client, user_token):
    # Teste para RF7 e RN7 (listagem de tarefas concluídas)
    # Criar e concluir tarefas
    response = client.post("/tasks/", json={
        "title": "Completed Task 1",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    task_id = response.json()["id"]
    client.patch(f"/tasks/{task_id}/complete", headers=user_token)
    response = client.get("/tasks?status=concluídas", headers=user_token)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 1
    for task in tasks:
        assert task["is_completed"] is True

def test_share_task_with_user(client, user_token):
    # Teste para RF8 e RN8 (compartilhamento de tarefa)
    # Registrar outro usuário
    client.post("/users/", json={"email": "otheruser@example.com", "password": "password123"})
    # Criar tarefa
    response = client.post("/tasks/", json={
        "title": "Task to Share",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    task_id = response.json()["id"]
    # Compartilhar tarefa
    response = client.post(f"/tasks/{task_id}/share", json={"user_email": "otheruser@example.com"}, headers=user_token)
    assert response.status_code == 200
    assert response.json()["msg"] == "Tarefa compartilhada com otheruser@example.com"

def test_share_task_with_nonexistent_user(client, user_token):
    # Teste para RN8 (compartilhar tarefa com usuário inexistente)
    # Criar tarefa
    response = client.post("/tasks/", json={
        "title": "Task to Share 2",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    task_id = response.json()["id"]
    # Tentar compartilhar com usuário inexistente
    response = client.post(f"/tasks/{task_id}/share", json={"user_email": "nonexistent@example.com"}, headers=user_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário para compartilhamento não encontrado"

def test_shared_user_can_view_task(client, user_token):
    # Teste para RF8 e RN8 (usuário compartilhado pode visualizar tarefa)
    # Registrar outro usuário
    client.post("/users/", json={"email": "shareduser@example.com", "password": "password123"})
    shared_user_token = get_auth_header(client, "shareduser@example.com", "password123")
    # Criar tarefa
    response = client.post("/tasks/", json={
        "title": "Shared Task",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=user_token)
    task_id = response.json()["id"]
    # Compartilhar tarefa
    client.post(f"/tasks/{task_id}/share", json={"user_email": "shareduser@example.com"}, headers=user_token)
    # Verificar se o usuário compartilhado pode ver a tarefa
    response = client.get("/tasks", headers=shared_user_token)
    tasks = response.json()
    task_titles = [task["title"] for task in tasks]
    assert "Shared Task" in task_titles

def test_delete_task_of_another_user(client, user_token):
    # Teste para RF5 (tentar excluir tarefa de outro usuário)
    # Registrar outro usuário
    client.post("/users/", json={"email": "otheruser2@example.com", "password": "password123"})
    other_user_token = get_auth_header(client, "otheruser2@example.com", "password123")
    # Outro usuário cria uma tarefa
    response = client.post("/tasks/", json={
        "title": "Other User Task",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=other_user_token)
    task_id = response.json()["id"]
    # Tentativa de excluir a tarefa do outro usuário
    response = client.delete(f"/tasks/{task_id}", headers=user_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

def test_mark_task_as_completed_by_another_user(client, user_token):
    # Teste para RF6 (tentar concluir tarefa de outro usuário)
    # Registrar outro usuário
    client.post("/users/", json={"email": "otheruser3@example.com", "password": "password123"})
    other_user_token = get_auth_header(client, "otheruser3@example.com", "password123")
    # Outro usuário cria uma tarefa
    response = client.post("/tasks/", json={
        "title": "Other User Task 2",
        "description": "Description",
        "due_date": "2023-12-31"
    }, headers=other_user_token)
    task_id = response.json()["id"]
    # Tentativa de concluir a tarefa do outro usuário
    response = client.patch(f"/tasks/{task_id}/complete", headers=user_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"

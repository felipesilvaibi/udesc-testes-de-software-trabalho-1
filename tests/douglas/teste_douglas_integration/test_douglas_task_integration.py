import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from auth import (
    create_access_token,  # Importando a função para criar o token de autenticação
)
from database import Task, User  # Importando o modelo Task e User


# Teste de edição de tarefa
def test_edit_task_endpoint(client: TestClient, db_session: Session):
    """
    CT001: Edição de tarefas via endpoint
    Entradas:
        ID de tarefa: 1
        Dados atualizados da tarefa: título e descrição.
    Resultado Esperado:
        O sistema responde com sucesso (código 200).
        A tarefa é atualizada no banco de dados com os dados corretos.
    Prioridade:
        Alta
    Pós-condições:
        A tarefa com o ID fornecido está atualizada no sistema.
    """
    # Arrange (Preparação)
    user_data = {
        "name": "João Silva",
        "email": "joao.silva@exemplo.com",
        "password": "SenhaForte123",
    }

    # Criação de um usuário no banco
    user = User(
        name=user_data["name"], email=user_data["email"], password="hashedpassword"
    )
    db_session.add(user)
    db_session.commit()

    # Criação de uma tarefa associada ao usuário
    task_data = {
        "title": "Tarefa Antiga",
        "description": "Descrição antiga",
        "is_completed": False,
        "owner_id": user.id,
    }

    task = Task(**task_data)
    db_session.add(task)
    db_session.commit()

    # Gerando o token de autenticação para o usuário
    token = create_access_token(data={"sub": user.email})

    # Dados de entrada para atualização
    updated_data = {"title": "Tarefa Atualizada", "description": "Descrição atualizada"}

    # Act (Ação): Envia a requisição PUT para atualizar a tarefa, incluindo o token no cabeçalho de autorização
    response = client.put(
        f"/tasks/{task.id}",
        json=updated_data,
        headers={"Authorization": f"Bearer {token}"},  # Incluindo o token no cabeçalho
    )

    # Assert (Verificação)
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]
    assert response.json()["description"] == updated_data["description"]
    assert (
        response.json()["is_completed"] is False
    )  # Verifica que a tarefa não foi concluída

    # Verifica no banco de dados se a tarefa foi realmente atualizada
    updated_task = db_session.query(Task).filter_by(id=task.id).first()
    assert updated_task.title == updated_data["title"]
    assert updated_task.description == updated_data["description"]


def test_edit_task_database_communication(client: TestClient, db_session: Session):
    """
    CT006: Comunicação com o banco para edição de tarefas
    Entradas:
        ID de tarefa: 1
        Dados atualizados da tarefa: título e descrição.
    Resultado Esperado:
        O banco de dados é atualizado com as novas informações da tarefa.
        As alterações são persistidas corretamente.
    Prioridade:
        Média
    Pós-condições:
        A tarefa no banco de dados reflete as alterações feitas.
        Dados antigos não estão mais presentes.
    """
    # Arrange (Preparação)
    user_data = {
        "name": "Carlos Silva",
        "email": "carlos.silva@exemplo.com",
        "password": "SenhaForte123",
    }

    # Criação de um usuário no banco
    user = User(
        name=user_data["name"], email=user_data["email"], password="hashedpassword"
    )
    db_session.add(user)
    db_session.commit()

    # Criação de uma tarefa associada ao usuário
    task_data = {
        "title": "Tarefa Antiga",
        "description": "Descrição antiga",
        "is_completed": False,
        "owner_id": user.id,
    }

    task = Task(**task_data)
    db_session.add(task)
    db_session.commit()

    # Gerando o token de autenticação para o usuário
    token = create_access_token(data={"sub": user.email})

    # Dados de entrada para atualização
    updated_data = {"title": "Tarefa Atualizada", "description": "Descrição atualizada"}

    # Act (Ação): Envia a requisição PUT para atualizar a tarefa, incluindo o token no cabeçalho de autorização
    response = client.put(
        f"/tasks/{task.id}",
        json=updated_data,
        headers={"Authorization": f"Bearer {token}"},  # Incluindo o token no cabeçalho
    )

    # Assert (Verificação)
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]
    assert response.json()["description"] == updated_data["description"]
    assert (
        response.json()["is_completed"] is False
    )  # Verifica que a tarefa não foi concluída

    # Verifica no banco de dados se a tarefa foi realmente atualizada
    updated_task = db_session.query(Task).filter_by(id=task.id).first()
    assert updated_task.title == updated_data["title"]
    assert updated_task.description == updated_data["description"]
    assert updated_task.is_completed is False  # Verifica que a tarefa não foi concluída

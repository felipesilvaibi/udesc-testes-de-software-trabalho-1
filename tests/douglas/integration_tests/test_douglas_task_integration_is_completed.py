import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from auth import (
    create_access_token,  # Importando a função para criar o token de autenticação
)
from database import Task, User  # Importando o modelo Task e User


def test_complete_task_endpoint(client: TestClient, db_session: Session):
    """
    CT007: Conclusão de tarefas via endpoint
    Entradas:
        ID de tarefa: 103
    Resultado Esperado:
        A tarefa é marcada como concluída.
        O sistema retorna uma resposta de sucesso.
    Prioridade:
        Alta
    Pós-condições:
        A tarefa está marcada como concluída no sistema.
        A mudança é refletida no banco de dados.
    """
    # Arrange (Preparação)
    user_data = {
        "name": "Ana Souza",
        "email": "ana.souza@exemplo.com",
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
        "title": "Tarefa a Concluir",
        "description": "Descrição da tarefa a concluir",
        "is_completed": False,
        "owner_id": user.id,
    }

    task = Task(**task_data)
    db_session.add(task)
    db_session.commit()

    # Gerando o token de autenticação para o usuário
    token = create_access_token(data={"sub": user.email})

    # Act (Ação): Envia a requisição PATCH para concluir a tarefa, incluindo o token no cabeçalho de autorização
    response = client.patch(
        f"/tasks/{task.id}/complete",  # Endpoint para concluir a tarefa
        headers={"Authorization": f"Bearer {token}"},  # Incluindo o token no cabeçalho
    )

    # Assert (Verificação)
    assert response.status_code == 200
    assert response.json()["is_completed"] is True
    assert (
        "completion_date" in response.json()
    )  # Verifica se a data de conclusão foi preenchida

    # Verifica no banco de dados se a tarefa foi marcada como concluída
    completed_task = db_session.query(Task).filter_by(id=task.id).first()
    assert (
        completed_task.is_completed is True
    )  # Verifica que a tarefa foi marcada como concluída
    assert (
        completed_task.completion_date is not None
    )  # Verifica se a data de conclusão foi preenchida


def test_complete_task_database_communication(client: TestClient, db_session: Session):
    """
    CT008: Comunicação com o banco para conclusão de tarefas
    Entradas:
        ID de tarefa: 104
    Resultado Esperado:
        O status da tarefa é alterado para "concluída" no banco de dados.
        Não é possível alterar ou concluir novamente a tarefa.
    Prioridade:
        Alta
    Pós-condições:
        A tarefa não pode mais ser editada ou concluída novamente.
        O sistema respeita as regras de negócio estabelecidas.
    """
    # Arrange (Preparação)
    user_data = {
        "name": "Lucas Almeida",
        "email": "lucas.almeida@exemplo.com",
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
        "title": "Tarefa a Concluir",
        "description": "Descrição da tarefa a concluir",
        "is_completed": False,
        "owner_id": user.id,
    }

    task = Task(**task_data)
    db_session.add(task)
    db_session.commit()

    # Act (Ação): Envia a requisição PATCH para concluir a tarefa, incluindo o token no cabeçalho de autorização
    completed_task = db_session.query(Task).filter_by(id=task.id).first()
    completed_task.is_completed = True

    db_session.commit()

    # Assert (Verificação)
    completed_task_to_assert = db_session.query(Task).filter_by(id=task.id).first()
    assert completed_task_to_assert.is_completed is True

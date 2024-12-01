# test_task.py

from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import Task, User
from routers.task import TaskCreate, create_task, delete_task


def test_create_task_unique_title():
    """
    CT007: Garantir cadastro de tarefa com título único
    Entradas:
        Título: "Comprar leite"
        Descrição: "Ir ao mercado comprar mais leite"
    Resultado Esperado:
        A função retorna sucesso e um mock da tarefa é criado.
    Pós-condições:
        A tarefa está disponível no mock de tarefas
    """

    # Arrange (Preparação)
    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Mock para que nenhuma tarefa existente seja encontrada com o mesmo título
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None  # Nenhuma tarefa existente

    # Função auxiliar para simular a adição de uma nova tarefa
    def add_task(task):
        task.id = 1  # Simula a atribuição de um ID após inserção no banco

    mock_db.add.side_effect = add_task

    # Dados da nova tarefa a ser criada
    task_data = TaskCreate(
        title="Comprar leite",
        description="Ir ao mercado comprar mais leite",
    )

    # Act (Ação)
    new_task = create_task(task=task_data, current_user=mock_current_user, db=mock_db)

    # Assert (Verificação)
    assert new_task.title == "Comprar leite"
    assert new_task.description == "Ir ao mercado comprar mais leite"
    assert new_task.owner_id == mock_current_user.id

    mock_db.add.assert_called_once_with(new_task)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(new_task)


def test_create_task_duplicate_title():
    """
    CT008: Garantir erro ao cadastrar tarefa com título duplicado
    Entradas:
        Título: "Comprar leite" (título já existente)
        Descrição: "Ir ao mercado comprar mais leite"
    Resultado Esperado:
        A função retorna erro informando que o título da tarefa já existe
    Pós-condições:
        Nenhuma nova tarefa é adicionada ao mock
    """

    # Arrange (Preparação)
    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Simula uma tarefa existente com o mesmo título
    existing_task = Task(
        id=1,
        title="Comprar leite",
        description="Tarefa existente",
        owner_id=mock_current_user.id,
    )

    # Mock para retornar a tarefa existente ao filtrar por título
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = existing_task  # Tarefa existente encontrada

    # Dados da nova tarefa que tenta usar um título duplicado
    task_data = TaskCreate(
        title="Comprar leite",
        description="Ir ao mercado comprar mais leite",
    )

    # Act and Assert (Ação e Verificação)
    with pytest.raises(HTTPException) as exc_info:
        create_task(task=task_data, current_user=mock_current_user, db=mock_db)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Você já possui uma tarefa com este título"


def test_delete_existing_task():
    """
    CT009: Garantir exclusão de tarefa existente
    Entradas:
        ID da tarefa: 1
    Resultado Esperado:
        A função retorna sucesso e remove o mock da tarefa
    Pós-condições:
        Mock da tarefa não existe mais
    """

    # Arrange (Preparação)
    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Simula a tarefa existente a ser deletada
    existing_task = Task(
        id=1,
        title="Comprar pão",
        description="Ir à padaria",
        is_completed=False,
        owner_id=mock_current_user.id,
    )

    # Mock para retornar a tarefa existente ao filtrar por ID
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = existing_task  # Tarefa existente encontrada

    # Act (Ação)
    response = delete_task(task_id=1, current_user=mock_current_user, db=mock_db)

    # Assert (Verificação)
    assert response == {"msg": "Tarefa excluída com sucesso"}
    mock_db.delete.assert_called_once_with(existing_task)
    mock_db.commit.assert_called_once()


def test_delete_completed_task():
    """
    CT010: Garantir erro ao excluir tarefa concluída
    Entradas:
        ID da tarefa: 2
    Resultado Esperado:
        A função retorna erro informando que a tarefa já está concluída
    Pós-condições:
        Nenhuma alteração no mock de tarefas
    """

    # Arrange (Preparação)
    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Simula uma tarefa concluída
    completed_task = Task(
        id=2,
        title="Ler livro",
        description="Terminar de ler o capítulo 5",
        is_completed=True,
        owner_id=mock_current_user.id,
    )

    # Mock para retornar a tarefa concluída ao filtrar por ID
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = completed_task  # Tarefa concluída encontrada

    # Act and Assert (Ação e Verificação)
    with pytest.raises(HTTPException) as exc_info:
        delete_task(task_id=2, current_user=mock_current_user, db=mock_db)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Tarefas concluídas não podem ser excluídas"

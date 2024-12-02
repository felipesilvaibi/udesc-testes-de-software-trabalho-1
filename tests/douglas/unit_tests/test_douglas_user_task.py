# test_auth.py

from unittest.mock import Mock

from models import Task
from sqlalchemy.orm import Session

from routers.task import list_user_tasks


def test_list_tasks_for_user_with_tasks():
    """
    CT17: Listagem de tarefas do usuário
    Caso 1: Usuário com tarefas cadastradas
    Entradas:
        ID do usuário: 123
    Resultado Esperado:
        O sistema retorna a lista de tarefas do usuário.
    Pós-condições:
        O sistema mantém a integridade dos dados de tarefas.
    """
    # Arrange
    mock_db = Mock(spec=Session)
    user_id_with_tasks = 123

    # Simula tarefas cadastradas para o usuário
    tasks = [
        Task(
            id=1,
            title="Tarefa 1",
            description="Descrição 1",
            is_completed=False,
            owner_id=user_id_with_tasks,
        ),
        Task(
            id=2,
            title="Tarefa 2",
            description="Descrição 2",
            is_completed=True,
            owner_id=user_id_with_tasks,
        ),
    ]
    mock_db.query.return_value.filter.return_value.all.return_value = tasks

    # Act
    result = list_user_tasks(user_id=user_id_with_tasks, db=mock_db)

    # Assert
    assert len(result) == 2
    assert result[0].title == "Tarefa 1"
    assert result[1].is_completed is True


def test_list_tasks_for_user_without_tasks():
    """
    CT17: Listagem de tarefas do usuário
    Caso 2: Usuário sem tarefas cadastradas
    Entradas:
        ID do usuário: 456
    Resultado Esperado:
        O sistema retorna uma lista vazia.
    Pós-condições:
        O sistema mantém a integridade dos dados de tarefas.
    """
    # Arrange
    mock_db = Mock(spec=Session)
    user_id_without_tasks = 456

    # Simula que não há tarefas cadastradas para o usuário
    mock_db.query.return_value.filter.return_value.all.return_value = []

    # Act
    result = list_user_tasks(user_id=user_id_without_tasks, db=mock_db)

    # Assert
    assert result == []

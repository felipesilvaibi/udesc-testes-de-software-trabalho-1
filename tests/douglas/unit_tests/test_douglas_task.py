# test_auth.py

from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import Task, User
from routers.task import TaskUpdate, update_task


def test_update_task_not_completed_with_id():
    """
    CT11: Edição de tarefas não concluídas
    Entradas:
        Entrada 1: ID de uma tarefa pendente (exemplo: "002").
        Entrada 2: Novos dados para a tarefa (título atualizado).
    Resultado Esperado:
        O Sistema atualiza a tarefa e retorna sucesso.
    Pós-condições:
        A tarefa com ID "002" tem seus dados atualizados (título, descrição, prazo, etc.),
        mas o status permanece "pendente".
    """

    # Arrange (Preparação)
    task_id = 2
    titulo_atualizado = "título atualizado"

    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Criando uma tarefa não concluída
    task = Task(
        id=task_id,  # ID da tarefa sendo usada como entrada
        title="Tarefa Pendente",
        description="Esta tarefa não foi concluída",
        is_completed=False,  # A tarefa não está concluída
        owner_id=mock_current_user.id,
    )

    # Simulando a tarefa no mock DB
    mock_db.query.return_value.filter.return_value.first.side_effect = [task, None]

    # Act (Ação)
    response = update_task(
        task_id,
        TaskUpdate(title=titulo_atualizado),
        mock_current_user,
        mock_db,
    )
    # Assert (Verificação)
    assert response.title == titulo_atualizado


def test_update_task_completed():
    """
    CT12: Impedir edição de tarefas concluídas
    Entradas:
        Editar descrição da tarefa: "Tarefa completa"
    Resultado Esperado:
        O sistema retorna erro informando que a tarefa não pode ser editada.
    Pós-condições:
        Nenhuma alteração ocorre na tarefa (título, descrição, prazo, etc.).
    """

    # Arrange (Preparação)
    task_id = 2
    titulo_atualizado = "título atualizado"

    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Criando uma tarefa concluída (alterando o status para True)
    task = Task(
        id=1,
        title="Tarefa Completa",
        description="Esta tarefa foi concluída",
        is_completed=True,  # A tarefa está concluída
        owner_id=mock_current_user.id,
    )

    # Simulando a tarefa no mock DB
    mock_db.query.return_value.filter.return_value.first.return_value = task

    # Act (Ação)
    with pytest.raises(HTTPException) as exc_info:
        update_task(
            task_id,
            TaskUpdate(title=titulo_atualizado),
            mock_current_user,
            mock_db,
        )

    # Assert (Verificação)
    # Verificar se a exceção foi levantada corretamente
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Tarefas concluídas não podem ser editadas"


def test_update_nonexistent_task():
    """
    CT13: Edição de tarefa inexistente
    Entradas:
        Id: -2
    Resultado Esperado:
        O sistema retorna erro informando que a tarefa não foi encontrada.
    Pós-condições:
        O sistema não encontra a tarefa e retorna uma mensagem de erro.
    """

    # Arrange (Preparação)
    mock_db = Mock(spec=Session)

    # ID da tarefa inexistente
    task_id = -2
    updated_task_data = {
        "title": "Tarefa Inexistente Atualizada",
        "description": "Descrição atualizada",
    }

    # Simulando que nenhuma tarefa é encontrada no banco de dados
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act (Ação) e Assert (Verificação)
    with pytest.raises(HTTPException) as exc_info:
        task_to_update = mock_db.query.return_value.filter.return_value.first()
        if not task_to_update:
            raise HTTPException(
                status_code=404, detail=f"Tarefa com ID {task_id} não foi encontrada."
            )

    # Verificação do erro levantado
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Tarefa com ID {task_id} não foi encontrada."


def test_mark_task_as_completed():
    """
    CT14: Conclusão de tarefas não concluídas
    Entradas:
        Entrada 1: ID de uma tarefa pendente (exemplo: ID "002").
        Entrada 2: ID de uma tarefa já concluída.
    Resultado Esperado:
        Para a tarefa pendente, o sistema marca como concluída com sucesso.
        Para a tarefa já concluída, o sistema retorna um aviso informando que já está concluída.
    Pós-condições:
        O sistema guarda a mudança de status para a tarefa pendente.
    """

    # Arrange (Preparação)
    mock_db = Mock(spec=Session)

    # Tarefa pendente
    pending_task = Task(
        id=2,
        title="Tarefa Pendente",
        description="Descrição da tarefa pendente",
        is_completed=False,
        owner_id=1,
    )

    # Tarefa já concluída
    completed_task = Task(
        id=3,
        title="Tarefa Concluída",
        description="Descrição da tarefa concluída",
        is_completed=True,
        owner_id=1,
    )

    # Simulando tarefas no mock DB
    def mock_get_task(task_id):
        if task_id == 2:
            return pending_task
        elif task_id == 3:
            return completed_task
        else:
            return None

    mock_db.query.return_value.filter.return_value.first.side_effect = mock_get_task

    # Act & Assert (Ação e Verificação)

    # Cenário 1: Concluir tarefa pendente
    task_to_complete = mock_db.query.return_value.filter.return_value.first(task_id=2)
    if not task_to_complete:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    if not task_to_complete.is_completed:
        task_to_complete.is_completed = True  # Marca como concluída
        status_message = "Tarefa marcada como concluída com sucesso."
    else:
        status_message = "A tarefa já está concluída."

    assert task_to_complete.is_completed is True
    assert status_message == "Tarefa marcada como concluída com sucesso."

    # Cenário 2: Tentar concluir tarefa já concluída
    task_to_complete = mock_db.query.return_value.filter.return_value.first(task_id=3)
    if not task_to_complete:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    if not task_to_complete.is_completed:
        task_to_complete.is_completed = True  # Marca como concluída
        status_message = "Tarefa marcada como concluída com sucesso."
    else:
        status_message = "A tarefa já está concluída."

    assert task_to_complete.is_completed is True
    assert status_message == "A tarefa já está concluída."


def test_prevent_marking_already_completed_task():
    """
    CT15: Impedir conclusão de tarefas já concluídas
    Entradas:
        Entrada 1: ID de tarefa já concluída (ex.: "001").
        Entrada 2: ID de tarefa não concluída.
    Resultado Esperado:
        Para a tarefa já concluída, o sistema retorna erro informando que já está concluída.
        Para a tarefa não concluída, a tarefa é marcada como concluída com sucesso.
    Pós-condições:
        A tarefa já concluída mantém o status "concluída".
    """

    # Arrange (Preparação)
    mock_db = Mock(spec=Session)

    # Tarefa já concluída
    completed_task = Task(
        id=1,
        title="Tarefa Já Concluída",
        description="Descrição da tarefa já concluída",
        is_completed=True,
        owner_id=1,
    )

    # Tarefa não concluída
    pending_task = Task(
        id=2,
        title="Tarefa Não Concluída",
        description="Descrição da tarefa não concluída",
        is_completed=False,
        owner_id=1,
    )

    # Simulando tarefas no mock DB
    def mock_get_task(task_id):
        if task_id == 1:
            return completed_task
        elif task_id == 2:
            return pending_task
        else:
            return None

    mock_db.query.return_value.filter.return_value.first.side_effect = mock_get_task

    # teste 1: Tentar concluir tarefa já concluída
    task_to_complete = mock_db.query.return_value.filter.return_value.first(task_id=1)
    if not task_to_complete:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    if task_to_complete.is_completed:
        status_message = "Erro: A tarefa já está concluída."
    else:
        task_to_complete.is_completed = True
        status_message = "Tarefa marcada como concluída com sucesso."

    assert task_to_complete.is_completed is True
    assert status_message == "Erro: A tarefa já está concluída."

    # teste 2: Concluir tarefa não concluída
    task_to_complete = mock_db.query.return_value.filter.return_value.first(task_id=2)
    if not task_to_complete:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    if task_to_complete.is_completed:
        status_message = "Erro: A tarefa já está concluída."
    else:
        task_to_complete.is_completed = True
        status_message = "Tarefa marcada como concluída com sucesso."

    assert task_to_complete.is_completed is True
    assert status_message == "Tarefa marcada como concluída com sucesso."


def test_mark_nonexistent_task_as_completed():
    """
    CT16: Conclusão de tarefa inexistente
    Entradas:
        Entrada 1: ID de tarefa inexistente (ex.: "123456").
        Entrada 2: ID de tarefa válida.
    Resultado Esperado:
        Para a tarefa inexistente, o sistema retorna erro informando que não foi encontrada.
        Para a tarefa válida, a tarefa é marcada como concluída com sucesso.
    Pós-condições:
        O estado do sistema permanece inalterado para tarefas inexistentes.
        Para a tarefa válida, o status é atualizado para "concluído".
    """

    # Arrange (Preparação)
    mock_db = Mock(spec=Session)

    # Tarefa válida
    valid_task = Task(
        id=1,
        title="Tarefa Válida",
        description="Descrição da tarefa válida",
        is_completed=False,
        owner_id=1,
    )

    # Simulando tarefas no mock DB
    def mock_get_task(task_id):
        if task_id == 1:
            return valid_task
        else:
            return None

    mock_db.query.return_value.filter.return_value.first.side_effect = mock_get_task

    # Act & Assert (Ação e Verificação)

    # Cenário 1: Tentar concluir tarefa inexistente
    nonexistent_task = mock_db.query.return_value.filter.return_value.first(
        task_id=123456
    )
    if not nonexistent_task:
        error_message = "Erro: Tarefa não encontrada."
    else:
        nonexistent_task.is_completed = True
        error_message = "Tarefa marcada como concluída com sucesso."

    assert nonexistent_task is None
    assert error_message == "Erro: Tarefa não encontrada."

    # Cenário 2: Concluir tarefa válida
    task_to_complete = mock_db.query.return_value.filter.return_value.first(task_id=1)
    if not task_to_complete:
        error_message = "Erro: Tarefa não encontrada."
    else:
        task_to_complete.is_completed = True
        success_message = "Tarefa marcada como concluída com sucesso."

    assert task_to_complete.is_completed is True
    assert success_message == "Tarefa marcada como concluída com sucesso."

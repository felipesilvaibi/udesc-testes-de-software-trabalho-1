# test_auth.py

from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import Task, User
from routers.task import (
    ShareTask,
    TaskUpdate,
    complete_task,
    list_tasks,
    share_task,
    update_task,
)


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


def test_update_task_not_found():
    """
    CT13: Edição de tarefa inexistente
    Entradas:
        Entrada 1: ID de tarefa inexistente (ex.: "123456").
        Entrada 2: Novos dados para a tarefa.
    Resultado Esperado:
        O sistema retorna erro informando que a tarefa não foi encontrada.
    Pós-condições:
        O sistema não altera nada, já que a tarefa não existe.
    """

    # Arrange (Preparação)
    task_id = 123456  # ID de tarefa inexistente
    titulo_atualizado = "Tarefa atualizada"

    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Simulando que não encontramos a tarefa no mock DB
    mock_db.query.return_value.filter.return_value.first.return_value = None

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
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Tarefa não encontrada"


def test_mark_task_as_completed():
    """
    CT14: Conclusão de tarefas não concluídas
    Entradas:
        Entrada 1: ID de uma tarefa pendente.
    Resultado Esperado:
        O sistema marca a tarefa como concluída com sucesso.
    Pós-condições:
        O sistema guarda a mudança de status para a tarefa pendente.
    """

    # Arrange (Preparação)
    task_id = 2  # ID da tarefa pendente
    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Criando uma tarefa não concluída (status False)
    task = Task(
        id=task_id,
        title="Tarefa Pendente",
        description="Esta tarefa não foi concluída",
        is_completed=False,  # A tarefa não está concluída
        owner_id=mock_current_user.id,
    )

    # Simulando que a tarefa foi encontrada no mock DB
    mock_db.query.return_value.filter.return_value.first.return_value = task

    # Act (Ação)
    response = complete_task(task_id, mock_current_user, mock_db)

    # Assert (Verificação)
    # Verificar se a exceção foi levantada corretamente
    assert response.is_completed is True


def test_prevent_task_from_being_completed_if_already_completed():
    """
    CT15: Impedir conclusão de tarefas já concluídas
    """

    # Arrange (Preparação)
    task_id = 2  # ID da tarefa pendente
    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Criando uma tarefa não concluída (status False)
    task = Task(
        id=task_id,
        title="Tarefa Pendente",
        description="Esta tarefa não foi concluída",
        is_completed=True,  # A tarefa não está concluída
        owner_id=mock_current_user.id,
    )

    # Simulando que a tarefa foi encontrada no mock DB
    mock_db.query.return_value.filter.return_value.first.return_value = task

    # Act (Ação)
    with pytest.raises(HTTPException) as exc_info:
        complete_task(task_id, mock_current_user, mock_db)

    # Assert (Verificação)
    # Verificar se a exceção foi levantada corretamente
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Tarefa já está concluída"


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
    task_id = 123456  # ID de tarefa inexistente

    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Simulando que não encontramos a tarefa no mock DB
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act (Ação)
    with pytest.raises(HTTPException) as exc_info:
        complete_task(task_id, mock_current_user, mock_db)

    # Assert (Verificação)
    # Verificar se a exceção foi levantada corretamente
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Tarefa não encontrada"


def test_list_tasks():
    """
    CT17: Listagem de tarefas do usuário

    Resultado Esperado:
        O sistema retorna a lista de tarefas de um usuário.

    Entradas:

    Entrada 1: ID de um usuário com tarefas cadastradas (exemplo: ID "123").

    """
    # Arrange (Preparação)
    task_id = 1

    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Criando uma tarefa não concluída (status False)
    task = Task(
        id=task_id,
        title="Tarefa Pendente",
        description="Esta tarefa não foi concluída",
        is_completed=True,  # A tarefa não está concluída
        owner_id=mock_current_user.id,
    )

    # Simulando que a tarefa foi encontrada no mock DB
    mock_db.query.return_value.filter.return_value.all.return_value = [task]

    # Act (Ação)
    response = list_tasks(None, mock_current_user, mock_db)

    # Assert (Verificação)
    # Verificar se a exceção foi levantada corretamente
    assert len(response) == 1
    assert response[0] == task


@pytest.mark.parametrize(
    "status_filter, is_completed",
    [
        ("concluídas", True),
        ("pendentes", False),
    ],
)
def test_list_tasks_by_status(status_filter, is_completed):
    """
    CT18: Teste de filtragem de tarefas por status, com uma tarefa concluída e uma tarefa pendente no mock.
    """
    # Arrange (Preparação)
    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    tasks = [
        Task(
            id=1,
            title="Tarefa Concluída",
            description="Tarefa finalizada",
            is_completed=True,
            owner_id=mock_current_user.id,
        ),
        Task(
            id=2,
            title="Tarefa Pendente",
            description="Tarefa não finalizada",
            is_completed=False,
            owner_id=mock_current_user.id,
        ),
    ]

    expected_task = next(task for task in tasks if task.is_completed == is_completed)

    filters = []

    def filter_mock(*conditions):
        nonlocal filters
        filters.extend(conditions)
        return mock_db.query.return_value

    def all_mock():
        filtered_tasks = tasks
        for condition in filters:
            if not hasattr(condition, "right"):
                continue

            boolean = True if str(True).lower() == str(condition.right) else False
            filtered_tasks = [
                task for task in filtered_tasks if task.is_completed == boolean
            ]
        return filtered_tasks

    mock_db.query.return_value.filter.side_effect = filter_mock
    mock_db.query.return_value.all = all_mock

    # Act (Ação)
    response = list_tasks(status_filter, mock_current_user, mock_db)

    # Assert (Verificação)
    assert len(response) == 1
    assert response[0] == expected_task


def test_list_tasks_by_stats_not_exist():
    """
    CT19: Verificar o comportamento ao filtrar por um status que não existe
    Entradas:
        Entrada 1: Status inválido para filtragem (exemplo: "em progresso", que não é um status reconhecido pelo sistema).
    Resultado Esperado:
        O sistema retorna erro informando que o status fornecido é inválido, no caso de um status não reconhecido.
        Para um status válido, o sistema realiza a filtragem normalmente.
    """
    # Arrange (Preparação)
    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    # Act (Ação)
    with pytest.raises(HTTPException) as exc_info:
        list_tasks("concluídas2", mock_current_user, mock_db)

    # Assert (Verificação)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Status inválido. Use 'concluídas' ou 'pendentes'."


def test_task_sharing():
    """
    CT20: Compartilhamento de tarefas
    Resultado Esperado:
        Tarefa é compartilhada com sucesso.
    Entradas:
        ID do usuário com tarefa: "123" (usuário com tarefa cadastrada).
        ID do usuário para compartilhar a tarefa: "456" (outro usuário cadastrado no sistema).
    Prioridade:
        Alta
    Pós-condições:
        O outro usuário tem acesso à tarefa compartilhada, podendo visualizá-la e interagir com ela conforme as permissões do sistema.
    """
    # Arrange (Preparação)
    mock_db = Mock(spec=Session)
    mock_current_user = User(id=1, email="user@example.com")

    task_id = 123
    task = Task(
        id=task_id,
        title="Tarefa Pendente",
        description="Esta tarefa não foi concluída",
        is_completed=False,
        owner_id=mock_current_user.id,
    )

    share_user_email = "teste@gmail.com"
    share_user = User(
        id=1,
        name="User to Share",
        email=share_user_email,
        password="fake_password",
        tasks=[],
        shared_tasks=[],
    )

    mock_db.query.return_value.filter.return_value.first.side_effect = [
        task,
        share_user,
    ]

    response = share_task(
        task_id, ShareTask(user_email=share_user_email), mock_current_user, mock_db
    )

    assert response == {"msg": f"Tarefa compartilhada com {share_user_email}"}
    assert task.shared_with_users[0] == share_user

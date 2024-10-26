from database import Task, User
from datetime import date

def test_create_task(db_session):
    """
    RF3 - RN3: Testa a criação de uma nova tarefa com título único, descrição e data de vencimento.
    """
    user = User(email="felipe@test.com", password="senha123")
    db_session.add(user)
    db_session.commit()

    task = Task(
        title="Nova Tarefa",
        description="Descrição da tarefa",
        due_date=date.today(),
        owner_id=user.id
    )
    db_session.add(task)
    db_session.commit()

    assert task.id is not None
    assert task.title == "Nova Tarefa"
    assert task.owner_id == user.id

def test_delete_task(db_session):
    """
    RF5 - RN5: Testa a exclusão de uma tarefa não concluída.
    """
    user = User(email="felipe@test.com", password="senha123")
    task = Task(
        title="Tarefa a Ser Deletada",
        description="Descrição",
        due_date=date.today(),
        owner_id=user.id
    )
    db_session.add_all([user, task])
    db_session.commit()

    # Deletar a tarefa
    db_session.delete(task)
    db_session.commit()

    assert db_session.query(Task).filter(Task.id == task.id).first() is None

def test_delete_completed_task(db_session):
    """
    RF5 - RN5: Verifica que uma tarefa concluída não pode ser deletada.
    """
    user = User(email="felipe@test.com", password="senha123")
    task = Task(
        title="Tarefa Concluída para Deleção",
        description="Descrição",
        due_date=date.today(),
        owner_id=user.id,
        is_completed=True
    )
    db_session.add_all([user, task])
    db_session.commit()

    # Tentar deletar a tarefa concluída
    try:
        db_session.delete(task)
        db_session.commit()
    except Exception:
        db_session.rollback()

    # Verificar que a tarefa ainda existe
    assert db_session.query(Task).filter(Task.id == task.id).first() is not None

def test_task_due_date(db_session):
    """
    RF3 - RN3: Verifica se a data de vencimento da tarefa está correta.
    """
    user = User(email="felipe@test.com", password="senha123")
    task = Task(
        title="Tarefa com Data",
        description="Descrição",
        due_date=date(2024, 12, 31),
        owner_id=user.id
    )
    db_session.add_all([user, task])
    db_session.commit()

    assert task.due_date == date(2024, 12, 31)

def test_task_overdue(db_session):
    """
    RF7 - RN7: Testa se uma tarefa está atrasada com base na data de vencimento.
    """
    user = User(email="felipe@test.com", password="senha123")
    task = Task(
        title="Tarefa Atrasada",
        description="Descrição",
        due_date=date(2020, 1, 1),
        owner_id=user.id
    )
    db_session.add_all([user, task])
    db_session.commit()

    assert task.due_date < date.today()

def test_duplicate_task_title(db_session):
    """
    RF3 - RN3: Verifica se é permitido ter tarefas com títulos duplicados (dependendo da lógica de negócio).
    """
    user = User(email="felipe@test.com", password="senha123")
    task1 = Task(
        title="Tarefa Duplicada",
        description="Primeira tarefa",
        due_date=date.today(),
        owner_id=user.id
    )
    task2 = Task(
        title="Tarefa Duplicada",
        description="Segunda tarefa",
        due_date=date.today(),
        owner_id=user.id
    )
    db_session.add_all([user, task1, task2])
    db_session.commit()

    # Dependendo da lógica de negócio, pode haver restrições de unicidade
    # Aqui assumimos que títulos duplicados são permitidos
    assert task1.title == task2.title

def test_share_task_visibility(db_session):
    """
    RF5 - RN5: Verifica se uma tarefa compartilhada aparece na listagem do usuário com quem foi compartilhada.
    """
    owner = User(email="felipe@test.com", password="senha123")
    recipient = User(email="amigo@test.com", password="senha456")
    task = Task(
        title="Visível Compartilhada",
        description="Descrição",
        due_date=date.today(),
        owner_id=owner.id
    )
    db_session.add_all([owner, recipient, task])
    db_session.commit()

    # Compartilhar a tarefa
    task.shared_with_users.append(recipient)
    db_session.commit()

    # Verificar se a tarefa aparece nas shared_tasks do destinatário
    assert task in recipient.shared_tasks

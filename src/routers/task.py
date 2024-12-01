# src/routers/task.py

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session

from auth import get_current_user
from database import Task, User, get_db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


# Schemas
class TaskCreate(BaseModel):
    title: constr(min_length=1)
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=1)] = None
    description: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    completion_date: Optional[datetime]
    owner_id: int

    class Config:
        orm_mode = True


class ShareTask(BaseModel):
    user_email: EmailStr


# Endpoints


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    RF3: O sistema deve permitir que o usuário cadastre novas tarefas
    """

    # RF3-RN1: O mesmo usuário não pode ter mais de uma tarefa com o mesmo nome
    existing_task = (
        db.query(Task)
        .filter(Task.title == task.title, Task.owner_id == current_user.id)
        .first()
    )
    if existing_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você já possui uma tarefa com este título",
        )

    new_task = Task(
        title=task.title, description=task.description, owner_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    RF4: O sistema deve permitir a edição de tarefas cadastradas
    """

    existing_task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada",
        )

    # RF4-RN1: Tarefas concluídas não podem ser editadas
    if existing_task.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tarefas concluídas não podem ser editadas",
        )

    if task.title and task.title != existing_task.title:
        duplicate_task = (
            db.query(Task)
            .filter(Task.title == task.title, Task.owner_id == current_user.id)
            .first()
        )
        if duplicate_task:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você já possui uma tarefa com este título",
            )

    for key, value in task.dict(exclude_unset=True).items():
        setattr(existing_task, key, value)

    db.commit()
    db.refresh(existing_task)

    return existing_task


@router.delete("/{task_id}", response_model=dict, status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    RF5: O sistema deve permitir a exclusão de tarefas
    """

    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada",
        )

    # RF5-RN1: Tarefas concluídas não podem ser excluídas
    if task.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tarefas concluídas não podem ser excluídas",
        )

    db.delete(task)
    db.commit()

    return {"msg": "Tarefa excluída com sucesso"}


@router.patch(
    "/{task_id}/complete", response_model=TaskResponse, status_code=status.HTTP_200_OK
)
def complete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    RF6: O sistema deve permitir marcar tarefas como concluídas
    """

    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada",
        )

    # RF6-RN1: Tarefas já concluídas não podem ser concluídas novamente
    if task.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tarefa já está concluída",
        )

    task.is_completed = True
    task.completion_date = datetime.utcnow()
    db.commit()
    db.refresh(task)

    return task


@router.get("/", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def list_tasks(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    RF7: O sistema deve permitir a listagem de tarefas
    """

    query = db.query(Task).filter(
        (Task.owner_id == current_user.id)
        | (Task.shared_with_users.any(id=current_user.id))
    )

    # RF7-RN1: O usuário deve poder filtrar tarefas por status (concluídas ou pendentes).
    if status:
        if status.lower() == "concluídas":
            query = query.filter(Task.is_completed == True)
        elif status.lower() == "pendentes":
            query = query.filter(Task.is_completed == False)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status inválido. Use 'concluídas' ou 'pendentes'.",
            )

    tasks = query.all()
    return tasks


@router.post("/{task_id}/share", response_model=dict, status_code=status.HTTP_200_OK)
def share_task(
    task_id: int,
    share: ShareTask,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    RF8: O sistema deve permitir que usuários compartilhem suas tarefas com demais usuários
    """

    # RF8-RN1: Somente tarefas criadas pelo usuário logado podem ser compartilhadas pelo mesmo
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada ou você não tem permissão para compartilhá-la",
        )

    user_to_share = db.query(User).filter(User.email == share.user_email).first()
    if not user_to_share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário para compartilhamento não encontrado",
        )

    if user_to_share in task.shared_with_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tarefa já está compartilhada com este usuário",
        )

    task.shared_with_users.append(user_to_share)
    db.commit()

    return {"msg": f"Tarefa compartilhada com {share.user_email}"}

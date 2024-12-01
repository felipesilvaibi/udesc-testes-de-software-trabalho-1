# src/database.py

from typing import Generator

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

task_shares = Table(
    "task_shares",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)

    # Relacionamento com as tarefas que o usuário possui
    tasks = relationship("Task", back_populates="owner")

    # Relacionamento com as tarefas que foram compartilhadas com o usuário
    shared_tasks = relationship(
        "Task", secondary=task_shares, back_populates="shared_with_users"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relacionamento com o usuário que possui a tarefa
    owner = relationship("User", back_populates="tasks")

    # Relacionamento com os usuários com quem a tarefa foi compartilhada
    shared_with_users = relationship(
        "User", secondary=task_shares, back_populates="shared_tasks"
    )


# Dependência para obter a sessão do banco de dados
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

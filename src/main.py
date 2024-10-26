from fastapi import FastAPI
from routers import user, task
from database import Base, engine

# Criação das tabelas no banco de dados (se ainda não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gerenciador de Tarefas",
    description="API para gerenciamento de tarefas com autenticação de usuários",
    version="1.0.0"
)

# Inclusão dos roteadores
app.include_router(user.router)
app.include_router(task.router)

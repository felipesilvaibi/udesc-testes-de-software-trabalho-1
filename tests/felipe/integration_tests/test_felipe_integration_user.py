# tests/felipe/integration_tests/test_felipe_integration_user.py

import pytest
from sqlalchemy.orm import Session

from auth import get_password_hash
from database import User


def test_register_user_endpoint(client: pytest.fixture, db_session: Session):
    """
    CT001: Cadastro de novos usuários via endpoint
    Entradas:
        Nome: "João silva"
        Email: "joao.silva@exemplo.com"
        Senha: "SenhaForte123"
    Resultado Esperado:
        O sistema responde com sucesso (código 201).
        O usuário é armazenado no banco de dados com os dados corretos.
    Prioridade:
        Alta
    Pós-condições:
        O usuário está cadastrado no sistema.
    """
    # Arrange (Preparação)
    user_data = {
        "name": "João silva",
        "email": "joao.silva@exemplo.com",
        "password": "SenhaForte123",
    }

    # Act (Ação)
    response = client.post("/users/", json=user_data)

    # Assert (Verificação)
    assert response.status_code == 201
    assert response.json() == {"msg": "Usuário registrado com sucesso"}

    # Verifica se o usuário foi armazenado no banco de dados
    user_in_db = db_session.query(User).filter_by(email=user_data["email"]).first()
    assert user_in_db.name == user_data["name"]
    assert user_in_db.email == user_data["email"]


def test_register_user_database_communication(db_session: Session):
    """
    CT002: Comunicação com o banco para cadastro de usuários
    Entradas:
        Nome: "Maria silva"
        Email: "maria.silva@exemplo.com"
        Senha: "SenhaSegura456"
    Resultado Esperado:
        O sistema salva o usuário no banco de dados.
        Os dados do usuário estão corretos e completos no banco.
    Prioridade:
        Alta
    Pós-condições:
        O usuário está cadastrado no sistema.
    """
    # Arrange (Preparação)
    user_data = {
        "name": "Maria silva",
        "email": "maria.silva@exemplo.com",
        "password": "SenhaSegura456",
    }

    # Hasheia a senha
    hashed_password = get_password_hash(user_data["password"])

    new_user = User(
        name=user_data["name"], email=user_data["email"], password=hashed_password
    )

    # Act (Ação)
    # Cria um novo usuário diretamente usando o db_session
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    # Assert (Verificação)
    # Verifica se o usuário foi salvo corretamente no banco de dados
    user_in_db = db_session.query(User).filter_by(email=user_data["email"]).first()
    assert user_in_db.name == user_data["name"]
    assert user_in_db.email == user_data["email"]
    assert user_in_db.password == hashed_password

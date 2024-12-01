# test_user.py

from unittest.mock import Mock

import pytest
from pydantic import ValidationError
from sqlalchemy.orm import Session

# Importa a função register atualizada e os modelos necessários
from routers.user import UserCreate, register


def test_register_user_with_valid_data():
    """
    CT003: Garantir cadastro de usuário com dados válidos
    Entradas:
        Nome: "João"
        Email: "joao@test.com"
        Senha: "Senha123"
    Resultado Esperado:
        Função retorna sucesso e um mock de usuário criado
    Pós-condições:
        O mock de usuário contém os dados fornecidos
    """
    # Arrange
    mock_db = Mock(spec=Session)
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None  # Nenhum usuário existente com o mesmo e-mail

    def add_user(user):
        user.id = 1  # Simula a atribuição de um ID após salvar no banco

    mock_db.add.side_effect = add_user

    user_data = UserCreate(name="João", email="joao@test.com", password="Senha123")

    # Act
    response = register(user=user_data, db=mock_db)

    # Assert
    assert response == {"msg": "Usuário registrado com sucesso"}
    created_user = mock_db.add.call_args[0][0]
    assert created_user.name == "João"
    assert created_user.email == "joao@test.com"
    assert created_user.password != "Senha123"  # A senha deve estar hasheada


def test_register_user_with_empty_name():
    """
    CT004: Garantir erro ao cadastrar usuário com nome vazio
    Entradas:
        Nome: ""
        Email: "joao@test.com"
        Senha: "Senha123"
    Resultado Esperado:
        Função retorna erro informando que o nome é obrigatório
    Pós-condições:
        Nenhum mock de usuário criado
    """
    # Arrange
    mock_db = Mock(spec=Session)
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None  # Nenhum usuário existente com o mesmo e-mail

    # Dados do usuário com nome vazio
    user_data = {"name": "", "email": "joao@test.com", "password": "Senha123"}

    # Act
    with pytest.raises(ValidationError) as exc_info:
        user = UserCreate(**user_data)
        register(user=user, db=mock_db)

    # Assert
    errors = exc_info.value.errors()
    assert any(error["loc"] == ("name",) for error in errors)
    assert any(
        "String should have at least 1 character" in error["msg"] for error in errors
    )

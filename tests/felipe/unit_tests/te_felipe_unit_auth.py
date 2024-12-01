from unittest import mock

from sqlalchemy.orm import Session

import auth
from auth import authenticate_user, get_password_hash, verify_password
from database import User

class teste(BaseModel)

def test_returns_hashed_password_from_plain_text():
    """
    RF1: O sistema deve permitir manter usuários
    RF1-RN1: Deve ser possível cadastrar novos usuários com senha criptografada de forma unidirecional.
    UT001: Criptografia da senha
    """

    # Arrange
    password = "senha_segura123"

    # Act
    hashed_password = get_password_hash(password)

    # Assert
    assert hashed_password != password
    assert hashed_password.startswith("$2b$")  # Verifica se é um hash bcrypt


def test_hashed_password_matches_original_with_key():
    """
    RF1: O sistema deve permitir manter usuários
    RF1-RN1: Deve ser possível cadastrar novos usuários com senha criptografada de forma unidirecional.
    UT002: Consistência do hash para a mesma senha
    """

    # Arrange
    password = "senha_segura123"
    hashed_password = get_password_hash(password)

    # Act
    result = verify_password(password, hashed_password)

    # Assert
    assert result is True


def test_hashed_password_does_not_match_non_original_password():
    """
    RF1: O sistema deve permitir manter usuários
    RF1-RN1: Deve ser possível cadastrar novos usuários com senha criptografada de forma unidirecional.
    UT003: Diferenciação de hashes para senhas diferentes
    """

    # Arrange
    password = "senha_segura123"
    hashed_password = get_password_hash(password)

    # Act
    result = verify_password("outra_senha", hashed_password)

    # Assert
    assert result is False


def test_authenticate_user_success():
    """
    RF1: O sistema deve permitir manter usuários
    RF1-RN2: O usuário deve poder acessar o sistema com o e-mail e senha cadastrados.
    UT004: Autenticação com credenciais corretas
    """

    # Arrange
    fake_user_data = {
        "email": "felipe@test.com",
        "password": "senha_teste123",
        "hashed_password": get_password_hash("senha_teste123"),
    }
    fake_user = User(
        email=fake_user_data["email"], password=fake_user_data["hashed_password"]
    )

    mock_db = mock.Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = fake_user

    # Act
    response = authenticate_user(
        fake_user_data["email"], fake_user_data["password"], mock_db
    )

    # Assert
    assert response == fake_user


def test_authenticate_user_wrong_password(mocker_fixture):
    """
    RF1: O sistema deve permitir manter usuários
    RF1-RN2: O usuário deve poder acessar o sistema com o e-mail e senha cadastrados.
    UT005: Autenticação com senha incorreta
    """

    # Arrange
    fake_user_data = {
        "email": "felipe@test.com",
        "password": "senha_teste123",
        "hashed_password": get_password_hash("senha_teste123"),
    }
    fake_user = User(
        email=fake_user_data["email"], password=fake_user_data["hashed_password"]
    )

    mock_db = mock.Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = fake_user

    spy_verify_password = mocker_fixture.patch_object(
        auth, "verify_password", wraps=verify_password
    )

    # Act
    response = authenticate_user(
        fake_user_data["email"], "senha_diferente_da_original_123", mock_db
    )

    # Assert
    assert response is False
    spy_verify_password.call_count == 1


def test_authenticate_user_nonexistent(mocker_fixture):
    """
    RF1: O sistema deve permitir manter usuários
    RF1-RN2: O usuário deve poder acessar o sistema com o e-mail e senha cadastrados.
    UT006: Autenticação de usuário não cadastrado
    """

    # Arrange
    mock_db = mock.Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    spy_verify_password = mocker_fixture.patch_object(
        auth, "verify_password", wraps=verify_password
    )

    # Act
    response = authenticate_user("felipe@test.com", "senha_teste987", mock_db)

    # Assert
    assert response is False
    spy_verify_password.call_count == 0

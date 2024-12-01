from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from auth import authenticate_user, get_password_hash
from database import User


def test_user_login_endpoint(client: TestClient, db_session: Session):
    """
    CT003: Login de usuários via endpoint
    Entradas:
        Email: "joao.silva@exemplo.com"
        Senha: "SenhaForte123"
    Resultado Esperado:
        O sistema responde com sucesso (código 200).
        Um token de autenticação é fornecido ao usuário.
    Prioridade:
        Alta
    Pós-condições:
        O usuário está autenticado no sistema.
    """
    # Arrange: Cria o usuário no banco de dados
    user_data = {
        "name": "João Silva",
        "email": "joao.silva@exemplo.com",
        "password": "SenhaForte123",
    }

    # Hasheia a senha e cria o usuário
    hashed_password = get_password_hash(user_data["password"])
    user = User(
        name=user_data["name"], email=user_data["email"], password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Act: Tenta fazer login via endpoint
    login_data = {"username": user_data["email"], "password": user_data["password"]}

    response = client.post("/users/login", data=login_data)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json
    assert response_json["token_type"] == "bearer"


def test_user_login_database_communication(db_session: Session):
    """
    CT004: Comunicação com o banco para login de usuários
    Entradas:
        Email: "maria.silva@exemplo.com"
        Senha: "SenhaSegura456"
    Resultado Esperado:
        O sistema consulta o banco de dados.
        Autentica o usuário se as credenciais forem válidas.
    Prioridade:
        Alta
    Pós-condições:
        O usuário está autenticado no sistema.
    """
    # Arrange: Cria o usuário no banco de dados
    user_data = {
        "name": "Maria Silva",
        "email": "maria.silva@exemplo.com",
        "password": "SenhaSegura456",
    }

    # Hasheia a senha e cria o usuário
    hashed_password = get_password_hash(user_data["password"])
    user = User(
        name=user_data["name"], email=user_data["email"], password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Act: Autentica o usuário diretamente usando a função authenticate_user

    authenticated_user = authenticate_user(
        email=user_data["email"], password=user_data["password"], db=db_session
    )

    # Assert
    assert authenticated_user is not False
    assert authenticated_user.email == user_data["email"]
    assert authenticated_user.name == user_data["name"]

from auth import get_password_hash, verify_password, authenticate_user
from database import User

def test_get_password_hash():
    """
    RF1 - RN1: Verifica se a função de hash de senha está funcionando corretamente.
    """
    password = "senha_segura123"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert hashed_password.startswith("$2b$")  # Verifica se é um hash bcrypt

def test_verify_password():
    """
    RF1 - RN1: Testa a verificação de senha com senha correta e incorreta.
    """
    password = "senha_segura123"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) == True
    assert verify_password("senha_errada", hashed_password) == False

def test_authenticate_user_success(db_session):
    """
    RF2 - RN2: Testa a autenticação de usuário com credenciais corretas.
    """
    # Criar usuário de teste
    password = "senha_teste123"
    user = User(email="felipe@test.com", password=get_password_hash(password))
    db_session.add(user)
    db_session.commit()

    # Testar autenticação bem-sucedida
    authenticated_user = authenticate_user("felipe@test.com", password, db_session)
    assert authenticated_user == user

def test_authenticate_user_wrong_password(db_session):
    """
    RF2 - RN2: Testa a autenticação de usuário com senha incorreta.
    """
    # Criar usuário de teste
    password = "senha_teste123"
    user = User(email="felipe@test.com", password=get_password_hash(password))
    db_session.add(user)
    db_session.commit()

    # Testar autenticação com senha errada
    authenticated_user = authenticate_user("felipe@test.com", "senha_errada", db_session)
    assert authenticated_user == False

def test_authenticate_user_nonexistent(db_session):
    """
    RF2 - RN2: Testa a autenticação com um usuário que não existe.
    """
    # Testar autenticação com usuário inexistente
    authenticated_user = authenticate_user("inexistente@test.com", "senha123", db_session)
    assert authenticated_user == False

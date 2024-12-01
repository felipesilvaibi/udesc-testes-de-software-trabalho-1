# test_auth.py

from auth import get_password_hash, verify_password


def test_get_password_hash_valid_password():
    """
    CT001: Garantir geração de hash para senha válida
    Entradas:
        Senha: "senha_segura123"
    Resultado Esperado:
        O hash gerado é diferente da senha original
    Pós-condições:
        Nenhum
    """
    # Arrange (Preparação)
    password = "senha_segura123"

    # Act (Ação)
    hashed_password = get_password_hash(password)

    # Assert (Verificação)
    assert hashed_password != password


def test_get_password_hash_empty_password():
    """
    CT002: Garantir geração de hash para senha vazia
    Entradas:
        Senha: "" (string vazia)
    Resultado Esperado:
        O sistema gera um hash válido (não deve retornar erro)
    Pós-condições:
        Nenhum
    """
    # Arrange (Preparação)
    password = ""

    # Act (Ação)
    hashed_password = get_password_hash(password)

    # Assert (Verificação)
    assert hashed_password != password


def test_verify_password_correct():
    """
    CT005: Garantir correspondência de senha correta com hash
    Entradas:
        Senha: "senha_segura123"
        Hash correspondente à senha
    Resultado Esperado:
        A função retorna True
    Pós-condições:
        Nenhuma
    """
    # Arrange (Preparação)
    password = "senha_segura123"
    hashed_password = get_password_hash(password)

    # Act (Ação)
    result = verify_password(password, hashed_password)

    # Assert (Verificação)
    assert result is True


def test_verify_password_incorrect():
    """
    CT006: Garantir erro para senha incorreta com hash
    Entradas:
        Senha: "senha_errada"
        Hash correspondente a outra senha
    Resultado Esperado:
        A função retorna False
    Pós-condições:
        Nenhuma
    """
    # Arrange (Preparação)
    correct_password = "senha_correta"
    hashed_password = get_password_hash(correct_password)
    wrong_password = "senha_errada"

    # Act (Ação)
    result = verify_password(wrong_password, hashed_password)

    # Assert (Verificação)
    assert result is False

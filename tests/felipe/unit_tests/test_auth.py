# tests/felipe/unit_tests/test_auth.py

# Testes Unitários de Felipe para autenticação (RF1, RN1, RF2, RN2)

def test_register_user(client):
    # Teste para RF1 e RN1 (registro com dados válidos)
    response = client.post("/users/", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 201
    assert response.json()["msg"] == "Usuário registrado com sucesso"

def test_register_user_with_short_password(client):
    # Teste para RN1 (senha com menos de 8 caracteres)
    response = client.post("/users/", json={"email": "test2@example.com", "password": "short"})
    assert response.status_code == 422  # Erro de validação

def test_register_user_with_existing_email(client):
    # Teste para RN1 (e-mail já cadastrado)
    client.post("/users/", json={"email": "test3@example.com", "password": "password123"})
    response = client.post("/users/", json={"email": "test3@example.com", "password": "password123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "E-mail já cadastrado"

def test_login_with_correct_credentials(client):
    # Teste para RF2 e RN2 (login com credenciais corretas)
    client.post("/users/", json={"email": "test4@example.com", "password": "password123"})
    response = client.post("/users/login", data={"username": "test4@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_with_incorrect_password(client):
    # Teste para RN2 (senha incorreta)
    client.post("/users/", json={"email": "test5@example.com", "password": "password123"})
    response = client.post("/users/login", data={"username": "test5@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos"

def test_login_with_nonexistent_email(client):
    # Teste para RN2 (e-mail não cadastrado)
    response = client.post("/users/login", data={"username": "nonexistent@example.com", "password": "password123"})
    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos"

def test_register_with_invalid_email_format(client):
    # Teste para RN1 (e-mail inválido)
    response = client.post("/users/", json={"email": "invalidemail", "password": "password123"})
    assert response.status_code == 422  # Erro de validação

def test_login_without_password(client):
    # Teste para RF2 (login sem senha)
    client.post("/users/", json={"email": "test6@example.com", "password": "password123"})
    response = client.post("/users/login", data={"username": "test6@example.com", "password": ""})
    assert response.status_code == 401

def test_register_without_email(client):
    # Teste para RF1 (registro sem e-mail)
    response = client.post("/users/", json={"email": "", "password": "password123"})
    assert response.status_code == 422  # Erro de validação

def test_register_without_password(client):
    # Teste para RF1 (registro sem senha)
    response = client.post("/users/", json={"email": "test7@example.com", "password": ""})
    assert response.status_code == 422  # Erro de validação

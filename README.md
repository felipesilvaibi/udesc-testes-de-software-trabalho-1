# Gerenciador de Tarefas

Este é um projeto de um **Gerenciador de Tarefas** desenvolvido em **Python**, utilizando **FastAPI** para o backend. O sistema permite que usuários registrem-se, façam login, criem e gerenciem tarefas, além de compartilhar tarefas com outros usuários.

## Índice

*   [Descrição do Projeto](#descri%C3%A7%C3%A3o-do-projeto)

*   [Requisitos Funcionais e Regras de Negócio](#requisitos-funcionais-e-regras-de-neg%C3%B3cio)

*   [Funcionalidades](#funcionalidades)

*   [Tecnologias Utilizadas](#tecnologias-utilizadas)

*   [Estrutura do Projeto](#estrutura-do-projeto)

*   [Instalação e Execução](#instala%C3%A7%C3%A3o-e-execu%C3%A7%C3%A3o)

    *   [Gerenciando o Python e Pacotes com uv](#gerenciando-o-python-e-pacotes-com-uv)

    *   [Instalando Dependências](#instalando-depend%C3%AAncias)

*   [Testes](#testes)

*   [Autores](#autores)

## Descrição do Projeto

O Gerenciador de Tarefas é uma aplicação web que permite aos usuários administrar suas tarefas diárias de forma eficiente. Com funcionalidades que incluem criação, edição, exclusão, conclusão e compartilhamento de tarefas, o sistema visa melhorar a produtividade e organização pessoal.

## Requisitos Funcionais e Regras de Negócio

### RF1: Cadastro de Usuário

*   **RN1:** O usuário deve fornecer um **e-mail válido** e uma senha com **no mínimo 8 caracteres**.

### RF2: Login de Usuário

*   **RN2:** O login deve ser realizado com o **e-mail e senha** cadastrados.

### RF3: Criação de Tarefas

*   **RN3:** A tarefa deve ter um **título único**, descrição e data de vencimento.

### RF4: Edição de Tarefas

*   **RN4:** Apenas **tarefas não concluídas** podem ser editadas.

### RF5: Exclusão de Tarefas

*   **RN5:** Tarefas **concluídas não podem ser excluídas**.

### RF6: Marcar Tarefas como Concluídas

*   **RN6:** Ao concluir uma tarefa, deve-se registrar a **data de conclusão**.

### RF7: Listagem de Tarefas

*   **RN7:** O usuário pode **filtrar** tarefas por status (concluídas ou pendentes).

### RF8: Compartilhamento de Tarefas

*   **RN8:** O usuário pode **compartilhar** uma tarefa com outro usuário, permitindo visualização.

## Funcionalidades

*   **Registro de Usuários:** Permite que novos usuários se cadastrem no sistema fornecendo um e-mail e senha válidos.

*   **Autenticação de Usuários:** Login seguro utilizando e-mail e senha.

*   **Gerenciamento de Tarefas:**

    *   **Criação de Tarefas:** Crie novas tarefas com título único, descrição e data de vencimento.

    *   **Edição de Tarefas:** Edite tarefas que ainda não foram concluídas.

    *   **Exclusão de Tarefas:** Exclua tarefas que não foram concluídas.

    *   **Marcar como Concluída:** Marque tarefas como concluídas, registrando a data de conclusão.

*   **Listagem de Tarefas:**

    *   Visualize todas as suas tarefas.

    *   Filtre tarefas por status: pendentes ou concluídas.

*   **Compartilhamento de Tarefas:**

    *   Compartilhe suas tarefas com outros usuários registrados no sistema.

    *   Usuários compartilhados podem visualizar as tarefas.

## Tecnologias Utilizadas

*   **Python 3.12**

*   **FastAPI:** Framework web para o backend.

*   **SQLAlchemy:** ORM para interação com o banco de dados.

*   **SQLite:** Banco de dados relacional para armazenamento dos dados.

*   **Passlib:** Biblioteca para hashing de senhas.

*   **JWT (JSON Web Tokens):** Utilizado para autenticação e autorização.

*   **Uvicorn:** Servidor ASGI para executar a aplicação FastAPI.

*   **uv:** Gerenciador de pacotes e versões do Python escrito em Rust.

*   **pytest:** Framework para testes em Python.

## Estrutura do Projeto

```
- src/
  - main.py                # Aplicação FastAPI
  - database.py            # Modelos e configuração do banco de dados
  - auth.py                # Utilitários de autenticação
  - routers/
    - user.py              # Endpoints relacionados a usuários
    - task.py              # Endpoints relacionados a tarefas
- tests/
  - felipe/
    - unit_tests/
      - test_auth.py       # 10 Testes Unitários de Felipe
      - test_tasks.py
    - integration_tests/
      - test_integration.py  # 4 Testes de Integração de Felipe
    - conftest.py          # Configurações do pytest para Felipe
  - douglas/
    - unit_tests/
      - test_tasks.py      # 10 Testes Unitários de Douglas
    - integration_tests/
      - test_integration.py  # 4 Testes de Integração de Douglas
    - conftest.py          # Configurações do pytest para Douglas
- requirements.txt         # Dependências do projeto
- requirements-dev.txt     # Dependências de desenvolvimento (opcional)
- uv.lock                  # Arquivo de lock do uv
- .python-version          # Arquivo de versão do Python

```

## Instalação e Execução

### Gerenciando o Python e Pacotes com uv

Para garantir que você esteja usando a versão correta do Python (3.12) e gerenciar os pacotes do projeto, utilizaremos o **uv**, uma ferramenta rápida para gerenciamento de pacotes e versões do Python.

#### Instalando o uv

Você pode instalar o `uv` usando o script de instalação ou via `pip`.

**Instalação via script (recomendado):**

*   **No macOS e Linux:**

    ```
    curl -LsSf https://astral.sh/uv/install.sh | sh

    ```

*   **No Windows (PowerShell):**

    ```
    irm https://astral.sh/uv/install.ps1 | iex

    ```

**Instalação via pip:**

```
pip install uv

```

Após a instalação, você pode atualizar o `uv` para a versão mais recente com:

```
uv self update

```

#### Instalando o Python 3.12 com uv

```
uv python install 3.12.0

```

#### Definindo a Versão do Python para o Projeto

No diretório raiz do projeto, execute:

```
uv python pin 3.12.0

```

Isso criará um arquivo `.python-version` especificando a versão do Python a ser usada.

### Instalando Dependências

#### Criar e Ativar o Ambiente Virtual

Com o `uv`, podemos criar e ativar um ambiente virtual para o projeto:

```
uv venv

```

Isso criará um ambiente virtual utilizando a versão do Python especificada.

#### Instalando as Dependências do Projeto

Utilize o `uv` para instalar as dependências listadas no `requirements.txt`:

```
uv pip install -r requirements.txt

```

### Executando o Backend

1.  Inicie o servidor FastAPI com o Uvicorn:

    ```
    uv run uvicorn main:app --app-dir src --reload 

    ```

    O backend estará rodando em `http://localhost:8000`.

## Testes

### Executando os Testes com pytest

#### Testes de Felipe

*   **Executar todos os testes de Felipe:**

    ```
    pytest tests/felipe/

    ```

#### Testes de Douglas

*   **Executar todos os testes de Douglas:**

    ```
    pytest tests/douglas/

    ```

### Cobertura de Testes

Cada membro do grupo desenvolveu:

*   **10 Casos de Teste Unitários** utilizando no mínimo 4 RFs ou RNs.

*   **4 Casos de Teste de Integração** utilizando no mínimo 2 RFs ou RNs.

Os testes cobrem os requisitos funcionais e regras de negócio conforme especificado, garantindo a qualidade e confiabilidade do sistema.

## Autores

*   **Felipe**

    *   **Responsabilidades:**

        *   Implementação dos endpoints de registro e autenticação de usuários (`/register`, `/login`).

        *   Desenvolvimento das funcionalidades de criação e edição de tarefas.

        *   Desenvolvimento dos testes unitários e de integração correspondentes utilizando **pytest**.

*   **Douglas**

    *   **Responsabilidades:**

        *   Implementação dos endpoints de exclusão, conclusão e compartilhamento de tarefas.

        *   Desenvolvimento das funcionalidades de listagem e filtragem de tarefas.

        *   Desenvolvimento dos testes unitários e de integração correspondentes utilizando **pytest**.


# Gerenciador de Tarefas

Este é um projeto de um **Gerenciador de Tarefas** desenvolvido em **Python**, utilizando **FastAPI** para o backend. O sistema permite que usuários registrem-se, façam login, criem e gerenciem tarefas, além de compartilhar tarefas com outros usuários.

## Índice

1.  [Descrição do Projeto](#descri%C3%A7%C3%A3o-do-projeto)

2.  [Requisitos Funcionais e Regras de Negócio](#requisitos-funcionais-e-regras-de-neg%C3%B3cio)

3.  [Funcionalidades](#funcionalidades)

4.  [Tecnologias Utilizadas](#tecnologias-utilizadas)

5.  [Estrutura do Projeto](#estrutura-do-projeto)

6.  [Instalação e Execução](#instala%C3%A7%C3%A3o-e-execu%C3%A7%C3%A3o)

    *   [Gerenciando o Python e Pacotes com uv](#gerenciando-o-python-e-pacotes-com-uv)

    *   [Instalando Dependências](#instalando-depend%C3%AAncias)

    *   [Comandos Utilitários](#comandos-utilit%C3%A1rios)

7.  [Testes](#testes)

    *   [Executando os Testes com pytest](#executando-os-testes-com-pytest)

        *   [Testes de Unidade](#testes-de-unidade)

        *   [Testes de Integração](#testes-de-integra%C3%A7%C3%A3o)

    *   [Cobertura de Testes](#cobertura-de-testes)

        *   [Mapeamento dos Testes para RFs e RNs](#mapeamento-dos-testes-para-rfs-e-rns)

            *   [Felipe](#felipe)

            *   [Douglas](#douglas)

8.  [Autores](#autores)

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
      - test_felipe_auth.py       # 10 Testes Unitários de Felipe
      - test_felipe_tasks.py
      - conftest.py               # Configurações do pytest para Felipe
    - integration_tests/
      - test_felipe_integration.py  # 4 Testes de Integração de Felipe
  - douglas/
    - unit_tests/
      - test_douglas_tasks.py      # 10 Testes Unitários de Douglas
      - conftest.py                # Configurações do pytest para Douglas
    - integration_tests/
      - test_douglas_integration.py  # 4 Testes de Integração de Douglas
- Makefile                 # Comandos úteis do Makefile
- requirements.txt         # Dependências do projeto
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

Utilize o `Makefile` para instalar as dependências listadas no `requirements.txt`:

```
make install

```

### Executando o Backend

1.  Inicie o servidor FastAPI com o Uvicorn:

    ```
    make run

    ```

    O backend estará rodando em `http://localhost:8000`.

### 📂 Comandos Utilitários

Além dos comandos principais, você pode utilizar comandos utilitários para manter o projeto limpo e organizado.

#### Limpar Cache de Testes

Remova todos os diretórios `__pycache__` e arquivos `.pyc` para evitar conflitos de importação e garantir que os testes sejam executados com os arquivos mais recentes.

```
make clean-cache

```

***

## Testes

### Executando os Testes com pytest

#### Testes de Unidade

*   **Felipe:**

    Execute os testes unitários de Felipe:

    ```
    pytest tests/felipe/unit_tests/

    ```

*   **Douglas:**

    Execute os testes unitários de Douglas:

    ```
    pytest tests/douglas/unit_tests/

    ```

#### Testes de Integração

*   **Felipe:**

    Execute os testes de integração de Felipe:

    ```
    pytest tests/felipe/integration_tests/

    ```

*   **Douglas:**

    Execute os testes de integração de Douglas:

    ```
    pytest tests/douglas/integration_tests/

    ```

### Cobertura de Testes

Cada membro do grupo desenvolveu:

*   **10 Casos de Teste Unitários** utilizando no mínimo 4 RFs ou RNs.

*   **4 Casos de Teste de Integração** utilizando no mínimo 2 RFs ou RNs.

Os testes cobrem os requisitos funcionais e regras de negócio conforme especificado, garantindo a qualidade e confiabilidade do sistema.

#### Mapeamento dos Testes para RFs e RNs

##### Felipe

**Testes de Unidade:**

1.  `test_felipe_auth.py` - RF1 - RN1

2.  `test_felipe_tasks.py` - RF3 - RN3

3.  `test_create_task` - RF3 - RN3

4.  `test_complete_task` - RF5 - RN5

5.  `test_share_task` - RF5 - RN5

6.  `test_task_due_date` - RF3 - RN3

7.  `test_task_overdue` - RF7 - RN7

8.  `test_duplicate_task_title` - RF3 - RN3

9.  `test_shared_task_visibility` - RF5 - RN5

10. `test_unshare_task` - RF5 - RN5

**Testes de Integração:**

1.  `test_felipe_integration.py` - RF1 - RN1 e RF2 - RN2

2.  `test_create_task` - RF3 - RN3

3.  `test_share_task` - RF5 - RN5

4.  `test_list_tasks_shared` - RF5 - RN5

##### Douglas

**Testes de Unidade:**

1.  `test_douglas_tasks.py` - RF4 - RN4

2.  `test_edit_task` - RF4 - RN4

3.  `test_edit_completed_task` - RF4 - RN4

4.  `test_delete_task` - RF5 - RN5

5.  `test_delete_completed_task` - RF5 - RN5

6.  `test_list_tasks_with_filter` - RF7 - RN7

7.  `test_list_tasks_with_filter_pending` - RF7 - RN7

8.  `test_share_task_douglas` - RF8 - RN8

9.  `test_unshare_task_douglas` - RF8 - RN8

10. `test_delete_shared_task_douglas` - RF5 - RF8

**Testes de Integração:**

1.  `test_douglas_integration.py` - RF1 - RN1 e RF2 - RN2

2.  `test_edit_task` - RF4 - RN4

3.  `test_delete_task` - RF5 - RN5

4.  `test_list_tasks_owner` - RF7 - RN7

## Autores

*   **Felipe**

    *   **Responsabilidades:**

        *   **RF1 - RN1:** Implementação dos endpoints de registro de usuários (`/users/`).

        *   **RF2 - RN2:** Implementação dos endpoints de login de usuários (`/users/login`).

        *   **RF3 - RN3:** Desenvolvimento das funcionalidades de criação de tarefas.

        *   **RF5 - RN5:** Implementação das funcionalidades de exclusão de tarefas.

        *   **Testes:** Desenvolvimento de 10 testes unitários e 4 testes de integração relacionados aos requisitos acima.

*   **Douglas**

    *   **Responsabilidades:**

        *   **RF4 - RN4:** Implementação das funcionalidades de edição de tarefas.

        *   **RF6 - RN6:** Desenvolvimento das funcionalidades de marcação de tarefas como concluídas.

        *   **RF7 - RN7:** Desenvolvimento das funcionalidades de listagem e filtragem de tarefas.

        *   **RF8 - RN8:** Implementação das funcionalidades de compartilhamento de tarefas.

        *   **Testes:** Desenvolvimento de 10 testes unitários e 4 testes de integração relacionados aos requisitos acima.


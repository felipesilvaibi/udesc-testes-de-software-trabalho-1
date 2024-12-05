# UDESC Testes de Software - Trabalho 1

## Descrição

Este projeto, focado na automação de testes de unidade e testes de integração, é um Gerenciador de Tarefas desenvolvido em Python com FastAPI no backend. Ele oferece funcionalidades como registro de usuários, login, criação e compartilhamento de tarefas, garantindo a qualidade do sistema por meio de testes robustos. As ferramentas utilizadas incluem unittest, pytest, SQLAlchemy, SQLite e FastAPI TestClient, permitindo validar tanto componentes isolados quanto a integração entre diferentes partes do sistema.

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

## Requisitos Funcionais e Regras de Negócio

### RF1: Manter Usuários

#### RN1.1
O sistema deve permitir o cadastro de novos usuários, garantindo que a senha seja criptografada de forma unidirecional usando algoritmos seguros, como `bcrypt`.

#### RN1.2
O sistema deve validar as credenciais de login dos usuários, verificando se a senha fornecida corresponde ao hash armazenado de maneira segura.

### RF2: Manter Tarefas

#### RN2.1
Deve ser possível cadastrar novas tarefas, garantindo que o título seja único por usuário e rejeitando títulos duplicados, com mensagem de erro adequada.

#### RN2.2
O sistema deve permitir a exclusão de tarefas, garantindo que apenas tarefas não concluídas possam ser removidas, e que uma mensagem de erro seja exibida caso a tarefa não exista.

#### RN2.3
O sistema deve permitir a edição de tarefas pendentes, rejeitando alterações em tarefas concluídas ou inexistentes.

#### RN2.4
Deve ser possível marcar tarefas pendentes como concluídas, rejeitando qualquer tentativa de concluir uma tarefa já concluída ou inexistente.

#### RN2.5
O sistema deve permitir listar as tarefas do usuário, aplicando filtro por status (concluído ou pendente) ou sem filtro, retornando todos os registros disponíveis.

#### RN2.6
O sistema deve permitir que um usuário logado compartilhe suas tarefas com outros usuários, retornando erro caso a tarefa ou o usuário de destino não existam.

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
- tests/                   # Testes implementados
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

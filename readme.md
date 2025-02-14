# API de Empresas - Processo Seletivo

Este projeto foi desenvolvido para o processo seletivo. Ele consiste em uma API de gerenciamento de empresas, onde é possível cadastrar empresas, suas obrigações acessórias, e realizar operações de CRUD (Create, Read, Update, Delete).

## Tecnologias Utilizadas

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- pytest
- httpx

## 1. Configuração do Ambiente

### a. Criar o repositório no GitHub

Crie um repositório no GitHub e compartilhe o link público do repositório.

### b. Estrutura de Pastas

Coloque todos os arquivos na pasta raiz do repositório (sem criar subpastas).

### c. Criar um ambiente virtual

Crie um ambiente virtual com o comando:

```bash
python -m venv venv
```

Ative o ambiente virtual:

- No Windows:
    ```bash
    venv\Scripts\activate
    ```
- No Linux/MacOS:
    ```bash
    source venv/bin/activate
    ```

### d. Instalar as dependências necessárias

Instale as dependências com o comando:

```bash
pip install fastapi[all] sqlalchemy psycopg2 pydantic
```

## 2. Banco de Dados e Configuração

### a. Criar arquivo de configuração `.env`

Na raiz do projeto, crie um arquivo `.env` para armazenar as credenciais do banco de dados:

```bash
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
```

### b. Conexão com o banco de dados usando SQLAlchemy

A conexão com o banco é feita no arquivo `database.py`. O SQLAlchemy é utilizado para gerenciar a persistência das entidades no banco de dados.

### c. Criar o script de migração

Você pode usar o Alembic para gerar as migrações do banco de dados. Para isso, siga os passos abaixo:

1. Instale o Alembic:

    ```bash
    pip install alembic
    ```

2. Inicialize o Alembic no seu projeto:

    ```bash
    alembic init alembic
    ```

    Isso criará uma pasta `alembic/` com a configuração inicial.

3. Configure o arquivo `alembic.ini` com o caminho correto do banco de dados:

    Abra o arquivo `alembic.ini` e edite a variável `sqlalchemy.url` com a URL do seu banco de dados:

    ```ini
    sqlalchemy.url = postgresql://usuario:senha@localhost:5432/nome_do_banco
    ```

4. No arquivo `alembic/env.py`, adicione o seguinte código para configurar a migração com o SQLAlchemy:

    ```python
    from database import Base
    target_metadata = Base.metadata
    ```

5. Gere a migração com o comando:

    ```bash
    alembic revision --autogenerate -m "Criação das tabelas"
    ```

6. Aplique a migração no banco de dados com o comando:

    ```bash
    alembic upgrade head
    ```

Agora, suas tabelas serão criadas no banco de dados.

## 3. Modelagem de Dados (SQLAlchemy & Pydantic)

### a. Modelos

Os modelos de dados foram definidos usando SQLAlchemy para a persistência no banco de dados e Pydantic para a validação dos dados. O modelo `Empresa` representa as empresas e o modelo `ObrigacaoAcessoria` representa as obrigações acessórias associadas a uma empresa.

### b. Schemas

Os schemas Pydantic são utilizados para a entrada e saída de dados na API. Eles estão definidos no arquivo `schema.py`.

## 4. Implementação de CRUD de Empresa e Obrigação Acessória

A API oferece os seguintes endpoints para realizar operações de CRUD:

- **GET /empresas**: Retorna todas as empresas com suas obrigações acessórias.
- **GET /empresas/{empresa_id}**: Retorna os detalhes de uma empresa específica.
- **POST /empresas/**: Cadastra uma nova empresa.
- **PUT /empresas/{empresa_id}**: Atualiza os dados de uma empresa.
- **DELETE /empresa/{empresa_id}**: Deleta uma empresa.
- **POST /obrigacoes/**: Cadastra uma nova obrigação acessória para uma empresa.
- **PUT /obrigacoes/{obrigacao_id}**: Atualiza os dados de uma obrigação acessória.

## 5. Testes e Documentação

### a. Implementação de Testes Unitários

Os testes unitários foram implementados utilizando `pytest` e `httpx`. Eles testam os endpoints da API para garantir que tudo esteja funcionando corretamente.

#### Como rodar os testes

1. Instale o pytest:

    ```bash
    pip install pytest
    ```

2. Para rodar os testes, execute o seguinte comando:

    ```bash
    pytest
    ```

### b. Documentação da API

A documentação da API está disponível automaticamente no Swagger UI. Para acessá-la, basta iniciar o servidor e abrir o navegador em:

```
http://127.0.0.1:8000/docs
```

A documentação será gerada automaticamente a partir dos endpoints definidos no FastAPI.

## 6. Instruções Finais

- Para rodar a aplicação, execute:

    ```bash
    uvicorn main:app --reload
    ```

- A API estará disponível em `http://127.0.0.1:8000`.

- Para rodar as migrações e garantir que o banco esteja atualizado, use o Alembic conforme descrito anteriormente.

## Licença

Este projeto foi desenvolvido como parte de um processo seletivo e está sob a licença MIT.
```

Esse README contém as instruções detalhadas para configurar o ambiente, realizar migrações de banco de dados com Alembic, rodar os testes e utilizar a documentação Swagger gerada automaticamente pelo FastAPI.
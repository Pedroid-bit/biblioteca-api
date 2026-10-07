# Biblioteca Digital API

API REST para gerenciamento de biblioteca com FastAPI, SQLAlchemy e Alembic.

## Descrição do modelo de negócio

A biblioteca deseja controlar:
- usuários
- livros
- empréstimos

### Entidades
- Usuário
  - id
  - nome
  - email
  - telefone
  - criado_em

- Livro
  - id
  - titulo
  - autor
  - isbn
  - ano_publicacao
  - disponivel
  - usuario_id

- Empréstimo
  - id
  - livro_id
  - usuario_id
  - data_emprestimo
  - data_devolucao
  - status

### Relacionamentos
- Um usuário pode ter muitos livros cadastrados
- Um usuário pode ter vários empréstimos
- Um livro pode estar em vários empréstimos
- Um empréstimo pertence a um livro e a um usuário

### Diagrama textual

```text
Usuario 1 ─── N Livro
Usuario 1 ─── N Empréstimo
Livro   1 ─── N Empréstimo
```

## Requisitos
- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração do banco

Crie um arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
```

Se quiser, também pode deixar `DATABASE_URL` padrão como:

```env
DATABASE_URL=sqlite:///./biblioteca.db
```

## Migrações com Alembic

Crie a migration:

```bash
alembic revision --autogenerate -m "create initial tables"
```

Aplique a migration:

```bash
alembic upgrade head
```

## Executar a aplicação

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:
- Swagger: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## Endpoints implementados

### Usuários
- GET /usuarios
- GET /usuarios/{usuario_id}
- POST /usuarios
- PUT /usuarios/{usuario_id}
- DELETE /usuarios/{usuario_id}

### Livros
- GET /livros
- GET /livros/{livro_id}
- POST /livros
- PUT /livros/{livro_id}
- DELETE /livros/{livro_id}

### Empréstimos
- GET /emprestimos
- GET /emprestimos/{emprestimo_id}
- POST /emprestimos
- PUT /emprestimos/{emprestimo_id}
- PATCH /emprestimos/{emprestimo_id}/devolucao
- DELETE /emprestimos/{emprestimo_id}

## Tratamento de erros
- 201 Created para criação com sucesso
- 404 Not Found para registro inexistente
- 400 Bad Request para regras de negócio
- 422 Unprocessable Entity para dados inválidos

## Observações
- A criação do banco é feita exclusivamente via Alembic.
- A validação de relacionamento com chave estrangeira foi incluída ao criar empréstimos.

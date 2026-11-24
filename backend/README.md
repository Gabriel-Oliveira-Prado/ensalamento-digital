# Backend do Ensalamento Digital

API REST em Django responsável pelos cadastros, autenticação e regras de ensalamento do projeto.

## Requisitos

- Python 3.13
- PostgreSQL
- Git

## Instalação

No PowerShell, entre na pasta `backend` e crie o ambiente virtual:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Banco PostgreSQL

Crie o usuário e o banco usando o `psql` ou outra ferramenta de administração:

```sql
CREATE USER ensalamento WITH PASSWORD 'ensalamento';
CREATE DATABASE ensalamento OWNER ensalamento;
```

O PostgreSQL é o banco padrão. Configure as variáveis no PowerShell antes de iniciar o Django:

```powershell
$env:DJANGO_SECRET_KEY="uma-chave-local-segura"
$env:DATABASE_ENGINE="postgresql"
$env:POSTGRES_DB="ensalamento"
$env:POSTGRES_USER="ensalamento"
$env:POSTGRES_PASSWORD="ensalamento"
$env:POSTGRES_HOST="127.0.0.1"
$env:POSTGRES_PORT="5432"
```

O arquivo `.env.example` lista todas as variáveis aceitas. Ele é apenas uma referência: configure as variáveis no terminal, na IDE ou no serviço de hospedagem.

| Variável | Padrão | Uso |
| --- | --- | --- |
| `DATABASE_ENGINE` | `postgresql` | Use `postgresql` no projeto e `sqlite` somente em testes rápidos |
| `POSTGRES_DB` | `ensalamento` | Nome do banco |
| `POSTGRES_USER` | `ensalamento` | Usuário do banco |
| `POSTGRES_PASSWORD` | `ensalamento` | Senha do banco |
| `POSTGRES_HOST` | `127.0.0.1` | Servidor do PostgreSQL |
| `POSTGRES_PORT` | `5432` | Porta do PostgreSQL |
| `POSTGRES_CONN_MAX_AGE` | `60` | Tempo de reutilização das conexões em segundos |
| `POSTGRES_SSLMODE` | vazio | Use `require` quando a hospedagem exigir SSL |
| `DJANGO_SECRET_KEY` | chave insegura local | Chave do Django; deve ser definida fora do código em produção |

## Preparação do projeto

Com o PostgreSQL em execução e as variáveis configuradas:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

A API ficará disponível em `http://127.0.0.1:8000/`.

## Testes

Para executar rapidamente a suíte com um banco SQLite temporário:

```powershell
$env:DATABASE_ENGINE="sqlite"
python manage.py check
python manage.py test
```

Para validar a integração com PostgreSQL, mantenha `DATABASE_ENGINE=postgresql`, configure o banco de teste e execute o mesmo comando de testes.

## Rotas principais

- `POST /api/auth/token/` — login JWT
- `POST /api/auth/token/refresh/` — renovação do token
- `/api/usuarios/` — usuários
- `/api/ensalamento/` — cadastros e alocações
- `/api/schema/` — schema OpenAPI
- `/api/docs/` — Swagger UI
- `/api/redoc/` — ReDoc

## Estrutura

- `config/` — configurações e URLs do Django
- `contas/` — usuário customizado, autenticação e permissões
- `ensalamento/` — models, serializers, regras e endpoints do domínio
- `requirements.txt` — dependências Python

## Comandos úteis

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py check
python manage.py test
python manage.py spectacular --file openapi.yml --validate
```

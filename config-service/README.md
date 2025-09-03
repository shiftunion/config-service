# Config Service

Small FastAPI service managing applications and configurations with raw SQL (psycopg2) and a minimal migration runner.

## Requirements
- Python 3.13
- PostgreSQL 16
- uv (https://github.com/astral-sh/uv)

## Setup
1. Copy `.env.example` to `.env` and adjust DB settings.
2. Create the database in Postgres (DB_NAME from .env).
3. Apply migrations and run:

```sh
uv sync
make migrate
make dev
```

Service runs at http://localhost:8000, docs at /docs.

## Endpoints (base /api/v1)
- POST /applications
- PUT /applications/{id}
- GET /applications/{id}
- GET /applications

- POST /configurations
- PUT /configurations/{id}
- GET /configurations/{id}

## Testing
```sh
make test
```

All dependencies are strictly pinned in `pyproject.toml` per the plan.
# Config Service

FastAPI service to manage applications and their configurations. Persistence uses raw SQL via `psycopg2` with a lightweight SQL migration runner.

## Requirements
- Python 3.13
- PostgreSQL 16
- uv (https://github.com/astral-sh/uv)

## Project Structure
- `app/`:
  - `main.py`: FastAPI app factory and wiring
  - `api/routes/`: HTTP route handlers (FastAPI routers)
  - `core/`: runtime settings and utilities
  - `db/`: connection pool and SQL helpers
  - `models/`: pydantic request/response models
  - `repositories/`: database persistence (raw SQL)
  - `services/`: business logic and error translation
- `migrations.py`: simple migration CLI (status/up/verify)
- `migrations/*.sql`: ordered SQL migration files

## Configuration (env)
Set via `.env` (see `app/core/config.py` for defaults):
- `APP_ENV`: environment name (`dev`, etc.)
- `LOG_LEVEL`: log level (e.g., `INFO`, `DEBUG`)
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- `DB_POOL_MIN`, `DB_POOL_MAX`: psycopg2 threaded pool sizes

## Setup
1. Copy `.env.example` to `.env` and adjust DB settings.
2. Start the database with Docker (no API container):

```sh
make db-up      # builds image and starts Postgres
```

3. Install deps, apply migrations, and run the app:

```sh
uv sync
make migrate    # runs against the Dockerized DB
make dev
```

- App served at `http://localhost:8000`
- OpenAPI docs available at `/docs` and `/redoc`

## Endpoints (base `/api/v1`)
Applications
- `POST   /applications`
- `PUT    /applications/{id}`
- `GET    /applications/{id}`
- `GET    /applications`

Configurations
- `POST   /configurations`
- `PUT    /configurations/{id}`
- `GET    /configurations/{id}`

See `app/models/types.py` for request/response schemas.

## Migrations
Run status, apply pending, or verify checksums:

```sh
python -m config-service.migrations status
python -m config-service.migrations up
python -m config-service.migrations verify
```

`verify` returns non-zero when drift is detected.

## Docker helpers (DB only)
- `make db-build`: build the Postgres image that includes SQL migrations
- `make db-up`: start the DB and wait for health
- `make db-logs`: tail database logs
- `make db-down`: stop the DB (keeps volume)
- `make db-reset`: stop and remove volume (fresh init on next start)

Only the database is containerized. The API runs directly via `uvicorn`.

## Testing
```sh
make test
```

Dependencies are strictly pinned in `pyproject.toml`.

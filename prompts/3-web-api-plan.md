# Goals & Scope

Build a small, focused REST Web API for managing **applications** and their **configurations**, with exact tech and versions, explicit schema, raw SQL (no ORM), a lightweight migration system, and a tight test strategy. Endpoints are namespaced under `/api/v1`.

---

# Tech Stack (exact versions)

- **Python** 3.13.5  
- **FastAPI** 0.116.1  
- **Pydantic** 2.11.7 (validation + service config models)  
- **pytest** 8.4.1  
- **httpx** 0.28.1 (HTTP testing)  
- **PostgreSQL** v16  
- **psycopg2** 2.9.10  

All versions are **fixed** per spec; do not deviate.

> Important: treat version pinning as a **non-negotiable requirement** across `uv add` and lockfiles.

---

# Data Model & Schema

## Domain entities

- **Application**  
  - `id`: ULID (string) – PK  
  - `name`: string(256) – **unique**  
  - `comments`: string(1024)  
- **Configuration**  
  - `id`: ULID (string) – PK  
  - `application_id`: ULID (string) – FK → applications(id)  
  - `name`: string(256) – **unique per application**  
  - `comments`: string(1024)  
  - `config`: JSONB (KV dictionary)  

(Use ULIDs via `pydantic_extra_types.ulid.ULID`; store as text in Postgres.)

## SQL DDL (first migration proposal: `migrations/0001_init.sql`)

```sql
-- applications
CREATE TABLE applications (
  id TEXT PRIMARY KEY,
  name VARCHAR(256) NOT NULL UNIQUE,
  comments VARCHAR(1024)
);

-- configurations
CREATE TABLE configurations (
  id TEXT PRIMARY KEY,
  application_id TEXT NOT NULL REFERENCES applications(id),
  name VARCHAR(256) NOT NULL,
  comments VARCHAR(1024),
  config JSONB NOT NULL,
  CONSTRAINT configurations_unique_name_per_app UNIQUE (application_id, name)
);

-- helpful indexes
CREATE INDEX idx_configurations_app_id ON configurations(application_id);
```

> Notes  
> • ULID is stored as text; ULID validity is enforced at the **application layer** with Pydantic ULID parsing.  
> • We deliberately **avoid** extra columns (timestamps, soft-delete, etc.) because they’re not in scope.

---

# API Design

**Base path**: `/api/v1` (all endpoints below are relative to this).

## Applications
- **POST** `/applications`  
- **PUT** `/applications/{id}`  
- **GET** `/applications/{id}`  
- **GET** `/applications`  

## Configurations
- **POST** `/configurations`  
- **PUT** `/configurations/{id}`  
- **GET** `/configurations/{id}`  

### Status codes & errors
- `400` validation errors (Pydantic)
- `404` resource not found
- `409` uniqueness violations (`applications.name` or `(application_id,name)`)

---

# Architecture & Folder Structure

```
project-root/
├─ app/
│  ├─ main.py
│  ├─ api/
│  │  ├─ routes/
│  │  │  ├─ applications.py
│  │  │  └─ configurations.py
│  │  └─ deps.py
│  ├─ core/
│  │  ├─ config.py
│  │  └─ timeutils.py
│  ├─ db/
│  │  ├─ pool.py
│  │  └─ sql.py
│  ├─ models/
│  │  ├─ dto.py
│  │  └─ types.py
│  ├─ repositories/
│  │  ├─ applications_repo.py
│  │  └─ configurations_repo.py
│  └─ services/
│     ├─ applications_service.py
│     └─ configurations_service.py
├─ migrations/
│  ├─ 0001_init.sql
│  └─ ...
├─ migrations.py
├─ migrations_test.py
├─ Makefile
├─ .env.example
├─ pyproject.toml
└─ README.md
```

---

# Persistence & Concurrency

- **No ORM**.  
- **Connection pooling**: `psycopg2.pool.ThreadedConnectionPool`.  
- **Async compatibility**: `concurrent.futures.ThreadPoolExecutor` + `contextlib.asynccontextmanager`.  
- **Cursor**: `psycopg2.extras.RealDictCursor`.  
- **IDs**: ULID via `pydantic_extra_types.ulid.ULID`.

---

# Validation & DTOs

- Define Pydantic models for requests and responses.  
- Use ULID type from `pydantic_extra_types.ulid`.  
- Validate lengths: `name` (≤256), `comments` (≤1024).  
- Validate `config` as `dict[str, Any]`.

---

# Migrations

- SQL files in `migrations/` folder.  
- `migrations` table to track applied migrations.  
- `migrations.py` CLI with `status`, `up`, `verify`.  
- `migrations_test.py` to cover bootstrap, apply, idempotency, checksum drift.

---

# Endpoint Behavior Details

**Applications**
- POST/PUT with validation, uniqueness enforcement.  
- GET by ID returns related configuration IDs.  
- GET list returns all.

**Configurations**
- POST validates `application_id` existence.  
- PUT updates fields except `application_id`.  
- GET returns full config.

---

# Error Handling & Mapping

- Unique violation → 409 Conflict.  
- FK violation → 400 Bad Request.  
- FastAPI `HTTPException` for client-safe errors.

---

# Dates & Times

- Use only stdlib (`datetime`, `time`).  
- Validate against latest Python docs.

---

# Configuration

- `.env` with DB config, pool sizes, log level.  
- Use `pydantic-settings (>=2,<3)`.

---

# Developer Experience

- Use `uv` for deps and execution.  
- **Makefile** with `run`, `dev`, `test`, `migrate`, `status`.  
- All commands invoke via `uv run`.

---

# Testing Strategy

- Unit tests for every code file.  
- Co-located `*_test.py` files.  
- Focus on ~80% of critical scenarios.  
- `test/` folder only if needed for helpers/mocks.

---

# Logging

- Python stdlib logging.  
- Level from `.env`.

---

# Security / Auth

- Out of scope (future feature).

---

# Acceptance Criteria

1. Endpoints behave per spec.  
2. Schema matches exactly.  
3. Raw SQL via psycopg2.  
4. Migrations system implemented.  
5. Tests cover 80% critical paths.  
6. `.env` via pydantic-settings.  
7. Versions pinned.  

---

# Next Actions

1. Initialize repo & deps with `uv`.  
2. Create `migrations/0001_init.sql`; implement migration runner.  
3. Implement config + db pool.  
4. Add DTOs, repos, services, routers.  
5. Add unit tests.  
6. Wire Makefile targets and verify.

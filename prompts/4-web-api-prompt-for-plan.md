# GitHub Copilot Execution Prompts

This document contains step-by-step prompts you can provide to **GitHub Copilot Agent** (Agent mode) to execute the implementation plan for the Web API. It also includes some **Edit mode** one-liners for working inside individual files.

---

## Agent mode — step-by-step prompts

### 0) Preflight (run first)
> You are GitHub Copilot Agent. Read `prompts/2-web-api-prompt.md` and strictly follow it. Do **not** add any dependency that is not listed (e.g., no uvicorn) unless I explicitly approve. Use Python 3.13.5, FastAPI 0.116.1, Pydantic 2.11.7, pytest 8.4.1, httpx 0.28.1, psycopg2 2.9.10, PostgreSQL 16. Confirm the ordered plan of actions you’ll take and any assumptions you need me to approve.

### 1) Initialize project & deps with uv (no extras)
> Initialize a `uv` project for Python 3.13.5 and add only these packages with exact constraints:  
> `fastapi==0.116.1 pydantic==2.11.7 pydantic-settings>=2,<3 psycopg2==2.9.10 pydantic-extra-types python-ulid>=2,<3 pytest==8.4.1 httpx==0.28.1`  
> Do not add uvicorn or any other package. Show me the resulting `pyproject.toml`.

### 2) Create folders & empty files
> Create this structure with empty files (stubs where noted):
```
app/
  main.py
  api/routes/applications.py
  api/routes/configurations.py
  api/deps.py
  core/config.py
  core/timeutils.py
  db/pool.py
  db/sql.py
  models/dto.py
  models/types.py
  repositories/applications_repo.py
  repositories/configurations_repo.py
  services/applications_service.py
  services/configurations_service.py
migrations/
  0001_init.sql
migrations.py
migrations_test.py
Makefile
.env.example
README.md
```
> Populate each file with minimal scaffolding per the prompt; keep code compiling.

### 3) Migrations system
> Implement `migrations/0001_init.sql` with the two tables, uniqueness constraints, and helpful index per the prompt.  
> Implement `migrations.py` with commands `status`, `up`, `verify`. Use psycopg2, `migrations` table (filename, checksum, applied_at), transactional apply, checksum drift detection. No external libs. Show me the code.

### 4) Settings & env
> Implement `app/core/config.py` using `pydantic-settings (>=2,<3)` to parse `.env` values: `DATABASE_URL`, `DB_MIN_CONN`, `DB_MAX_CONN`, `LOG_LEVEL`. Produce `.env.example` with placeholders.

### 5) DB pool & concurrency glue
> Implement `app/db/pool.py`:  
> - `ThreadedConnectionPool` from psycopg2, initialized from settings  
> - `@asynccontextmanager` `db_conn()` yielding a cursor with `RealDictCursor`  
> - commit/rollback on exit, always return connection to pool  
> - use `ThreadPoolExecutor` for blocking DB ops through `asyncio.run_in_executor` helpers  
> Provide small helpers in `app/db/sql.py` for running queries and mapping `UniqueViolation`/FK errors.

### 6) DTOs & types
> In `app/models/types.py`, define a `ULIDStr` type using `pydantic_extra_types.ulid.ULID` (serialize to str).  
> In `app/models/dto.py`, add request/response models enforcing lengths: `name<=256`, `comments<=1024`, `config: dict[str, Any]`.

### 7) Repositories
> Implement `applications_repo.py` and `configurations_repo.py` using **raw SQL** only:  
> - applications: insert (ULID assigned in service), update, get by id, list all  
> - configurations: insert, update, get by id  
> - enforce uniqueness and FK via SQL; raise typed errors mapped in `db/sql.py`.

### 8) Services
> Implement services to orchestrate repos, convert DB rows to DTOs, and map psycopg2 errors to domain errors used by the API layer.

### 9) FastAPI wiring
> Implement `app/main.py` with an app factory and include routers under `/api/v1`.  
> Implement `api/routes/applications.py` and `configurations.py` with POST/PUT/GET endpoints exactly as specified, including returning `configuration_ids` in `GET /applications/{id}`. Use dependency for `db_conn()`.

### 10) Makefile (no uvicorn by default)
> Create `Makefile` with targets `run`, `test`, `migrate`, `status`.  
> - `run`: `uv run python -m app.main`  
> - `test`: `uv run python -m pytest -q`  
> - `migrate`: `uv run python migrations.py up`  
> - `status`: `uv run python migrations.py status`  
> Add a commented `dev` target that would use uvicorn for autoreload, but **do not** add uvicorn without my approval.

### 11) Tests (co-located)
> For every non-`__init__` file, add a `*_test.py` next to it focusing on ~80% of important scenarios. Use `httpx` for endpoint tests and a dedicated test DB. Include `migrations_test.py` for bootstrap/apply/idempotency/checksum. Show me a summary of created tests.

### 12) Run & verify
> Provide commands in order: `uv sync`, set up test DB, `make migrate`, `make test`, then `make run`.  
> Then show sample curl requests for each endpoint and expected JSON. Confirm acceptance criteria are met.

---

## Edit mode — handy one-liners

Use these when working inside a single file in **Edit mode**.

### app/db/pool.py
> Implement a `ThreadedConnectionPool`‐backed `@asynccontextmanager db_conn()` that yields a `RealDictCursor`. Ensure commit/rollback on exit and connection is returned to the pool. Add `run_query(sql, params)` and `run_queryrow(sql, params)` helpers that execute in a `ThreadPoolExecutor` via `asyncio.get_running_loop().run_in_executor`.

### migrations.py
> Add an argparse CLI with `status|up|verify`. Create `migrations` table if missing, compute SHA256 checksums for `migrations/*.sql`, apply pending migrations in filename order with per-file transactions, and implement drift detection if checksum changes. Print a clear table of applied/pending.

### api/routes/applications.py
> Add endpoints: POST/PUT/GET(id)/GET(list) under `/api/v1/applications`. Use DTOs, ULID generation in service, and ensure `GET(id)` returns `{..., "configuration_ids": [ulid, ...]}` from a second query.

### repositories/applications_repo.py
> Implement SQL for insert/update/get/list using placeholders, `RETURNING` clauses, and map `UniqueViolation` to a custom error consumed by the service.

---

## Optional: dev autoreload
If you want hot-reload later, say to Agent:
> Requesting approval to add `uvicorn` strictly for dev autoreload. If approved, add `uvicorn>=0.30,<1` and enable the `dev` Makefile target: `uv run uvicorn app.main:app --reload`.

UV=uv

# Load .env for targets that need raw env (migrations). The app itself reads
# .env via pydantic-settings, so run/dev don't require this.

.PHONY: run dev test migrate status fmt db-build db-up db-down db-logs db-reset setup

run:
	$(UV) run uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
	$(UV) run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(UV) run pytest

migrate:
	bash -lc 'set -a; [ -f .env ] && source .env; set +a; $(UV) run python migrations.py up'

status:
	bash -lc 'set -a; [ -f .env ] && source .env; set +a; $(UV) run python migrations.py status'

# --- Dockerized Postgres (DB only) ---
db-build:
	docker compose -f docker-compose.yml build db

db-up:
	docker compose -f docker-compose.yml up -d db
	@echo "Waiting for database to become healthy..." && \
	for i in $$(seq 1 40); do \
	  status=$$(docker inspect -f '{{ .State.Health.Status }}' config-db 2>/dev/null || echo starting); \
	  if [ "$$status" = "healthy" ]; then echo "DB is healthy"; exit 0; fi; \
	  sleep 1; \
	done; \
	echo "DB not healthy yet; continuing. You can run 'make status' to retry migrations.";

db-logs:
	docker compose -f docker-compose.yml logs -f db

db-down:
	docker compose -f docker-compose.yml down

db-reset:
	docker compose -f docker-compose.yml down -v

# Bring up DB, apply migrations, then run dev
setup:
	uv sync
	$(MAKE) db-up
	$(MAKE) migrate
	$(MAKE) dev

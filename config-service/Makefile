UV=uv

# Load .env for targets that need raw env (migrations). The app itself reads
# .env via pydantic-settings, so run/dev don't require this.

.PHONY: run dev test migrate status fmt

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

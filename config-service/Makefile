UV=uv

.PHONY: run dev test migrate status fmt

run:
	$(UV) run uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
	$(UV) run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(UV) run pytest

migrate:
	$(UV) run python migrations.py up

status:
	$(UV) run python migrations.py status

.PHONY: help run dev test migrate status verify install clean

# Default target
help:
	@echo "Available targets:"
	@echo "  install    Install dependencies"
	@echo "  run        Run the application"
	@echo "  dev        Run in development mode"
	@echo "  test       Run tests"
	@echo "  migrate    Apply database migrations"
	@echo "  status     Show migration status"
	@echo "  verify     Verify migrations"
	@echo "  clean      Clean up"

# Install dependencies
install:
	uv sync

# Run the application
run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run in development mode
dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	uv run python -m pytest

# Apply migrations
migrate:
	uv run python migrations.py up

# Show migration status
status:
	uv run python migrations.py status

# Verify migrations
verify:
	uv run python migrations.py verify

# Clean up
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

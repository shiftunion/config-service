# Config Service API

A REST API for managing applications and their configurations, built with FastAPI and PostgreSQL.

## Features

- RESTful API for managing applications and configurations
- PostgreSQL database with raw SQL queries (no ORM)
- ULID-based identifiers
- Async database operations with connection pooling
- Comprehensive validation with Pydantic
- Migration system with checksum verification
- Docker-ready setup

## Tech Stack

- **Python**: 3.13.5
- **FastAPI**: 0.116.1
- **PostgreSQL**: 16
- **Pydantic**: 2.11.7
- **psycopg2**: 2.9.10

## API Endpoints

### Applications (`/api/v1/applications`)

- `POST /` - Create new application
- `GET /{id}` - Get application by ID
- `PUT /{id}` - Update application
- `GET /` - List all applications

### Configurations (`/api/v1/configurations`)

- `POST /` - Create new configuration
- `GET /{id}` - Get configuration by ID
- `PUT /{id}` - Update configuration

## Getting Started

### Prerequisites

- Python 3.13.5+
- PostgreSQL 16
- uv package manager

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   make install
   ```

3. Set up environment variables (copy `.env.example` to `.env`):
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. Run database migrations:
   ```bash
   make migrate
   ```

### Running the Application

```bash
# Development mode
make dev

# Production mode
make run
```

The API will be available at `http://localhost:8000`

## Database Schema

### Applications
- `id`: ULID (Primary Key)
- `name`: VARCHAR(256) UNIQUE
- `comments`: VARCHAR(1024)

### Configurations
- `id`: ULID (Primary Key)
- `application_id`: ULID (Foreign Key)
- `name`: VARCHAR(256)
- `comments`: VARCHAR(1024)
- `config`: JSONB

Unique constraint: `(application_id, name)`

## Development

### Running Tests

```bash
make test
```

### Migration Commands

```bash
make status    # Show migration status
make migrate   # Apply pending migrations
make verify    # Verify migration checksums
```

### Project Structure

```
config-service-b/
├── app/
│   ├── core/           # Core functionality
│   ├── db/             # Database utilities
│   ├── models/         # Pydantic models
│   ├── repositories/   # Data access layer
│   ├── services/       # Business logic
│   └── api/            # FastAPI routers
├── migrations/         # Database migrations
├── tests/              # Unit tests
├── pyproject.toml      # Project configuration
├── Makefile           # Development commands
└── README.md
```

## License

This project is licensed under the MIT License.

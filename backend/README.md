# SmartSpace AI Backend

FastAPI backend for the existing SmartSpace AI frontend. The frontend remains unchanged.

## Run Locally

1. Copy environment:

```powershell
copy .env.example .env
```

2. Start services:

```powershell
docker compose up --build
```

3. API docs:

```text
http://localhost:8000/docs
```

## Development Without Docker

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install ".[dev]"
uvicorn app.main:app --reload
```

## First Modules Implemented

- JWT authentication
- RBAC dependencies
- Users
- Spaces
- Bookings
- Search
- AI placeholder job creation
- Admin/analytics/payment/upload route surfaces

## Database

The SQL schema is available at:

```text
../outputs/smartspace_schema.sql
```

Alembic is configured for SQLAlchemy models and future migrations.

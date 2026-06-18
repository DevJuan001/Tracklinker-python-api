---
name: development-workflow
description: Use when running the API, the Celery worker, the test suite, adding dependencies, building the Docker image, or auditing for vulnerabilities. Covers the uv workflow, the Windows-specific Celery flag, the test layout, and the standard pre-commit checks.
---

# Development Workflow Skill

Tracklinker uses `uv` for environment + dependency management, `pytest` for tests, `Celery + Redis` for background tasks, and `Docker` for production images.

## First-time setup

```bash
# 1. Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install uv (Windows PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Clone and enter
git clone https://github.com/DevJuan001/Tracklinker-python-api.git
cd Tracklinker-python-api

# 3. Create venv and install dependencies
uv venv
uv sync

# 4. Activate the venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 5. Copy environment template
cp .env.example .env       # macOS / Linux
copy .env.example .env     # Windows
# Edit .env and fill every variable (validated by pydantic-settings at startup)

# 6. Run the SQL scripts in order
mysql -u root -p < database/01_database.sql
mysql -u root -p < database/02_dml.sql
mysql -u root -p < database/03_views.sql
```

## Running the API (development)

```bash
uvicorn app.main:app --reload
```

URLs:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/
- DB ping: http://localhost:8000/ping-db

## Running the Celery worker

In a **second terminal** with the venv active:

```bash
# Windows (REQUIRED: --pool=solo)
celery -A app.core.celery_app.celery worker --loglevel=info --pool=solo

# macOS / Linux
celery -A app.core.celery_app.celery worker --loglevel=info
```

The two registered tasks live in `app/tasks/email_tasks.py`:
- `send_welcome_email` — fired when an Admin creates a new user.
- `recovery_password_email` — fired by `POST /api/auth/recover-password`.

Both have `bind=True, max_retries=3` and retry with a 60-second countdown.

## Adding a dependency

```bash
# Always use uv, never edit pyproject.toml by hand
uv add <paquete>

# Dev-only dependency
uv add --dev <paquete>
```

This updates `pyproject.toml` and `uv.lock` together.

## Running tests

```bash
# All tests
pytest

# Only unit tests
pytest test/unit/

# Only BDD tests
pytest test/bdd/

# Single file
pytest test/unit/test_user_models.py -v
```

The test layout is:

```
test/
├── conftest.py        # shared fixtures (currently empty — populate when tests are added)
├── unit/              # fast, isolated tests
└── bdd/               # behavior-driven tests (e.g. test_flujo_auth.py)
```

Both directories exist but are empty (`0 lines`). When adding tests, follow pytest conventions and use fixtures from `conftest.py` for the database / app instance.

## Linting and security

```bash
# Install dev tools (already in pyproject.toml)
uv sync

# Audit dependencies for known vulnerabilities
pip-audit
```

There is **no** `ruff` or `flake8` configuration checked in. If you add one, keep it minimal — the project relies on conventions documented in the `code-conventions` skill rather than aggressive autoformatting.

## Docker

```bash
# Build
docker build -t tracklinker-api .

# Run (passes .env to the container)
docker run -p 8000:8000 --env-file .env tracklinker-api
```

The `Dockerfile`:
- Base: `python:3.13-slim`.
- Installs `uv` from `ghcr.io/astral-sh/uv:latest`.
- Runs `uv sync --frozen --no-dev` (no dev dependencies in the image).
- Starts `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

## Pre-commit checklist

Before opening a PR:

1. `uv sync` (deps in sync).
2. `pytest` (all tests pass — even if there are none, the command must exit 0).
3. `pip-audit` (no high-severity CVEs).
4. Manually smoke-test the touched endpoints via `http://localhost:8000/docs`.
5. If you touched SQL, run the matching `find_*` query manually in MySQL Workbench / CLI to confirm the result shape.
6. If you added a feature, follow the architecture rule: service → repository only, never service → service.

## Common pitfalls

- **Forgot to activate the venv**: `uvicorn` not found. Run `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/macOS).
- **Celery worker crashes on Windows**: missing `--pool=solo`. Always add it on Windows.
- **JWT errors after changing `ACCESS_TOKEN_SECRET_KEY`**: existing cookies become invalid; users must log in again.
- **CORS error in the browser**: the origin isn't in the allow-list in `app/main.py`. Add it.
- **Rate limit hit during testing**: lower the threshold temporarily or clear Redis with `FLUSHDB` (dev only).

## Reference paths

- `pyproject.toml` — deps, metadata.
- `uv.lock` — pinned versions.
- `Dockerfile` — image build.
- `.env.example` — env template.
- `app/main.py` — FastAPI app, lifespan, CORS, router registration.
- `app/core/celery_app.py` — Celery configuration.
- `app/tasks/email_tasks.py` — Celery tasks.
- `test/conftest.py` — pytest fixtures.
- `database/01_database.sql` — DDL.

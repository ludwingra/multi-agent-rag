# Developer Environment Setup — TechNova Solutions

**Owner:** Engineering Platform Team | **Last Updated:** 2025-10-12 | **Applies To:** All Software Engineers

---

## Overview

This guide covers the complete local development environment setup for contributing to the **FlowEngine** platform. It assumes your laptop is already configured per the [Laptop Setup Guide](laptop-setup.md) and that you have VPN and GitHub access per [VPN Setup Guide](vpn-setup-guide.md) and [GitHub Access](github-access.md).

---

## Repositories

| Repository | Description | Clone URL |
|------------|-------------|-----------|
| `flowengine-core` | Backend Python services (FastAPI + Celery) | `git@github.technova.io:technova-engineering/flowengine-core.git` |
| `flowengine-frontend` | React/TypeScript UI | `git@github.technova.io:technova-engineering/flowengine-frontend.git` |
| `flowengine-infra` | Terraform, Helm charts, K8s manifests | `git@github.technova.io:technova-platform/flowengine-infra.git` |
| `flowengine-api-specs` | OpenAPI 3.1 specs | `git@github.technova.io:technova-engineering/flowengine-api-specs.git` |

---

## Backend Setup (Python / FastAPI)

### Clone and Install

```bash
git clone git@github.technova.io:technova-engineering/flowengine-core.git
cd flowengine-core

# Create virtual environment (Python 3.12 required)
pyenv local 3.12.4
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Install pre-commit hooks (runs Ruff, detect-secrets, mypy on each commit)
pre-commit install
```

### Environment Variables

Copy the example env file and populate it using values from the **FlowEngine Dev** vault in 1Password:

```bash
cp .env.example .env
# Edit .env — retrieve secrets from 1Password vault "FlowEngine Dev"
# Required keys: DATABASE_URL, REDIS_URL, AWS_REGION, SECRET_KEY, OKTA_CLIENT_ID
```

**Never commit `.env` to version control.** It is in `.gitignore` by default.

### Local Database with Docker Compose

```bash
# Start PostgreSQL 16 and Redis 7.2 locally
docker compose up -d postgres redis

# Run migrations
alembic upgrade head

# Seed development data
python scripts/seed_dev_data.py

# Verify
psql postgresql://flowengine:secret@localhost:5432/flowengine_dev -c "\dt"
```

### Run the API Server

```bash
# Development mode with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using the Makefile shortcut
make dev
```

API available at [http://localhost:8000](http://localhost:8000). Interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Frontend Setup (React / TypeScript)

```bash
git clone git@github.technova.io:technova-engineering/flowengine-frontend.git
cd flowengine-frontend

# Use Node 20 (via nvm)
nvm use 20

# Install dependencies
npm install

# Copy env file
cp .env.local.example .env.local
# Set NEXT_PUBLIC_API_URL=http://localhost:8000

# Start dev server
npm run dev
# Available at http://localhost:3000
```

### Type Checking and Linting

```bash
# Type check
npx tsc --noEmit

# Lint
npx eslint src/ --max-warnings=0

# Format
npx prettier --write src/
```

---

## Running Tests

### Backend

```bash
# All tests
pytest -v

# Specific module
pytest tests/unit/test_webhook_service.py -v

# With coverage report
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Integration tests (requires Docker services running)
pytest tests/integration/ -v --timeout=30
```

### Frontend

```bash
# Unit tests (Jest + React Testing Library)
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

---

## Database Migrations

Refer to [Database Access](database-access.md) for the full migration guide. Quick reference:

```bash
# Create migration from model changes
alembic revision --autogenerate -m "describe_your_change"

# Apply to local dev DB
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Local Kubernetes (Optional — Advanced)

For testing Kubernetes-specific behavior locally:

```bash
# Install kind (Kubernetes in Docker)
brew install kind

# Create local cluster
kind create cluster --name technova-local --config k8s/kind-config.yaml

# Load local image
kind load docker-image flowengine-api:local --name technova-local

# Deploy using Helm
helm upgrade --install flowengine-api helm/flowengine-api \
  --values helm/flowengine-api/values.local.yaml \
  --namespace flowengine --create-namespace
```

---

## Useful Make Targets

```bash
make dev          # Start backend dev server
make test         # Run all backend tests
make lint         # Run Ruff + mypy
make migrate      # Run Alembic migrations
make seed         # Seed dev database
make docker-up    # Start Docker Compose services
make docker-down  # Stop Docker Compose services
```

---

## FAQ

**Q: I get `ModuleNotFoundError` after installing requirements.**
A: Ensure your virtual environment is activated (`source .venv/bin/activate`) and that you installed into it (`pip install -r requirements.txt`).

**Q: Docker Compose fails with "port already in use".**
A: Check for conflicting processes: `lsof -i :5432` (PostgreSQL) or `lsof -i :6379` (Redis). Stop the conflicting process and retry.

**Q: Pre-commit hooks are blocking my commit.**
A: Run `pre-commit run --all-files` to see all issues, fix them, then re-commit. Do not skip hooks with `--no-verify` — this will fail CI anyway.

**Q: Where do I find the development API keys for third-party services?**
A: All dev secrets are in 1Password under the **FlowEngine Dev** vault. Request access via your manager if you don't see it.

---

## Related Documents

- [Laptop Setup Guide](laptop-setup.md)
- [GitHub Access](github-access.md)
- [Database Access](database-access.md)
- [CI/CD Pipeline](ci-cd-pipeline.md)
- [API Documentation Standards](api-documentation-standards.md)

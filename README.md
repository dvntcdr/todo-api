## ☑️ FastAPI Todo API

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/FastAPI-0.135.2-cyan?logo=fastapi&logoColor=cyan" />
    <img src="https://img.shields.io/badge/SQLAlchemy-2.0.48-red?logo=sqlalchemy&logoColor=white" />
    <img src="https://img.shields.io/badge/Alembic-1.18.4-cyan" />
    <img src="https://img.shields.io/badge/SQLite-dev-blue?logo=sqlite&logoColor=white" />
    <img src="https://img.shields.io/badge/PostgreSQL-18-blue?logo=postgresql&logoColor=white" />
    <img src="https://img.shields.io/badge/Redis-8-red?logo=redis&logoColor=white" />
    <img src="https://img.shields.io/badge/Celery-5.6.3-lime?logo=celery&logoColor=white" />
    <img src="https://img.shields.io/badge/RabbitMQ-4.0-orange?logo=rabbitmq&logoColor=white" />
    <img src="https://img.shields.io/badge/uv-package%20manager-red?logo=uv&logoColor=white" />
    <img src="https://img.shields.io/badge/MIT-license-green" />
</p>

---

# 🚀 Todo API

REST API for managing tasks, projects, users and memberships.

Built with modern Python tools and a clean layered architecture.

## 📦 Tech Stack

**Framework & API**
- **FastAPI** — web framework
- **Pydantic** — data validation & settings management
- **slowapi** — rate limiting

**Database**
- **SQLAlchemy** — async ORM
- **Alembic** — database migrations
- **PostgreSQL** — primary database
- **SQLite** — development & testing database

**Caching & Messaging**
- **Redis** — caching
- **Celery** — async task queue
- **RabbitMQ** — message broker

**Auth & Security**
- **python-jose** — JWT tokens
- **pwdlib (Argon2)** — password hashing

**Email**
- **fastapi-mail** — email sending

**Testing**
- **Pytest** — unit & integration testing
- **factory-boy** — test data factories
- **fakeredis** — Redis mock for tests

**Tooling**
- **uv** — package manager
- **Docker Compose** — local development environment

## 🔍 Features

- JWT authentication (access + refresh tokens)
- Email verification on signup
- Password reset via email
- User management
- Projects & task management
- Membership / role-based access
- Async email sending via Celery
- Redis caching
- Rate limiting
- Logging
- Database migrations
- Unit and integration tests

## ⚡ Getting Started

### Requirements

- Python 3.14+
- Docker + Docker Compose
- uv

### Install dependencies

```bash
uv sync
```

### Start services

```bash
docker compose up -d
```

### Run migrations

```bash
uv run alembic upgrade head
```

### Run the API

```bash
uv run uvicorn src.main:app --reload
```

### Run the Celery worker

```bash
uv run celery -A src.worker.app worker --loglevel=info
```

### Run the Celery beat scheduler (due date reminders)

```bash
uv run celery -A src.worker.app beat --loglevel=info
```

## 🧪 Testing

### Run all tests

```bash
uv run pytest
```

## 📜 License

This project is licensed under the MIT License.

# ============================================================================
# Dockerfile - Fullstack image (FastAPI + Angular) for Cloud Run
# ============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Build Angular frontend
# ---------------------------------------------------------------------------
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend

# Install frontend dependencies first for better layer caching
COPY front/package*.json ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Build Angular production bundle
COPY front/ ./
RUN npm run build -- --configuration production


# ---------------------------------------------------------------------------
# Stage 2: Build Python dependencies with Poetry
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS backend-builder

WORKDIR /build

ENV PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Build tools for scientific Python wheels when needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.0

COPY back/pyproject.toml ./pyproject.toml
RUN poetry install --only main --no-root --no-ansi


# ---------------------------------------------------------------------------
# Stage 3: Runtime image
# ---------------------------------------------------------------------------
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

# Minimal runtime tools (curl only for optional health checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python environment and backend code
COPY --from=backend-builder /build/.venv /app/.venv
COPY back/app/ /app/app/
COPY back/alembic/ /app/alembic/
COPY back/alembic.ini /app/alembic.ini

# Copy Angular static build into backend static folder
COPY --from=frontend-builder /frontend/dist/coreui-free-angular-admin-template/browser/ /app/static/

# Use non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Cloud Run provides PORT; default to 8080 for local container runs
EXPOSE 8080

CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1"]

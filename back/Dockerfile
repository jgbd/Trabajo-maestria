# ============================================================================
# Dockerfile - IRCA Backend + Frontend (Unified)
# ============================================================================
# Multi-stage build for optimized production image
# 
# Architecture:
#   - Stage 1: Builder - Installs Python dependencies
#   - Stage 2: Runtime - Final lightweight image with app + dependencies
#
# Features:
#   - Non-root user for security
#   - Health check included
#   - Optimized for Cloud Run (1 worker, horizontal scaling)
#   - Serves both API (/api/*) and Angular SPA (/*)
#
# Build: docker build -t irca-backend:latest .
# Run:   docker run -p 8000:8000 --env-file .env irca-backend:latest
# ============================================================================

# ============================================================================
# Stage 1: Builder - Install Python dependencies
# ============================================================================
FROM python:3.11-slim as builder

LABEL stage=builder
LABEL maintainer="IRCA Team"

WORKDIR /build

# Install system build dependencies for Python packages
# - gcc/g++: Compile C extensions (numpy, pandas, scikit-learn)
# - default-libmysqlclient-dev: MySQL client headers for PyMySQL
# - pkg-config: Helps find libraries during compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry package manager
RUN pip install --no-cache-dir poetry==1.8.0

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry and install dependencies
# --only main: Install only production dependencies (skip dev dependencies)
# --no-root: Don't install the project itself yet
# --no-interaction: Don't ask for user input
# virtualenvs.in-project: Create .venv inside /build
RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-root --no-interaction --no-ansi

# ============================================================================
# Stage 2: Runtime - Final production image
# ============================================================================
FROM python:3.11-slim

LABEL maintainer="IRCA Team"
LABEL description="IRCA Water Quality API + Frontend (Unified)"
LABEL version="1.0.0"

WORKDIR /app

# Install runtime dependencies only
# - default-libmysqlclient-dev: MySQL client libraries (runtime)
# - curl: For health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
# This contains all Python dependencies
COPY --from=builder /build/.venv /app/.venv

# Copy application code
COPY app/ /app/app/
COPY alembic/ /app/alembic/
COPY alembic.ini /app/

# Copy static files (Angular build)
# This directory should be created by build.sh script
# Contains: index.html, assets/, *.js, *.css
COPY static/ /app/static/

# Create non-root user for security
# Cloud Run and Kubernetes best practices recommend non-root containers
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app:$PYTHONPATH" \
    PYTHONUNBUFFERED=1

# Expose port 8000
# Cloud Run will automatically map this to HTTPS
EXPOSE 8000

# Health check
# Docker/Cloud Run will use this to determine if container is healthy
# Checks every 30s, timeout 10s, starts checking after 40s, 3 retries
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start application with Uvicorn
# --host 0.0.0.0: Listen on all network interfaces
# --port 8000: Port to bind (must match EXPOSE)
# --workers 1: Single worker (Cloud Run scales horizontally)
#
# For production with more resources, consider:
# - gunicorn with uvicorn workers: better process management
# - Command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

# ============================================================================
# Build & Run Instructions
# ============================================================================
#
# 1. Prepare static files (Angular build):
#    ./build.sh
#
# 2. Build Docker image:
#    docker build -t irca-backend:latest .
#
# 3. Run locally:
#    docker run -p 8000:8000 \
#      -e DB_HOST=mysql_local \
#      -e DB_USER=root \
#      -e DB_PASSWORD=1234 \
#      -e DB_NAME=calidad_agua \
#      --network bridge \
#      irca-backend:latest
#
# 4. Test:
#    Frontend: http://localhost:8000
#    API:      http://localhost:8000/api
#    Docs:     http://localhost:8000/docs
#    Health:   http://localhost:8000/health
#
# 5. Push to GCR (Google Container Registry):
#    docker tag irca-backend:latest gcr.io/PROJECT_ID/irca-backend:latest
#    docker push gcr.io/PROJECT_ID/irca-backend:latest
#
# 6. Deploy to Cloud Run:
#    gcloud run deploy irca-backend \
#      --image gcr.io/PROJECT_ID/irca-backend:latest \
#      --region us-central1 \
#      --platform managed
#
# ============================================================================

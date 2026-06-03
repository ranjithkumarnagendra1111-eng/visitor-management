# Multi-stage Dockerfile for Visitor Management API

# Build stage: install Python dependencies in a venv
FROM python:3.11-slim AS builder

WORKDIR /tmp

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage: lean image with only the app and installed deps
FROM python:3.11-slim AS runtime

RUN useradd --create-home --shell /bin/bash app
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .
RUN mkdir -p logs data \
    && chown -R app:app /app

USER app
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
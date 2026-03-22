# =============================================
# Multi-stage build: smaller + more secure image
# =============================================
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# =============================================
# Production image
# =============================================
FROM python:3.11-slim

# Security: run as non-root
RUN groupadd -r sentinel && useradd -r -g sentinel sentinel

WORKDIR /app

# Copy installed deps from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY src/ ./src/

# Switch to non-root user
USER sentinel

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

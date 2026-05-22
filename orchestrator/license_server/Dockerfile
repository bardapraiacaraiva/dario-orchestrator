FROM python:3.13-slim

WORKDIR /app/orchestrator

# System-level deps kept minimal; SQLite is built into Python.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Python runtime — pin to currently-used versions.
RUN pip install --no-cache-dir \
        "fastapi>=0.135,<1.0" \
        "uvicorn[standard]>=0.38,<1.0" \
        "pydantic>=2.12,<3.0"

# Copy the source. We only need the license_server package + its db helper.
COPY license_server /app/orchestrator/license_server

# Persistent storage for the SQLite DB lives outside the image.
ENV LICENSE_SERVER_DB=/data/license.db
VOLUME ["/data"]

EXPOSE 8430

# LICENSE_SERVER_SECRET must be injected at runtime — server refuses to
# start without one ≥32 chars (see _require_secret in app.py).
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8430/health || exit 1

CMD ["python", "-m", "license_server.app", "--host", "0.0.0.0", "--port", "8430"]

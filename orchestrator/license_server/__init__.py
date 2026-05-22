"""DARIO License Server (Onda 8) — server-side trial enforcement.

Closes the last bypass gap from the Onda 7 audit:
> "User técnico com 30 minutos e conhecimento pode bypass (sempre verdadeiro
>  sem license server)"

Architecture:
    POST /trial/activate {machine_id}
        - First request from machine_id → create trial record, return token
        - Subsequent requests → return existing trial state (idempotent)

    POST /trial/validate {machine_id, token}
        - Verify HMAC signature of token
        - Check server-side expiration
        - Record heartbeat (anti-snapshot)
        - Detect snapshot rollback: if local claims "started later" than
          server's earliest recorded activation, flag as tampered

    POST /vip/activate {machine_id, vip_key}
        - Bind a VIP key to a machine; future /trial/validate calls return
          tier=pro/enterprise with no expiry

    GET /health
        - Simple liveness probe for load balancers

Storage: SQLite (suitable for single-node up to ~10k machines/day).
For higher scale, swap to Postgres — same schema.

Auth: server uses its own HMAC secret (LICENSE_SERVER_SECRET env var),
distinct from the orchestrator's MASTER_SECRET. Compromising one does
not compromise the other.

Run:
    python -m license_server.app
    # OR
    uvicorn license_server.app:app --host 0.0.0.0 --port 8430
"""

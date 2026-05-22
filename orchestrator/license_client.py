"""License server client (Onda 8).

Thin HTTP client that the orchestrator uses to talk to the license server.
Keeps `license_manager.py` clean — all server I/O lives here.

Design rules:
    1. Never block startup. If the server is unreachable, fall back to the
       3-layer local fingerprint defence (Onda 7) and log a warning.
    2. All requests have a 5-second timeout. The server is supposed to be
       fast; if it's slow we'd rather degrade than freeze CLI.
    3. The server is OPTIONAL. If `DARIO_LICENSE_SERVER` is unset, this
       module is a no-op and the orchestrator behaves exactly as in Onda 7.

Env vars:
    DARIO_LICENSE_SERVER  Base URL of the server (e.g. https://license.dario.io)
                           Unset → all functions return None and orchestrator
                           uses local-only enforcement.
    DARIO_LICENSE_TOKEN   Cached token from last successful activation.
                           Also stored inside license.json.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any

log = logging.getLogger("license_client")

DEFAULT_TIMEOUT = float(os.getenv("DARIO_LICENSE_TIMEOUT", "5.0"))


def server_url() -> str | None:
    """Return base URL of the license server, or None if not configured."""
    url = os.getenv("DARIO_LICENSE_SERVER", "").strip().rstrip("/")
    return url or None


def is_enabled() -> bool:
    return server_url() is not None


def _post(path: str, payload: dict, timeout: float = DEFAULT_TIMEOUT) -> dict | None:
    """POST JSON to {server_url}{path}. Returns dict on success, None on failure."""
    base = server_url()
    if not base:
        return None
    url = f"{base}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            parsed: dict = json.loads(body)
            return parsed
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read())
        except Exception:
            err_body = {"error": str(e)}
        log.warning(f"[license-server] {path} HTTP {e.code}: {err_body}")
        return {"_http_status": e.code, **err_body}
    except urllib.error.URLError as e:
        log.warning(f"[license-server] {path} unreachable: {e.reason}")
        return None
    except Exception as e:
        log.warning(f"[license-server] {path} failed: {type(e).__name__}: {e}")
        return None


def activate_trial(machine_id: str) -> dict | None:
    """Call POST /trial/activate. Returns the server's trial record.

    Idempotent — repeat calls return the same record. Returns None if the
    server is unreachable or not configured.
    """
    return _post("/trial/activate", {"machine_id": machine_id})


def validate_trial(
    machine_id: str,
    token: str,
    client_first_init_at: str | None = None,
) -> dict | None:
    """Call POST /trial/validate. Returns the server's validation result."""
    payload: dict[str, Any] = {"machine_id": machine_id, "token": token}
    if client_first_init_at:
        payload["client_first_init_at"] = client_first_init_at
    return _post("/trial/validate", payload)


def upgrade_vip(machine_id: str, vip_key: str) -> dict | None:
    """Call POST /vip/activate. Returns the server's upgraded record."""
    return _post("/vip/activate", {"machine_id": machine_id, "vip_key": vip_key})


def ping() -> bool:
    """Quick health check. Returns True if the server is reachable."""
    base = server_url()
    if not base:
        return False
    try:
        with urllib.request.urlopen(f"{base}/health", timeout=DEFAULT_TIMEOUT) as resp:
            ok: bool = resp.status == 200
            return ok
    except Exception:
        return False


__all__ = [
    "server_url",
    "is_enabled",
    "activate_trial",
    "validate_trial",
    "upgrade_vip",
    "ping",
]

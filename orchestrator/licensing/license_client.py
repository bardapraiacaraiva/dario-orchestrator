"""License server client — simplified per RFC_STRATEGIC_DECISIONS (Risk #4).

Was 333 LOC with SPKI cert pinning + RFC 7469 + bypass env + obfuscated checks.
This rewrite (post 2026-05-24 strategic decision) is ~80 LOC honest:

  - Optional server check via DARIO_LICENSE_SERVER env var
  - 5-second timeout, fail-soft (server down → continue with local license)
  - Plain HTTPS (TLS terminated upstream — caller's responsibility)
  - No cert pinning (was theater; sophisticated attackers bypass it anyway)
  - No anti-debug, no bypass flags

The defense model is honest: server check is a SIGNAL ("who has installs
active") not a SECURITY BOUNDARY. Real attacker stops paying = we lose
revenue; real attacker decompiles = same outcome. Cost/benefit ratio of
obfuscation was negative.

Env vars:
    DARIO_LICENSE_SERVER       Base URL (e.g. https://license.dario.io)
                                Unset → all functions return None.
    DARIO_LICENSE_TIMEOUT      HTTP timeout in seconds (default 5.0).
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request

log = logging.getLogger("license_client")

DEFAULT_TIMEOUT = float(os.getenv("DARIO_LICENSE_TIMEOUT", "5.0"))


def server_url() -> str | None:
    """Return base URL of the license server, or None if not configured."""
    url = os.getenv("DARIO_LICENSE_SERVER", "").strip().rstrip("/")
    return url or None


def is_enabled() -> bool:
    return server_url() is not None


def _post(path: str, payload: dict) -> dict | None:
    """POST JSON to license server. Returns parsed response or None on any error."""
    base = server_url()
    if not base:
        return None
    url = f"{base}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "User-Agent": "dario-license-client/2.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            body = resp.read()
            return json.loads(body)
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError) as e:
        log.warning(f"license_server unreachable ({type(e).__name__}: {e}) — fail-soft, using local")
        return None


def init_trial_remote(machine_id: str) -> dict | None:
    """Ask server to issue a trial token for this machine. None if server unreachable."""
    return _post("/trial/init", {"machine_id": machine_id})


def revalidate(key: str, machine_id: str) -> dict | None:
    """Re-validate an active key. Returns server's response or None on error."""
    return _post("/license/revalidate", {"key": key, "machine_id": machine_id})


def report_activation(key: str, machine_id: str, tier: str) -> dict | None:
    """Notify server that this machine activated a license key (telemetry, not gate)."""
    return _post("/license/activate", {"key": key, "machine_id": machine_id, "tier": tier})


def report_check(key: str, machine_id: str) -> dict | None:
    """Heartbeat — report that the license was checked. Server returns optional override."""
    return _post("/license/heartbeat", {"key": key, "machine_id": machine_id})


# ─── CLI smoke test ──────────────────────────────────────────────────────────

def _main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true", help="Show config")
    args = ap.parse_args()
    print(f"DARIO_LICENSE_SERVER = {server_url() or '(unset)'}")
    print(f"DARIO_LICENSE_TIMEOUT = {DEFAULT_TIMEOUT}")
    print(f"enabled: {is_enabled()}")


if __name__ == "__main__":
    _main()

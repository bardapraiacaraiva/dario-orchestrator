"""License server client (Onda 8 + Onda 9).

Thin HTTPS client that the orchestrator uses to talk to the license server.
Keeps `license_manager.py` clean — all server I/O lives here.

Design rules:
    1. Never block startup. If the server is unreachable, fall back to the
       3-layer local fingerprint defence (Onda 7) and log a warning.
    2. All requests have a 5-second timeout. The server is supposed to be
       fast; if it's slow we'd rather degrade than freeze CLI.
    3. The server is OPTIONAL. If `DARIO_LICENSE_SERVER` is unset, this
       module is a no-op and the orchestrator behaves exactly as in Onda 7.
    4. **HTTPS connections are certificate-pinned** (Onda 9). The SHA-256 hash
       of the server's leaf certificate's public-key SPKI must match
       `DARIO_LICENSE_CERT_PIN`. DNS hijacks + MITM with a different cert
       fail closed. `http://` URLs skip the pin (dev convenience).

Env vars:
    DARIO_LICENSE_SERVER       Base URL (e.g. https://license.dario.io)
                                Unset → all functions return None.
    DARIO_LICENSE_CERT_PIN     SHA-256 hex of the leaf cert's SPKI. When set
                                AND server URL is https://, the TLS handshake
                                only succeeds if the cert matches the pin.
                                Get the pin once with the `--print-pin` CLI.
    DARIO_LICENSE_PIN_BYPASS=1 Skip pin validation. Dev/CI only — leaks the
                                whole defence if set in production. Logs a
                                loud warning on every call.
    DARIO_LICENSE_TIMEOUT      HTTP timeout in seconds (default 5.0).
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

log = logging.getLogger("license_client")

DEFAULT_TIMEOUT = float(os.getenv("DARIO_LICENSE_TIMEOUT", "5.0"))


# ─── URL + config helpers ────────────────────────────────────────────────────


def server_url() -> str | None:
    """Return base URL of the license server, or None if not configured."""
    url = os.getenv("DARIO_LICENSE_SERVER", "").strip().rstrip("/")
    return url or None


def is_enabled() -> bool:
    return server_url() is not None


def _expected_pin() -> str | None:
    pin = os.getenv("DARIO_LICENSE_CERT_PIN", "").strip().lower()
    return pin or None


def _pin_bypass_enabled() -> bool:
    return os.getenv("DARIO_LICENSE_PIN_BYPASS", "").lower() in ("1", "true", "yes")


# ─── Certificate pinning (Onda 9 #1) ─────────────────────────────────────────


def _spki_sha256(cert_der: bytes) -> str:
    """SHA-256 of the cert's SubjectPublicKeyInfo (SPKI).

    SPKI pinning is what RFC 7469 recommends — it survives certificate
    renewals as long as the same key pair is reused, but breaks if the
    operator rotates to a new key (intended).

    Falls back to hashing the raw bytes when:
      • `cryptography` is not installed (no x509 parser available), or
      • the input is not a parseable DER (e.g. corrupted / test stub).
    The fallback is less ideal cryptographically but keeps the function
    total — callers always get a hex digest.
    """
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import serialization

        cert = x509.load_der_x509_certificate(cert_der)
        spki = cert.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return hashlib.sha256(spki).hexdigest().lower()
    except (ImportError, ValueError, TypeError):
        # ImportError: cryptography not installed.
        # ValueError/TypeError: input wasn't a parseable DER (test stubs, etc.).
        return hashlib.sha256(cert_der).hexdigest().lower()


def fetch_server_pin(url: str, timeout: float = DEFAULT_TIMEOUT) -> str | None:
    """Connect to `url` (https://host[:port]) and return the SPKI SHA-256 pin.

    Used by the `--print-pin` CLI so operators can record the pin once
    during deploy and then export it as `DARIO_LICENSE_CERT_PIN`.

    Returns None for non-https URLs or on TLS errors.
    """
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        return None
    host = parsed.hostname or ""
    port = parsed.port or 443

    ctx = ssl.create_default_context()
    # We're sampling the cert chain — verification is OK to keep on,
    # since we just want to record the cert presented by the live server.
    with socket.create_connection((host, port), timeout=timeout) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as ssock:
            cert_der = ssock.getpeercert(binary_form=True)
            return _spki_sha256(cert_der) if cert_der else None


def _verify_pin_or_raise(host: str, port: int, expected_pin: str, timeout: float) -> None:
    """Open a TLS connection, compute pin, raise if it does not match.

    We do this BEFORE the urllib.request.urlopen so we can fail closed
    early. The actual HTTP call still goes through urllib (which performs
    its own normal cert chain verification on top of this).
    """
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as ssock:
            cert_der = ssock.getpeercert(binary_form=True)
            if not cert_der:
                raise ssl.SSLError("server returned no certificate")
            actual_pin = _spki_sha256(cert_der)
            if actual_pin != expected_pin.lower():
                raise ssl.SSLError(
                    f"certificate pin mismatch — expected {expected_pin[:16]}…, "
                    f"got {actual_pin[:16]}…"
                )


def _maybe_verify_pin(url: str, timeout: float) -> None:
    """Enforce cert pinning when applicable.

    Skips for:
      • http:// URLs (no TLS to pin)
      • DARIO_LICENSE_PIN_BYPASS=1 (dev/CI override; logs a warning)
      • DARIO_LICENSE_CERT_PIN unset (production should ALWAYS set it;
        we log a warning per call so the leak is loud).
    Raises ssl.SSLError on mismatch — caller catches as ordinary URLError.
    """
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        return
    if _pin_bypass_enabled():
        log.warning("[license-server] CERT PIN BYPASSED via DARIO_LICENSE_PIN_BYPASS")
        return
    pin = _expected_pin()
    if not pin:
        log.warning(
            "[license-server] HTTPS in use but DARIO_LICENSE_CERT_PIN unset — "
            "vulnerable to MITM. Set the pin in production."
        )
        return
    host = parsed.hostname or ""
    port = parsed.port or 443
    _verify_pin_or_raise(host, port, pin, timeout)


# ─── HTTP wrapper ────────────────────────────────────────────────────────────


def _post(path: str, payload: dict, timeout: float = DEFAULT_TIMEOUT) -> dict | None:
    """POST JSON to {server_url}{path}. Returns dict on success, None on failure."""
    base = server_url()
    if not base:
        return None
    url = f"{base}{path}"

    try:
        _maybe_verify_pin(url, timeout)
    except ssl.SSLError as e:
        log.warning(f"[license-server] TLS pin verification failed: {e}")
        return None
    except OSError as e:
        log.warning(f"[license-server] TLS handshake failed: {e}")
        return None

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


# ─── Public API ──────────────────────────────────────────────────────────────


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
        _maybe_verify_pin(f"{base}/health", DEFAULT_TIMEOUT)
    except (ssl.SSLError, OSError):
        return False
    try:
        with urllib.request.urlopen(f"{base}/health", timeout=DEFAULT_TIMEOUT) as resp:
            ok: bool = resp.status == 200
            return ok
    except Exception:
        return False


# ─── CLI (operator helper) ───────────────────────────────────────────────────


def _main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="DARIO license client utilities")
    parser.add_argument(
        "--print-pin",
        metavar="URL",
        help="Connect to the given https URL, print its SPKI SHA-256 pin "
             "(use this once at deploy time to record DARIO_LICENSE_CERT_PIN).",
    )
    parser.add_argument(
        "--verify-pin",
        metavar="URL",
        help="Test the configured pin against a live server. Exits 0 on match.",
    )
    args = parser.parse_args()

    if args.print_pin:
        pin = fetch_server_pin(args.print_pin)
        if not pin:
            print("ERROR: could not fetch pin (non-https URL or TLS failure)",
                  file=sys.stderr)
            return 1
        print(pin)
        return 0

    if args.verify_pin:
        expected = _expected_pin()
        if not expected:
            print("ERROR: DARIO_LICENSE_CERT_PIN env var not set", file=sys.stderr)
            return 2
        try:
            parsed = urllib.parse.urlparse(args.verify_pin)
            _verify_pin_or_raise(
                parsed.hostname or "",
                parsed.port or 443,
                expected,
                DEFAULT_TIMEOUT,
            )
        except ssl.SSLError as e:
            print(f"PIN MISMATCH: {e}", file=sys.stderr)
            return 1
        print(f"pin OK ({expected[:16]}…)")
        return 0

    parser.print_help()
    return 1


__all__ = [
    "server_url",
    "is_enabled",
    "activate_trial",
    "validate_trial",
    "upgrade_vip",
    "ping",
    "fetch_server_pin",
]


if __name__ == "__main__":
    import sys
    sys.exit(_main())

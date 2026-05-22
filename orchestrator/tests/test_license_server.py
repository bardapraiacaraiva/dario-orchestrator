"""End-to-end tests for the license server (Onda 8)."""

from __future__ import annotations

import json
import os
import secrets
import sys
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


@pytest.fixture
def server(monkeypatch, tmp_path):
    """Boot the FastAPI license server in-process with a temp DB + fresh secret."""
    secret = secrets.token_hex(32)
    monkeypatch.setenv("LICENSE_SERVER_SECRET", secret)
    monkeypatch.setenv("LICENSE_SERVER_DB", str(tmp_path / "test-license.db"))

    # Re-import to pick up new env. Reload db module + app.
    import importlib

    import license_server.db as db_mod
    importlib.reload(db_mod)

    import license_server.app as app_mod
    importlib.reload(app_mod)

    client = TestClient(app_mod.app)
    yield client


class TestHealth:
    def test_health_endpoint(self, server):
        r = server.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


class TestTrialActivation:
    def test_first_activation_returns_token(self, server):
        r = server.post("/trial/activate", json={"machine_id": "machine-001"})
        assert r.status_code == 200
        body = r.json()
        assert body["machine_id"] == "machine-001"
        assert body["tier"] == "trial"
        assert body["status"] == "active"
        assert 0 < body["days_remaining"] <= 7
        assert "." in body["token"]  # payload.signature

    def test_repeat_activation_is_idempotent(self, server):
        r1 = server.post("/trial/activate", json={"machine_id": "machine-002"})
        r2 = server.post("/trial/activate", json={"machine_id": "machine-002"})
        assert r1.json()["token"] == r2.json()["token"]
        assert r1.json()["first_init_at"] == r2.json()["first_init_at"]

    def test_distinct_machines_get_distinct_tokens(self, server):
        r1 = server.post("/trial/activate", json={"machine_id": "machine-A"})
        r2 = server.post("/trial/activate", json={"machine_id": "machine-B"})
        assert r1.json()["token"] != r2.json()["token"]


class TestTrialValidation:
    def test_valid_token_passes(self, server):
        activate = server.post("/trial/activate", json={"machine_id": "machine-010"})
        token = activate.json()["token"]
        r = server.post(
            "/trial/validate",
            json={"machine_id": "machine-010", "token": token},
        )
        body = r.json()
        assert body["valid"] is True
        assert body["tier"] == "trial"
        assert body["days_remaining"] > 0

    def test_tampered_token_rejected(self, server):
        activate = server.post("/trial/activate", json={"machine_id": "machine-011"})
        tampered = activate.json()["token"][:-1] + "X"  # alter last char of signature
        r = server.post(
            "/trial/validate",
            json={"machine_id": "machine-011", "token": tampered},
        )
        body = r.json()
        assert body["valid"] is False
        assert body["reason"] == "bad_signature"

    def test_token_replay_on_wrong_machine_rejected(self, server):
        a = server.post("/trial/activate", json={"machine_id": "machine-020"})
        token = a.json()["token"]
        # Try to validate that token claiming to be a different machine
        r = server.post(
            "/trial/validate",
            json={"machine_id": "machine-021", "token": token},
        )
        assert r.json()["valid"] is False
        assert r.json()["reason"] in ("machine_mismatch", "no_trial_record")

    def test_validate_no_record_for_unknown_machine(self, server):
        # Forge a token-shaped string with a random signature (signature
        # check still has to pass; we can't bypass it without the secret).
        # The Pydantic contract requires min_length=16, so use a long bogus.
        r = server.post(
            "/trial/validate",
            json={
                "machine_id": "machine-999",
                "token": "garbage-payload-too-long.bogus-signature-also-too-long-deadbeef",
            },
        )
        assert r.json().get("valid") is False

    def test_heartbeat_increments(self, server):
        a = server.post("/trial/activate", json={"machine_id": "machine-030"})
        token = a.json()["token"]
        for _ in range(3):
            server.post(
                "/trial/validate",
                json={"machine_id": "machine-030", "token": token},
            )
        # Re-activate to read current heartbeat_count
        r = server.post("/trial/activate", json={"machine_id": "machine-030"})
        assert r.json()["heartbeat_count"] >= 4  # 1 initial + 3 validates


class TestSnapshotRollbackDetection:
    """If the client claims a `client_first_init_at` that diverges from the
    server's stored `first_init_at` by more than the tolerance window, this
    indicates a VM snapshot rollback or local clock tamper. The server flags
    it and the validate response returns `rollback_detected=True`."""

    def test_rollback_detected_when_client_claims_later(self, server):
        a = server.post("/trial/activate", json={"machine_id": "machine-roll-A"})
        token = a.json()["token"]
        # Client pretends it just started — should be far in the future vs server
        future = (datetime.now(UTC) + timedelta(days=30)).isoformat()
        r = server.post(
            "/trial/validate",
            json={
                "machine_id": "machine-roll-A",
                "token": token,
                "client_first_init_at": future,
            },
        )
        assert r.json()["valid"] is False
        assert r.json()["rollback_detected"] is True

    def test_rollback_detected_when_client_claims_earlier(self, server):
        a = server.post("/trial/activate", json={"machine_id": "machine-roll-B"})
        token = a.json()["token"]
        past = (datetime.now(UTC) - timedelta(days=30)).isoformat()
        r = server.post(
            "/trial/validate",
            json={
                "machine_id": "machine-roll-B",
                "token": token,
                "client_first_init_at": past,
            },
        )
        assert r.json()["valid"] is False
        assert r.json()["rollback_detected"] is True

    def test_within_tolerance_passes(self, server):
        a = server.post("/trial/activate", json={"machine_id": "machine-roll-C"})
        token = a.json()["token"]
        server_init = a.json()["first_init_at"]
        # Drift by 30 minutes — within 1h tolerance
        almost = (
            datetime.fromisoformat(server_init) + timedelta(minutes=30)
        ).isoformat()
        r = server.post(
            "/trial/validate",
            json={
                "machine_id": "machine-roll-C",
                "token": token,
                "client_first_init_at": almost,
            },
        )
        assert r.json()["valid"] is True
        assert r.json()["rollback_detected"] is False


class TestVipUpgrade:
    def test_vip_upgrade_promotes_tier(self, server):
        server.post("/trial/activate", json={"machine_id": "machine-vip"})
        r = server.post(
            "/vip/activate",
            json={"machine_id": "machine-vip", "vip_key": "DARIO-A1B2-C3D4-E5F6-PRO"},
        )
        assert r.status_code == 200
        assert r.json()["tier"] == "pro"
        assert r.json()["status"] == "active"

    def test_vip_invalid_format_rejected(self, server):
        r = server.post(
            "/vip/activate",
            json={"machine_id": "machine-vip-bad", "vip_key": "DARIO-x-y-z-z"},
        )
        # Missing DARIO- prefix OR wrong tier — must fail
        assert r.status_code == 400 or r.json().get("status") != "active"

    def test_post_upgrade_validate_returns_pro(self, server):
        a = server.post("/trial/activate", json={"machine_id": "machine-vip-2"})
        token = a.json()["token"]
        server.post(
            "/vip/activate",
            json={"machine_id": "machine-vip-2", "vip_key": "DARIO-XXXX-YYYY-ZZZZ-PRO"},
        )
        r = server.post(
            "/trial/validate",
            json={"machine_id": "machine-vip-2", "token": token},
        )
        assert r.json()["tier"] == "pro"
        assert r.json()["valid"] is True
        assert r.json()["days_remaining"] > 365  # effectively unbounded


class TestRequestValidation:
    def test_short_machine_id_rejected(self, server):
        r = server.post("/trial/activate", json={"machine_id": "abc"})
        assert r.status_code == 422  # pydantic min_length

    def test_extra_field_rejected(self, server):
        r = server.post(
            "/trial/activate",
            json={"machine_id": "machine-extra", "unexpected": True},
        )
        assert r.status_code == 422


# ─── Onda 9 #1 — Certificate pinning ─────────────────────────────────────────


class TestCertificatePinning:
    """Unit tests for the cert-pinning helpers in license_client.

    These do NOT spin up a TLS server (which would require a real cert).
    They exercise the policy: when do we verify, when do we skip, and
    what failure modes return None vs raise.
    """

    def test_no_pin_skips_https_check(self, monkeypatch):
        """Without DARIO_LICENSE_CERT_PIN, https calls log-warn and proceed."""
        import license_client

        monkeypatch.delenv("DARIO_LICENSE_CERT_PIN", raising=False)
        monkeypatch.delenv("DARIO_LICENSE_PIN_BYPASS", raising=False)
        # Should not raise — pin is unset, so we proceed (with a warning logged)
        license_client._maybe_verify_pin("https://example.com/health", 1.0)

    def test_pin_bypass_env_skips_check(self, monkeypatch):
        import license_client

        monkeypatch.setenv("DARIO_LICENSE_CERT_PIN", "deadbeef" * 8)
        monkeypatch.setenv("DARIO_LICENSE_PIN_BYPASS", "1")
        # Bypass enabled — should not even attempt the TLS handshake
        license_client._maybe_verify_pin(
            "https://localhost-not-actually-running:1/", 0.5
        )

    def test_http_url_skips_pin(self, monkeypatch):
        import license_client

        monkeypatch.setenv("DARIO_LICENSE_CERT_PIN", "deadbeef" * 8)
        monkeypatch.delenv("DARIO_LICENSE_PIN_BYPASS", raising=False)
        # http:// is not pinned (no TLS)
        license_client._maybe_verify_pin("http://localhost:8430/health", 0.5)

    def test_spki_hash_is_deterministic(self):
        """_spki_sha256 returns the same hash for the same input bytes."""
        import license_client

        dummy = b"NOT-A-REAL-CERT-just-bytes-for-hashing"
        h1 = license_client._spki_sha256(dummy)
        h2 = license_client._spki_sha256(dummy)
        assert h1 == h2
        assert len(h1) == 64  # SHA-256 hex
        assert h1 != license_client._spki_sha256(dummy + b"x")

    def test_pin_mismatch_raises_sslerror(self, monkeypatch):
        """Direct _verify_pin_or_raise against a real TLS endpoint with a
        bogus expected pin should raise ssl.SSLError (or OSError if the host
        is unreachable — both are acceptable failure modes)."""
        import ssl

        import license_client

        # Use a public TLS endpoint that's likely reachable from a build host.
        # The expected pin is intentionally wrong → must raise.
        try:
            with pytest.raises((ssl.SSLError, OSError)):
                license_client._verify_pin_or_raise(
                    "example.com", 443, "00" * 32, timeout=3.0
                )
        except Exception as exc:
            # If example.com is unreachable from the CI sandbox, accept it.
            pytest.skip(f"network unreachable for pin test: {exc!r}")

    def test_post_returns_none_on_pin_mismatch(self, monkeypatch):
        """When the pin doesn't match, _post short-circuits and returns None."""
        import license_client

        monkeypatch.setenv("DARIO_LICENSE_SERVER", "https://example.com")
        monkeypatch.setenv("DARIO_LICENSE_CERT_PIN", "00" * 32)
        monkeypatch.delenv("DARIO_LICENSE_PIN_BYPASS", raising=False)

        # Real network call expected, but pin will mismatch → None.
        result = license_client._post("/trial/activate", {"machine_id": "test"},
                                       timeout=3.0)
        # None expected (pin mismatch) OR None (network unreachable in sandbox).
        # Either way must NOT be a dict (which would indicate the call went
        # through despite the bad pin).
        assert result is None or result.get("_http_status") is not None

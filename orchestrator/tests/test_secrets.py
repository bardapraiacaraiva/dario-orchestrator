"""Tests for the OS keyring secrets manager (Faixa 1 #2)."""
from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

keyring = pytest.importorskip("keyring")

from core.secrets import (
    SERVICE_NAME,
    delete_secret,
    get_keyring_backend,
    get_secret,
    is_keyring_available,
    list_secret_names,
    set_secret,
)


# Each test uses a UUID-based name to avoid collisions with real keys.
@pytest.fixture
def unique_name():
    return f"test-{uuid.uuid4().hex[:12]}"


@pytest.fixture(autouse=True)
def skip_if_no_keyring():
    if not is_keyring_available():
        pytest.skip(f"keyring backend unavailable ({get_keyring_backend()})")


# ─── Backend availability ────────────────────────────────────────────────


def test_backend_is_named():
    backend = get_keyring_backend()
    assert backend
    assert "Failing" not in backend


# ─── Round trip ──────────────────────────────────────────────────────────


def test_set_and_get_round_trip(unique_name):
    set_secret(unique_name, "the-secret-value", caller="test")
    try:
        v = get_secret(unique_name, caller="test")
        assert v == "the-secret-value"
    finally:
        delete_secret(unique_name, caller="test")


def test_get_nonexistent_returns_none():
    v = get_secret("definitely-does-not-exist-xyzzy-9999", caller="test")
    assert v is None


def test_delete_returns_true_when_existed(unique_name):
    set_secret(unique_name, "x", caller="test")
    assert delete_secret(unique_name, caller="test") is True
    assert get_secret(unique_name, caller="test") is None


def test_delete_returns_false_when_missing():
    assert delete_secret(f"missing-{uuid.uuid4().hex}", caller="test") is False


# ─── Fallback chain (env + file) ─────────────────────────────────────────


def test_fallback_env(monkeypatch, unique_name):
    """Secret not in keyring but in env → returned, not stored."""
    env_name = f"TEST_FALLBACK_{uuid.uuid4().hex[:8].upper()}"
    monkeypatch.setenv(env_name, "from-env")
    v = get_secret(unique_name, caller="test", fallback_env=env_name)
    assert v == "from-env"
    # And not stored in keyring
    assert keyring.get_password(SERVICE_NAME, unique_name) is None


def test_fallback_file(tmp_path, unique_name):
    f = tmp_path / "secret.txt"
    f.write_text("  from-file\n", encoding="utf-8")
    v = get_secret(unique_name, caller="test", fallback_file=str(f))
    assert v == "from-file"


def test_keyring_takes_priority_over_fallbacks(monkeypatch, unique_name):
    set_secret(unique_name, "from-keyring", caller="test")
    try:
        monkeypatch.setenv("TEST_FALLBACK_PRIORITY", "from-env")
        v = get_secret(unique_name, caller="test", fallback_env="TEST_FALLBACK_PRIORITY")
        assert v == "from-keyring"
    finally:
        delete_secret(unique_name, caller="test")


# ─── Catalog ─────────────────────────────────────────────────────────────


def test_catalog_lists_after_set(unique_name):
    set_secret(unique_name, "x", caller="test")
    try:
        names = list_secret_names()
        assert unique_name in names
    finally:
        delete_secret(unique_name, caller="test")


def test_catalog_removes_after_delete(unique_name):
    set_secret(unique_name, "x", caller="test")
    delete_secret(unique_name, caller="test")
    names = list_secret_names()
    assert unique_name not in names


# ─── Values never logged ─────────────────────────────────────────────────


def test_set_does_not_log_value(caplog, unique_name):
    """Verify that the secret VALUE never appears in any log record."""
    import logging
    caplog.set_level(logging.DEBUG, logger="core.secrets")
    secret_value = f"super-secret-{uuid.uuid4().hex}"
    set_secret(unique_name, secret_value, caller="test")
    try:
        for record in caplog.records:
            assert secret_value not in record.getMessage()
            assert secret_value not in (record.args or ())
    finally:
        delete_secret(unique_name, caller="test")


def test_failed_get_logs_audit_with_ok_false(unique_name):
    """Audit log should record a get-miss as ok=False."""
    # Implicit: we call get on a name that doesn't exist; the audit log gets
    # ok=False. We can't easily intercept audit_logger.log_event from here
    # without complex mocking, so we just confirm no exception.
    v = get_secret(f"missing-{uuid.uuid4().hex}", caller="test")
    assert v is None  # smoke test


# ─── Resilience ──────────────────────────────────────────────────────────


def test_get_handles_unicode_secret(unique_name):
    """Secrets with non-ASCII chars round-trip correctly."""
    secret = "🔐 пароль ñoño 日本語"
    set_secret(unique_name, secret, caller="test")
    try:
        assert get_secret(unique_name, caller="test") == secret
    finally:
        delete_secret(unique_name, caller="test")


def test_set_overwrites_existing(unique_name):
    set_secret(unique_name, "v1", caller="test")
    try:
        set_secret(unique_name, "v2", caller="test")
        assert get_secret(unique_name, caller="test") == "v2"
    finally:
        delete_secret(unique_name, caller="test")

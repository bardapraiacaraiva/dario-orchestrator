"""Tests for safety/sandbox.py — Faixa 1 #1 v1 subprocess sandbox.

These tests use only Python's stdlib (no external commands) for portability.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from safety.sandbox import (
    ENV_DENY_LIST,
    SAFE_ENV_DEFAULTS,
    SandboxResult,
    run_sandboxed,
)

PYTHON = sys.executable


# ─── Input validation ────────────────────────────────────────────────────


def test_rejects_string_cmd_to_prevent_shell_injection():
    with pytest.raises(ValueError, match="non-empty list"):
        run_sandboxed("python --version", caller="test")  # type: ignore[arg-type]


def test_rejects_empty_cmd():
    with pytest.raises(ValueError):
        run_sandboxed([], caller="test")


def test_rejects_non_string_cmd_elements():
    with pytest.raises(ValueError, match="must be strings"):
        run_sandboxed([PYTHON, 123], caller="test")  # type: ignore[list-item]


# ─── Basic execution ─────────────────────────────────────────────────────


def test_simple_command_runs():
    r = run_sandboxed([PYTHON, "-c", "print('hello sandbox')"], caller="test")
    assert isinstance(r, SandboxResult)
    assert r.ok
    assert r.returncode == 0
    assert "hello sandbox" in r.stdout
    assert r.duration_s > 0
    assert not r.timeout_hit


def test_returncode_propagates():
    r = run_sandboxed([PYTHON, "-c", "import sys; sys.exit(3)"], caller="test")
    assert r.returncode == 3
    assert not r.ok


def test_stderr_captured_separately():
    r = run_sandboxed(
        [PYTHON, "-c", "import sys; sys.stderr.write('err\\n'); print('out')"],
        caller="test",
    )
    assert "out" in r.stdout
    assert "err" in r.stderr


# ─── Env scoping ─────────────────────────────────────────────────────────


def test_unlisted_env_var_not_visible_in_subprocess(monkeypatch):
    """A secret env var NOT in allowlist must not appear in the subprocess."""
    monkeypatch.setenv("SUPER_SECRET_THAT_SHOULD_NOT_LEAK", "leaked-value")
    r = run_sandboxed(
        [PYTHON, "-c", "import os; print(os.environ.get('SUPER_SECRET_THAT_SHOULD_NOT_LEAK', 'NOT_PRESENT'))"],
        caller="test",
    )
    assert "NOT_PRESENT" in r.stdout
    assert "leaked-value" not in r.stdout


def test_allowlisted_env_var_is_visible(monkeypatch):
    monkeypatch.setenv("DARIO_TEST_ALLOWED", "i-am-allowed")
    r = run_sandboxed(
        [PYTHON, "-c", "import os; print(os.environ.get('DARIO_TEST_ALLOWED', 'NOT_FOUND'))"],
        caller="test",
        env_allowlist=["DARIO_TEST_ALLOWED"],
    )
    assert "i-am-allowed" in r.stdout
    assert "DARIO_TEST_ALLOWED" in r.env_keys_passed


def test_deny_list_overrides_allowlist(monkeypatch):
    """Even if explicitly allowlisted, DARIO_GH_TOKEN must never pass."""
    monkeypatch.setenv("DARIO_GH_TOKEN", "ghp_should_be_blocked")
    r = run_sandboxed(
        [PYTHON, "-c", "import os; print(os.environ.get('DARIO_GH_TOKEN', 'BLOCKED'))"],
        caller="test",
        env_allowlist=["DARIO_GH_TOKEN"],  # try to allow — should be denied anyway
    )
    assert "BLOCKED" in r.stdout
    assert "ghp_should_be_blocked" not in r.stdout
    assert "DARIO_GH_TOKEN" not in r.env_keys_passed


def test_env_extra_takes_effect():
    r = run_sandboxed(
        [PYTHON, "-c", "import os; print(os.environ.get('MY_INJECTED'))"],
        caller="test",
        env_extra={"MY_INJECTED": "injected-value"},
    )
    assert "injected-value" in r.stdout


def test_env_extra_respects_deny_list():
    r = run_sandboxed(
        [PYTHON, "-c", "import os; print(os.environ.get('AWS_SECRET_ACCESS_KEY', 'BLOCKED'))"],
        caller="test",
        env_extra={"AWS_SECRET_ACCESS_KEY": "should-not-pass"},
    )
    assert "BLOCKED" in r.stdout
    assert "should-not-pass" not in r.stdout


# ─── Working directory ───────────────────────────────────────────────────


def test_cwd_is_isolated_tempdir():
    r = run_sandboxed(
        [PYTHON, "-c", "import os, tempfile; cwd = os.getcwd(); print('match' if 'dario-sandbox' in cwd else 'no-match', cwd)"],
        caller="test",
    )
    assert "match" in r.stdout
    assert "dario-sandbox" in r.stdout


def test_tempdir_cleaned_up_after_run():
    r = run_sandboxed(
        [PYTHON, "-c", "import os; open('marker.txt', 'w').write('x'); print(os.getcwd())"],
        caller="test",
    )
    # Returned path was cleaned up
    assert not Path(r.sandbox_dir).exists() or not (Path(r.sandbox_dir) / "marker.txt").exists()


def test_keep_tempdir_when_cleanup_false():
    r = run_sandboxed(
        [PYTHON, "-c", "open('marker.txt', 'w').write('x'); print('ok')"],
        caller="test",
        cleanup_dir=False,
    )
    try:
        assert Path(r.sandbox_dir).exists()
        assert (Path(r.sandbox_dir) / "marker.txt").exists()
    finally:
        # Manual cleanup
        import shutil
        shutil.rmtree(r.sandbox_dir, ignore_errors=True)


# ─── Timeout ─────────────────────────────────────────────────────────────


def test_timeout_kills_long_running():
    r = run_sandboxed(
        [PYTHON, "-c", "import time; time.sleep(10)"],
        caller="test",
        timeout_s=1.0,
    )
    assert r.timeout_hit
    assert not r.ok
    assert "timeout" in " ".join(r.notes).lower()


def test_quick_command_completes_before_timeout():
    r = run_sandboxed(
        [PYTHON, "-c", "print('quick')"],
        caller="test",
        timeout_s=5.0,
    )
    assert not r.timeout_hit
    assert r.ok


# ─── Error handling ──────────────────────────────────────────────────────


def test_nonexistent_cmd_returns_127():
    r = run_sandboxed(
        ["definitely-does-not-exist-cmd-xyz-99999"],
        caller="test",
    )
    assert r.returncode == 127
    assert "cmd-not-found" in r.notes
    assert not r.ok


# ─── Result shape + auditing ─────────────────────────────────────────────


def test_result_to_audit_dict_excludes_stdout_content(monkeypatch):
    """to_audit_dict() must not include stdout/stderr contents (may contain secrets).

    To test this, pass the secret via STDIN (which never appears in cmd args)
    and have the child echo it to stdout. Audit dict should NOT carry it.
    """
    secret = "PASSWORD_FROM_STDIN_ABC123"
    r = run_sandboxed(
        [PYTHON, "-c", "import sys; print(sys.stdin.read())"],
        caller="test",
        input_data=secret,
    )
    assert secret in r.stdout  # subprocess did echo it
    audit = r.to_audit_dict()
    flat = str(audit)
    assert secret not in flat, f"secret leaked into audit dict: {flat}"


def test_env_keys_passed_is_names_only():
    """env_keys_passed contains var NAMES, never values."""
    r = run_sandboxed(
        [PYTHON, "-c", "print('ok')"],
        caller="test",
        env_extra={"TEST_KEY": "TEST_VALUE_SECRET"},
    )
    assert "TEST_VALUE_SECRET" not in str(r.env_keys_passed)


# ─── Deny-list completeness ──────────────────────────────────────────────


def test_all_deny_list_entries_blocked_even_via_extra(monkeypatch):
    """For every entry in ENV_DENY_LIST, confirm it's blocked via env_extra."""
    for denied in ENV_DENY_LIST:
        r = run_sandboxed(
            [PYTHON, "-c", f"import os; print(os.environ.get('{denied}', 'BLOCKED'))"],
            caller="test",
            env_extra={denied: f"should-not-leak-{denied}"},
        )
        assert "BLOCKED" in r.stdout, f"{denied} leaked via env_extra"


# ─── POSIX-only ──────────────────────────────────────────────────────────


@pytest.mark.skipif(sys.platform == "win32", reason="rlimit unavailable on Windows")
def test_memory_limit_kills_runaway_allocation():
    """A subprocess trying to allocate 2GB with 100MB limit should fail."""
    r = run_sandboxed(
        [PYTHON, "-c", "x = bytearray(2 * 1024 * 1024 * 1024); print('allocated')"],
        caller="test",
        memory_mb=100,
        timeout_s=10.0,
    )
    # Either allocation failed (returncode != 0) or it was killed.
    # We don't strictly require timeout_hit because rlimit may cause MemoryError.
    assert not r.ok or r.returncode != 0
    assert "allocated" not in r.stdout

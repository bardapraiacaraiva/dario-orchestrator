#!/usr/bin/env python3
"""Tests for v11.1+ license_guard hardening."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import license_guard


def _backup_license():
    src = ORCH_DIR / "license.json"
    if src.exists():
        shutil.copy(src, src.with_suffix(".json.test-bak"))


def _restore_license():
    bak = ORCH_DIR / "license.json.test-bak"
    if bak.exists():
        shutil.copy(bak, ORCH_DIR / "license.json")
        bak.unlink()


def _write_license(data: dict):
    (ORCH_DIR / "license.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def _set_trial_expired():
    """Force license.json to be an expired trial."""
    _write_license({
        "tier": "trial",
        "name": "Trial (7 dias)",
        "key": None,
        "activated_at": "2026-04-01T00:00:00+00:00",
        "expires_at": "2026-04-08T00:00:00+00:00",
        "max_parallel": 3,
        "features": {},
        "engines_allowed": "all",
        "status": "active",
    })


def _set_pro():
    _write_license({
        "tier": "pro",
        "name": "Professional",
        "key": "DARIO-TEST-TEST-TEST-PRO",
        "activated_at": "2026-05-01T00:00:00+00:00",
        "expires_at": None,
        "max_parallel": 3,
        "features": {"api_execution": True, "evolution_engine": True},
        "engines_allowed": "all",
        "status": "active",
    })


def test_is_valid_when_pro():
    _backup_license()
    try:
        _set_pro()
        assert license_guard.is_valid() is True
        return True
    finally:
        _restore_license()


def test_is_valid_when_expired():
    _backup_license()
    try:
        _set_trial_expired()
        assert license_guard.is_valid() is False
        return True
    finally:
        _restore_license()


def test_bypass_requires_both_env_and_flag():
    # No env, no flag -> bypass inactive
    os.environ.pop("DARIO_LICENSE_BYPASS", None)
    if license_guard.DEV_FLAG.exists():
        license_guard.DEV_FLAG.unlink()
    assert license_guard._bypass_active() is False

    # Only env -> still inactive
    os.environ["DARIO_LICENSE_BYPASS"] = "1"
    assert license_guard._bypass_active() is False

    # Only flag -> still inactive
    os.environ.pop("DARIO_LICENSE_BYPASS")
    license_guard.DEV_FLAG.touch()
    assert license_guard._bypass_active() is False

    # Both -> active
    os.environ["DARIO_LICENSE_BYPASS"] = "1"
    assert license_guard._bypass_active() is True

    # Cleanup
    os.environ.pop("DARIO_LICENSE_BYPASS")
    license_guard.DEV_FLAG.unlink()
    return True


def test_bypass_lets_expired_through():
    _backup_license()
    try:
        _set_trial_expired()
        # Without bypass -> invalid
        os.environ.pop("DARIO_LICENSE_BYPASS", None)
        if license_guard.DEV_FLAG.exists():
            license_guard.DEV_FLAG.unlink()
        assert license_guard.is_valid() is False

        # With both bypass gates -> valid
        os.environ["DARIO_LICENSE_BYPASS"] = "1"
        license_guard.DEV_FLAG.touch()
        assert license_guard.is_valid() is True

        # Cleanup
        os.environ.pop("DARIO_LICENSE_BYPASS")
        license_guard.DEV_FLAG.unlink()
        return True
    finally:
        _restore_license()


def test_require_license_decorator_passes_when_valid():
    _backup_license()
    try:
        _set_pro()

        @license_guard.require_license("test")
        def some_fn(x):
            return x * 2

        assert some_fn(5) == 10
        return True
    finally:
        _restore_license()


def test_require_license_decorator_raises_when_expired():
    _backup_license()
    try:
        _set_trial_expired()
        os.environ.pop("DARIO_LICENSE_BYPASS", None)
        if license_guard.DEV_FLAG.exists():
            license_guard.DEV_FLAG.unlink()

        @license_guard.require_license("test")
        def some_fn(x):
            return x * 2

        try:
            some_fn(5)
            assert False, "should have raised RuntimeError"
        except RuntimeError as e:
            assert "License invalid" in str(e)
            return True
    finally:
        _restore_license()


def test_whitelist_paths_includes_health_license():
    assert "/health" in license_guard.WHITELIST_PATHS
    assert "/license" in license_guard.WHITELIST_PATHS
    assert "/license/activate" in license_guard.WHITELIST_PATHS
    return True


def test_enforce_or_exit_exits_on_expired():
    """Run a tiny Python subprocess that calls enforce_or_exit. Should exit 2."""
    _backup_license()
    try:
        _set_trial_expired()
        # Make sure bypass off
        env = os.environ.copy()
        env.pop("DARIO_LICENSE_BYPASS", None)
        if license_guard.DEV_FLAG.exists():
            license_guard.DEV_FLAG.unlink()
        result = subprocess.run(
            [sys.executable, "-c",
             f"import sys; sys.path.insert(0, r'{ORCH_DIR}'); "
             "from license_guard import enforce_or_exit; enforce_or_exit('test', quiet=True)"],
            env=env, capture_output=True, timeout=10,
        )
        assert result.returncode == 2, f"expected exit 2, got {result.returncode}"
        return True
    finally:
        _restore_license()


def test_enforce_or_exit_passes_on_pro():
    _backup_license()
    try:
        _set_pro()
        env = os.environ.copy()
        env.pop("DARIO_LICENSE_BYPASS", None)
        result = subprocess.run(
            [sys.executable, "-c",
             f"import sys; sys.path.insert(0, r'{ORCH_DIR}'); "
             "from license_guard import enforce_or_exit; enforce_or_exit('test', quiet=True); "
             "print('OK')"],
            env=env, capture_output=True, timeout=10, text=True,
        )
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}: {result.stderr}"
        assert "OK" in result.stdout
        return True
    finally:
        _restore_license()


def test_fastapi_middleware_callable():
    """Just verify the middleware function exists and is callable."""
    assert callable(license_guard.fastapi_middleware)
    return True


def test_check_returns_dict():
    lic = license_guard._check()
    assert isinstance(lic, dict)
    assert "valid" in lic
    return True


def test_cli_check_smoke():
    """CLI --check should exit 0 if license valid."""
    result = subprocess.run(
        [sys.executable, str(ORCH_DIR / "license_guard.py"), "--check"],
        capture_output=True, timeout=10,
    )
    # Either 0 (valid) or 2 (invalid) — both acceptable, just confirming no crash
    assert result.returncode in (0, 2)
    return True


TESTS = [
    ("is_valid returns true for PRO", test_is_valid_when_pro),
    ("is_valid returns false for expired trial", test_is_valid_when_expired),
    ("bypass requires both env AND flag", test_bypass_requires_both_env_and_flag),
    ("bypass lets expired through when active", test_bypass_lets_expired_through),
    ("@require_license passes on valid", test_require_license_decorator_passes_when_valid),
    ("@require_license raises on expired", test_require_license_decorator_raises_when_expired),
    ("WHITELIST_PATHS includes health+license", test_whitelist_paths_includes_health_license),
    ("enforce_or_exit exits 2 on expired", test_enforce_or_exit_exits_on_expired),
    ("enforce_or_exit exits 0 on PRO", test_enforce_or_exit_passes_on_pro),
    ("fastapi_middleware is callable", test_fastapi_middleware_callable),
    ("_check returns dict shape", test_check_returns_dict),
    ("CLI --check smoke", test_cli_check_smoke),
]


def run():
    passed = 0
    failed = 0
    for name, fn in TESTS:
        try:
            ok = fn()
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {name}")
            if ok:
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: CRASHED — {e}")
            failed += 1
    print()
    print(f"Results: {passed} passed, {failed} failed (of {len(TESTS)})")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run())

"""Property-based tests using Hypothesis (Faixa 2 #3).

Why property-based:
  Unit tests check specific inputs you THOUGHT of. Property tests generate
  thousands of random inputs to find edge cases you didn't think of.
  Hypothesis is the de-facto Python lib for this (used by pip, attrs, etc.).

Coverage focus:
  - safety/sandbox.py — env handling, output capture, never-leak invariants
  - core/audit_signing.py — sign/verify symmetry, canonicalization stability
  - core/secrets.py — round-trip preserves value (covered by stateful test)
  - safety/prompt_shield.py — sanitize idempotency, deny-list completeness
"""
from __future__ import annotations

import string
import sys
from pathlib import Path

import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


# ─── Strategies ──────────────────────────────────────────────────────────


# Plausible secret-like strings (ASCII printable, 8-128 chars)
secret_value_strategy = st.text(
    alphabet=string.ascii_letters + string.digits + "_-",
    min_size=8,
    max_size=128,
)

# Env var names (uppercase + underscores, conventional)
env_name_strategy = st.text(
    alphabet=string.ascii_uppercase + "_",
    min_size=1,
    max_size=40,
).filter(lambda s: s[0].isalpha())  # must start with letter


# ─── audit_signing: sign+verify symmetry ─────────────────────────────────


from core.audit_signing import (
    entry_hash,
    genesis_hash,
    sign_entry,
    verify_chain,
    verify_entry,
)


@given(
    actor=st.text(min_size=1, max_size=40, alphabet=string.ascii_letters),
    action=st.text(min_size=1, max_size=40, alphabet=string.ascii_letters + "_"),
    prev_hash=st.text(min_size=64, max_size=64, alphabet=string.hexdigits),
)
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_sign_verify_round_trip(actor, action, prev_hash):
    """Any signed entry verifies cleanly against its own prev_hash."""
    entry = {"actor": actor, "action": action}
    signed = sign_entry(entry, prev_hash=prev_hash)
    ok, reason = verify_entry(signed, expected_prev_hash=prev_hash)
    assert ok, f"sign/verify mismatch: {reason}"


@given(prev_hash=st.text(min_size=64, max_size=64, alphabet=string.hexdigits))
@settings(max_examples=30, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
def test_entry_hash_deterministic(prev_hash):
    """Same canonical entry + same prev_hash → same hash, always."""
    entry = {"actor": "x", "action": "y", "prev_hash": prev_hash}
    h1 = entry_hash(entry)
    h2 = entry_hash(entry)
    assert h1 == h2


@pytest.mark.slow  # 1-10 audit signs per example
@given(
    n=st.integers(min_value=1, max_value=10),
    day=st.dates(min_value=__import__("datetime").date(2024, 1, 1),
                 max_value=__import__("datetime").date(2030, 1, 1)).map(str),
)
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_chain_of_n_entries_verifies(n, day):
    """A chain of N freshly-signed entries always verifies end-to-end."""
    prev = genesis_hash(day)
    chain = []
    for i in range(n):
        signed = sign_entry({"actor": f"a{i}", "action": f"act{i}"}, prev_hash=prev)
        chain.append(signed)
        prev = entry_hash(signed)

    result = verify_chain(chain, day=day)
    assert result["ok"], f"chain of {n} entries broke: {result['reason']}"
    assert result["verified"] == n


# ─── safety/sandbox: env scoping invariants ──────────────────────────────


from safety.sandbox import (
    ENV_DENY_LIST,
    run_sandboxed,
)


@pytest.mark.slow  # subprocess per example
@given(
    env_name=env_name_strategy,
    env_value=secret_value_strategy,
)
@settings(max_examples=10, deadline=None,
          suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
def test_arbitrary_unlisted_env_var_never_leaks(env_name, env_value, monkeypatch):
    """For ANY env var name not in allowlist, value must not reach subprocess.

    This is the core invariant of the sandbox. Hypothesis tries random
    names + random values to find any that bypass the filter.
    """
    # Skip names that ARE in our SAFE_ENV_DEFAULTS (would legitimately pass)
    assume(env_name not in ("PATH", "PYTHONPATH", "PYTHONHOME", "PYTHONIOENCODING",
                            "TEMP", "TMP", "TMPDIR", "LANG", "LC_ALL", "LC_CTYPE",
                            "HOME", "USERPROFILE", "SYSTEMROOT", "WINDIR", "OS", "COMSPEC"))

    monkeypatch.setenv(env_name, env_value)
    result = run_sandboxed(
        [sys.executable, "-c",
         f"import os; print(repr(os.environ.get({env_name!r}, 'ABSENT')))"],
        caller="hypothesis-test",
        timeout_s=10,
    )
    assert env_value not in result.stdout, \
        f"VALUE LEAKED for env_name={env_name!r}, value={env_value!r}"


@pytest.mark.slow  # subprocess per example
@given(env_name=st.sampled_from(ENV_DENY_LIST), value=secret_value_strategy)
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_deny_list_entries_never_pass_via_extra(env_name, value):
    """For every deny-listed name, no value passes via env_extra either."""
    result = run_sandboxed(
        [sys.executable, "-c",
         f"import os; print(repr(os.environ.get({env_name!r}, 'BLOCKED')))"],
        caller="hypothesis-test",
        env_extra={env_name: value},
        timeout_s=10,
    )
    assert "BLOCKED" in result.stdout, f"{env_name} leaked"
    assert value not in result.stdout, f"value {value!r} leaked via {env_name}"


# ─── prompt_shield: sanitize idempotency ─────────────────────────────────


from safety.prompt_shield import inspect_output


@given(text=st.text(min_size=0, max_size=500, alphabet=st.characters(blacklist_categories=("Cs",))))
@settings(max_examples=30, deadline=5000)
def test_sanitize_is_idempotent(text):
    """Sanitizing already-sanitized text doesn't change it further.

    If inspect_output produces sanitized X, then inspect_output(X)["sanitized"]
    must equal X. Otherwise we'd have an infinite loop risk.
    """
    v1 = inspect_output(text)
    s1 = v1["sanitized"]
    v2 = inspect_output(s1)
    s2 = v2["sanitized"]
    assert s1 == s2, "sanitize not idempotent"


@given(text=st.text(min_size=0, max_size=500, alphabet=st.characters(blacklist_categories=("Cs",))))
@settings(max_examples=30, deadline=5000)
def test_sanitize_never_grows_text(text):
    """Sanitization is mask-or-keep — output length never exceeds input by
    more than the REDACTED-token expansion ratio (~3-5x worst case per match).
    """
    v = inspect_output(text)
    sanitized = v["sanitized"]
    # Allow up to 5x growth from masking (REDACTED tokens are ~20 chars)
    assert len(sanitized) <= max(len(text) * 5 + 100, 100), \
        f"sanitized grew suspiciously: {len(text)} → {len(sanitized)}"


# ─── core/secrets: round trip ────────────────────────────────────────────


keyring = pytest.importorskip("keyring")
from core.secrets import (
    SERVICE_NAME,
    delete_secret,
    get_secret,
    is_keyring_available,
    set_secret,
)


@pytest.mark.slow  # keyring + IO per example
@pytest.mark.skipif(not is_keyring_available(), reason="keyring backend unavailable")
@given(value=secret_value_strategy)
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_keyring_round_trip_preserves_value(value):
    """For any plausible secret value, set→get returns the same bytes."""
    import uuid
    name = f"hyp-test-{uuid.uuid4().hex[:10]}"
    set_secret(name, value, caller="hypothesis-test")
    try:
        retrieved = get_secret(name, caller="hypothesis-test")
        assert retrieved == value, f"round trip changed value: {value!r} → {retrieved!r}"
    finally:
        delete_secret(name, caller="hypothesis-test")

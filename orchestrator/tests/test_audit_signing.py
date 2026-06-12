"""Tests for the Ed25519 audit trail signing (Faixa 1 #5)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

cryptography = pytest.importorskip("cryptography")  # skip if not installed

from core.audit_signing import (
    entry_hash,
    genesis_hash,
    seal_day,
    sign_entry,
    verify_chain,
    verify_entry,
    verify_seal,
)

# ─── Hashing primitives ──────────────────────────────────────────────────


def test_canonicalization_is_deterministic():
    """Same entry produces same hash regardless of key order."""
    e1 = {"actor": "a", "action": "b", "timestamp": "2026-05-25T00:00:00Z"}
    e2 = {"timestamp": "2026-05-25T00:00:00Z", "actor": "a", "action": "b"}
    assert entry_hash(e1) == entry_hash(e2)


def test_entry_hash_changes_with_prev_hash():
    """Changing prev_hash changes the full hash (chain link)."""
    entry = {"actor": "x", "action": "y"}
    h1 = entry_hash({**entry, "prev_hash": "AAA"})
    h2 = entry_hash({**entry, "prev_hash": "BBB"})
    assert h1 != h2


def test_genesis_hash_per_day():
    """Each day gets a unique genesis hash."""
    g1 = genesis_hash("2026-05-25")
    g2 = genesis_hash("2026-05-26")
    assert g1 != g2
    assert len(g1) == 64  # SHA-256 hex


# ─── Signing + verification ──────────────────────────────────────────────


def test_sign_entry_adds_sig_and_prev_hash():
    entry = {"actor": "test", "action": "create"}
    signed = sign_entry(entry, prev_hash="abc123")
    assert "sig" in signed
    assert signed["prev_hash"] == "abc123"
    # Original entry unchanged
    assert "sig" not in entry


def test_verify_entry_passes_for_valid_signature():
    entry = {"actor": "test", "action": "create"}
    signed = sign_entry(entry, prev_hash="abc")
    ok, reason = verify_entry(signed, expected_prev_hash="abc")
    assert ok, reason


def test_verify_entry_detects_tampered_content():
    """Modifying any field after signing breaks verification."""
    entry = {"actor": "alice", "action": "delete"}
    signed = sign_entry(entry, prev_hash="abc")
    signed["actor"] = "bob"  # tamper
    ok, reason = verify_entry(signed, expected_prev_hash="abc")
    assert not ok
    assert "signature verification failed" in reason


def test_verify_entry_detects_chain_break():
    """Wrong expected_prev_hash means the chain doesn't link properly."""
    entry = {"actor": "x", "action": "y"}
    signed = sign_entry(entry, prev_hash="abc")
    ok, reason = verify_entry(signed, expected_prev_hash="DIFFERENT")
    assert not ok
    assert "prev_hash mismatch" in reason or "chain broken" in reason


def test_verify_entry_rejects_missing_sig():
    entry = {"actor": "x", "action": "y", "prev_hash": "abc"}  # no sig
    ok, reason = verify_entry(entry, expected_prev_hash="abc")
    assert not ok
    assert "missing sig" in reason


# ─── Chain verification ──────────────────────────────────────────────────


def test_verify_chain_passes_for_clean_sequence():
    """Build a 3-entry chain manually and verify end-to-end."""
    day = "2026-05-25"
    prev = genesis_hash(day)
    entries = []
    for i in range(3):
        signed = sign_entry({"actor": f"a{i}", "action": f"act{i}"}, prev_hash=prev)
        entries.append(signed)
        prev = entry_hash(signed)

    result = verify_chain(entries, day=day)
    assert result["ok"], result["reason"]
    assert result["verified"] == 3
    assert result["broken_at"] is None


def test_verify_chain_detects_break_at_middle():
    """Tamper with entry #1 (of 3) — verify catches it."""
    day = "2026-05-25"
    prev = genesis_hash(day)
    entries = []
    for i in range(3):
        signed = sign_entry({"actor": f"a{i}"}, prev_hash=prev)
        entries.append(signed)
        prev = entry_hash(signed)

    # Tamper middle
    entries[1]["actor"] = "evil"

    result = verify_chain(entries, day=day)
    assert not result["ok"]
    assert result["broken_at"] == 1
    assert result["verified"] == 1  # entry 0 passed, then break


def test_verify_chain_detects_deletion():
    """Deleting an entry breaks the chain at the gap."""
    day = "2026-05-25"
    prev = genesis_hash(day)
    entries = []
    for i in range(3):
        signed = sign_entry({"actor": f"a{i}"}, prev_hash=prev)
        entries.append(signed)
        prev = entry_hash(signed)

    # Delete middle entry — now entry[2]'s prev_hash references the deleted
    # entry, so verification of entry[1] (originally entry[2]) fails.
    entries.pop(1)

    result = verify_chain(entries, day=day)
    assert not result["ok"]
    assert result["broken_at"] == 1


def test_verify_chain_empty_is_ok():
    result = verify_chain([], day="2026-05-25")
    assert result["ok"]
    assert result["total"] == 0


# ─── Daily seal ──────────────────────────────────────────────────────────


def test_seal_day_produces_signed_root():
    day = "2026-05-25"
    prev = genesis_hash(day)
    entries = []
    for i in range(2):
        s = sign_entry({"actor": f"a{i}"}, prev_hash=prev)
        entries.append(s)
        prev = entry_hash(s)

    seal = seal_day(entries, day)
    assert seal["day"] == day
    assert seal["count"] == 2
    assert seal["final_hash"] == entry_hash(entries[-1])
    assert "sig" in seal


def test_verify_seal_passes():
    seal = seal_day([], "2026-05-25")
    ok, reason = verify_seal(seal)
    assert ok, reason


def test_verify_seal_detects_tampered_count():
    seal = seal_day([], "2026-05-25")
    seal["count"] = 999  # tamper
    ok, reason = verify_seal(seal)
    assert not ok

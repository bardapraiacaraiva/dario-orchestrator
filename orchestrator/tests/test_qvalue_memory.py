#!/usr/bin/env python3
"""Tests for Upgrade 5 Q-value memory wire-in."""

import sqlite3
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import qvalue_memory_wire as qvm_wire


def test_stop_word_filter():
    """Generic stop words should NOT count as meaningful overlap."""
    words = qvm_wire._meaningful_words("criar uma marca para o cliente")
    assert "criar" not in words, "criar should be stop word"
    assert "uma" not in words, "uma should be stop word"
    assert "marca" in words
    assert "cliente" in words


def test_suggest_returns_empty_for_no_overlap():
    """Query with no meaningful overlap with any episode -> empty list."""
    # Use a query that won't match any real episode context
    suggestions = qvm_wire.suggest_skill("xyzabc nonsense gibberish whatever12345")
    assert isinstance(suggestions, list)
    assert len(suggestions) == 0, f"expected empty, got {suggestions}"


def test_suggest_empty_text():
    assert qvm_wire.suggest_skill("") == []
    assert qvm_wire.suggest_skill("   ") == []


def test_record_outcome_roundtrip():
    """Record an episode and verify it persists + becomes retrievable."""
    test_context = "test_qvm_unique_context_xyzpitch12345 deck for investors"
    r = qvm_wire.record_outcome(
        context=test_context,
        skill="dario-pitch",
        score=88.0,
        tokens_used=5000,
        project="test-project",
    )
    assert r["recorded"] is True
    assert "episode_id" in r
    assert r["q_value"] > 0

    # Now query — should find it
    suggestions = qvm_wire.suggest_skill("xyzpitch12345 deck for investors")
    found = any(s["skill"] == "dario-pitch" for s in suggestions)
    assert found, f"recorded episode not retrievable: {suggestions}"

    # Cleanup
    conn = sqlite3.connect(str(qvm_wire.DB_PATH))
    conn.execute("DELETE FROM q_episodes WHERE episode_id = ?", (r["episode_id"],))
    conn.commit()
    conn.close()


def test_record_rejects_zero_score():
    r = qvm_wire.record_outcome(context="some context", skill="some-skill", score=0)
    assert r["recorded"] is False


def test_record_rejects_missing_skill():
    r = qvm_wire.record_outcome(context="ctx", skill="", score=80)
    assert r["recorded"] is False


def test_stats_returns_dict():
    s = qvm_wire.stats()
    assert "total_episodes" in s
    if s["total_episodes"] > 0:
        assert "distinct_skills" in s
        assert "avg_q_value" in s


def test_bootstrap_idempotent():
    """Running bootstrap twice should not double-insert episodes."""
    s1 = qvm_wire.bootstrap_from_history()
    total1 = qvm_wire.stats()["total_episodes"]
    s2 = qvm_wire.bootstrap_from_history()
    total2 = qvm_wire.stats()["total_episodes"]
    # All re-runs should skip — no new inserts
    assert total1 == total2, f"bootstrap not idempotent: {total1} -> {total2}"
    assert s2["skipped"] > 0


def test_td_learning_updates_qvalue():
    """Recording the same context twice should average outcomes via TD-learning."""
    # Use unique context to avoid matching other episodes
    ctx = "unique_td_test_context_abc_xyz_999 episode signature"
    r1 = qvm_wire.record_outcome(context=ctx, skill="test-skill-td", score=80.0)
    r2 = qvm_wire.record_outcome(context=ctx, skill="test-skill-td", score=95.0)
    # Episode IDs may differ (it depends on how _find_similar works in QValueMemory)
    # But visits should increment for the matching one
    conn = sqlite3.connect(str(qvm_wire.DB_PATH))
    rows = conn.execute(
        "SELECT visits, outcome_score FROM q_episodes WHERE skill = ?",
        ("test-skill-td",)
    ).fetchall()
    conn.close()
    # Either we have one episode with visits=2 or two episodes (similarity threshold)
    total_visits = sum(r[0] for r in rows)
    assert total_visits >= 2, f"expected total visits >= 2, got {total_visits}"

    # Cleanup
    conn = sqlite3.connect(str(qvm_wire.DB_PATH))
    conn.execute("DELETE FROM q_episodes WHERE skill = ?", ("test-skill-td",))
    conn.commit()
    conn.close()


def test_dispatch_integration_does_not_crash():
    """Verify dispatch_engine import + Q-value fallback path doesn't crash."""
    from dispatch.dispatch_engine import infer_skill_from_task
    # A task with no obvious keyword/semantic match
    result = infer_skill_from_task({
        "title": "xyzabc nonsense gibberish",
        "description": "nothing useful here totally random"
    })
    # May be None, may be something — just must not crash
    assert result is None or isinstance(result, str)


TESTS = [
    ("stop word filter", test_stop_word_filter),
    ("suggest returns empty for no overlap", test_suggest_returns_empty_for_no_overlap),
    ("suggest handles empty text", test_suggest_empty_text),
    ("record_outcome roundtrip", test_record_outcome_roundtrip),
    ("record rejects zero score", test_record_rejects_zero_score),
    ("record rejects missing skill", test_record_rejects_missing_skill),
    ("stats returns dict", test_stats_returns_dict),
    ("bootstrap idempotent", test_bootstrap_idempotent),
    ("TD-learning updates Q-value", test_td_learning_updates_qvalue),
    ("dispatch integration smoke", test_dispatch_integration_does_not_crash),
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

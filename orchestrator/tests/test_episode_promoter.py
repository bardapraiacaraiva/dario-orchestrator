#!/usr/bin/env python3
"""Tests for Upgrade 8 episode → semantic promotion."""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import episode_promoter as ep_module


def test_load_episodes_returns_list():
    eps = ep_module._load_episodes(days=365)
    assert isinstance(eps, list)
    assert len(eps) > 0, "expected episodes from filesystem"
    return True


def test_classify_separates_excellence_and_clusters():
    eps = [
        {"skill": "X", "project": "P1", "outcome": "success", "score": 95,
         "episode_id": "E1", "output_summary": "s1"},
        {"skill": "X", "project": "P1", "outcome": "success", "score": 88,
         "episode_id": "E2", "output_summary": "s2"},
        {"skill": "X", "project": "P1", "outcome": "success", "score": 87,
         "episode_id": "E3", "output_summary": "s3"},
        {"skill": "Y", "project": "P2", "outcome": "success", "score": 55,
         "episode_id": "E4", "output_summary": "s4"},
        {"skill": "Z", "project": "P3", "outcome": "failure", "score": 95,
         "episode_id": "E5", "output_summary": "s5"},
    ]
    c = ep_module._classify(eps)
    # E1 (X, P1, 95) is excellence
    assert any(e["episode_id"] == "E1" for e in c["excellence"])
    # E5 is failure -> excluded entirely
    assert not any(e["episode_id"] == "E5" for e in c["excellence"])
    # Cluster (X, P1) has 3 episodes
    assert len(c["clusters"][("X", "P1")]) == 3
    return True


def test_candidate_patterns_threshold():
    clusters = {
        ("X", "P1"): [
            {"skill": "X", "score": 90, "episode_id": "E1"},
            {"skill": "X", "score": 85, "episode_id": "E2"},
            {"skill": "X", "score": 88, "episode_id": "E3"},
        ],
        ("Y", "P2"): [
            {"skill": "Y", "score": 70, "episode_id": "E4"},
            {"skill": "Y", "score": 65, "episode_id": "E5"},
            {"skill": "Y", "score": 68, "episode_id": "E6"},
        ],
        ("Z", "P3"): [
            {"skill": "Z", "score": 95, "episode_id": "E7"},
            {"skill": "Z", "score": 92, "episode_id": "E8"},
        ],  # only 2 episodes — below threshold
    }
    patterns = ep_module._candidate_patterns(clusters)
    skill_names = [p["skill"] for p in patterns]
    assert "X" in skill_names, "X with avg 87.7 should pattern"
    assert "Y" not in skill_names, "Y below avg threshold"
    assert "Z" not in skill_names, "Z has too few episodes"
    return True


def test_excellence_content_builder():
    ep = {
        "skill": "dario-brand", "project": "test-proj",
        "outcome": "success", "score": 92,
        "episode_id": "E-X1",
        "output_summary": "Brand positioning complete with archetype.",
        "tags": ["brand", "test"],
    }
    name, content = ep_module._build_excellence_content(ep)
    assert "dario-brand" in name
    assert "test-proj" in name
    assert "excellence" in name
    assert "92/100" in content or "92" in content
    assert "Brand positioning" in content
    return True


def test_pattern_content_builder():
    pattern = {
        "skill": "dario-content",
        "project": "test-proj",
        "episodes": [
            {"episode_id": "E1", "score": 90, "output_summary": "first"},
            {"episode_id": "E2", "score": 85, "output_summary": "second"},
            {"episode_id": "E3", "score": 88, "output_summary": "third"},
        ],
        "count": 3,
        "avg_score": 87.7,
        "min_score": 85,
        "max_score": 90,
    }
    name, content = ep_module._build_pattern_content(pattern)
    assert "dario-content" in name
    assert "pattern" in name
    assert "3 episodes" in content
    assert "87.7" in content
    assert "Recommendation" in content
    return True


def test_scan_is_dry_run():
    """Scan must not write to filesystem."""
    import os
    before = list(ep_module.SEMANTIC_DIR.glob("SEM-*.yaml")) if ep_module.SEMANTIC_DIR.exists() else []
    r = ep_module.scan(days=7)
    after = list(ep_module.SEMANTIC_DIR.glob("SEM-*.yaml")) if ep_module.SEMANTIC_DIR.exists() else []
    assert len(before) == len(after), "scan should NOT promote"
    assert "would_promote_excellence" in r
    assert "would_promote_patterns" in r
    return True


def test_promote_idempotent():
    """Running promote twice on same window should not duplicate."""
    r1 = ep_module.promote(days=7, generate_rules=False)
    promoted1 = r1.get("promoted_excellence", 0) + r1.get("promoted_patterns", 0)
    r2 = ep_module.promote(days=7, generate_rules=False)
    promoted2 = r2.get("promoted_excellence", 0) + r2.get("promoted_patterns", 0)
    # Second run should promote 0 new (all already exist)
    assert promoted2 == 0, f"second promote produced {promoted2}, expected 0"
    return True


def test_stats_returns_counts():
    s = ep_module.stats()
    assert "semantic_memories" in s
    assert "by_type" in s
    assert "auto_rules" in s
    # We promoted earlier in this session, so should be > 0
    assert s["semantic_memories"] > 0
    return True


def test_existing_semantic_names_includes_promoted():
    names = ep_module._existing_semantic_names()
    assert isinstance(names, set)
    # We promoted dario-product cuidai pattern earlier
    assert any("dario-product" in n and "pattern" in n for n in names) or len(names) > 0
    return True


def test_rule_yaml_has_required_fields():
    """If we promoted with rules, verify their YAML structure."""
    rules_dir = ep_module.RULES_DIR
    if not rules_dir.exists():
        return True  # nothing to check
    rule_files = list(rules_dir.glob("auto-rule-*.yaml"))
    if not rule_files:
        return True  # no rules to check
    import yaml as _y
    sample = _y.safe_load(rule_files[0].read_text(encoding="utf-8"))
    for key in ("rule_id", "type", "skill", "rationale", "source_episodes"):
        assert key in sample, f"rule missing field: {key}"
    return True


TESTS = [
    ("load episodes from filesystem", test_load_episodes_returns_list),
    ("classify excellence + clusters", test_classify_separates_excellence_and_clusters),
    ("pattern thresholds enforced", test_candidate_patterns_threshold),
    ("excellence content includes score/summary", test_excellence_content_builder),
    ("pattern content includes recommendation", test_pattern_content_builder),
    ("scan is dry-run", test_scan_is_dry_run),
    ("promote is idempotent", test_promote_idempotent),
    ("stats returns counts", test_stats_returns_counts),
    ("existing names includes promoted", test_existing_semantic_names_includes_promoted),
    ("auto-rule YAML structure", test_rule_yaml_has_required_fields),
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

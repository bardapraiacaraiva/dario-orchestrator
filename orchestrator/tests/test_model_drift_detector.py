"""Tests for v4 schema + check_model_drift (Risk #10 stamp+warn)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


@pytest.fixture
def fresh_db(tmp_path):
    from db import DB
    return DB(db_path=str(tmp_path / "test_v4.db"))


class TestSchemaV4:
    def test_schema_version_4_present(self, fresh_db):
        with fresh_db._conn() as conn:
            versions = [r["version"] for r in
                        conn.execute("SELECT version FROM schema_versions").fetchall()]
        assert 4 in versions

    def test_polished_runs_has_model_used(self, fresh_db):
        with fresh_db._conn() as conn:
            cols = [r[1] for r in conn.execute("PRAGMA table_info(polished_runs)").fetchall()]
        assert "model_used" in cols

    def test_model_drift_events_table_exists(self, fresh_db):
        with fresh_db._conn() as conn:
            row = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='model_drift_events'"
            ).fetchone()
        assert row is not None


class TestRecordPolishedRunWithModel:
    def test_model_used_persisted(self, fresh_db):
        fresh_db.record_polished_run(
            skill="s", client="c", v1_score=80, v2_score=88,
            final="v2", gate_decision="revised",
            model_used="claude-opus-4-7",
        )
        runs = fresh_db.get_polished_runs()
        assert runs[0]["model_used"] == "claude-opus-4-7"

    def test_model_used_optional_defaults_empty(self, fresh_db):
        fresh_db.record_polished_run(
            skill="s", client="c", v1_score=80, v2_score=88,
            final="v2", gate_decision="revised",
        )
        runs = fresh_db.get_polished_runs()
        assert runs[0]["model_used"] == ""


class TestRecordModelDrift:
    def test_insert_drift_event(self, fresh_db):
        row_id = fresh_db.record_model_drift(
            skill="dario-pitch-polished",
            declared_model="claude-opus-4-7",
            actual_model="claude-sonnet-4-6",
        )
        assert row_id > 0
        events = fresh_db.get_drift_events()
        assert events[0]["declared_model"] == "claude-opus-4-7"
        assert events[0]["actual_model"] == "claude-sonnet-4-6"
        assert events[0]["severity"] == "warning"

    def test_invalid_severity_rejected(self, fresh_db):
        with pytest.raises(ValueError, match="severity"):
            fresh_db.record_model_drift("s", "a", "b", severity="bogus")

    def test_empty_models_rejected(self, fresh_db):
        with pytest.raises(ValueError):
            fresh_db.record_model_drift("s", "", "b")
        with pytest.raises(ValueError):
            fresh_db.record_model_drift("s", "a", "")

    def test_filter_by_skill(self, fresh_db):
        fresh_db.record_model_drift("skill_a", "a", "b")
        fresh_db.record_model_drift("skill_b", "a", "b")
        events_a = fresh_db.get_drift_events(skill="skill_a")
        assert len(events_a) == 1
        assert events_a[0]["skill"] == "skill_a"


class TestDriftScanLogic:
    """Scan/detect logic from scripts.check_model_drift."""

    def test_scan_no_runs_no_drift(self, fresh_db, monkeypatch):
        import scripts.check_model_drift as drift
        monkeypatch.setattr(drift, "read_tested_with_model", lambda s: "claude-opus-4-7")
        result = drift.scan(fresh_db, since_iso=None, dry_run=False)
        assert result["drift_detected"] == 0

    def test_scan_matching_model_no_drift(self, fresh_db, monkeypatch):
        import scripts.check_model_drift as drift
        monkeypatch.setattr(drift, "read_tested_with_model", lambda s: "claude-opus-4-7")
        fresh_db.record_polished_run(
            skill="dario-pitch-polished", client="c", v1_score=80, v2_score=88,
            final="v2", gate_decision="revised", model_used="claude-opus-4-7",
        )
        result = drift.scan(fresh_db, since_iso=None, dry_run=False)
        assert result["drift_detected"] == 0
        assert result["logged"] == 0

    def test_scan_mismatched_model_drifts(self, fresh_db, monkeypatch):
        import scripts.check_model_drift as drift
        monkeypatch.setattr(drift, "read_tested_with_model", lambda s: "claude-opus-4-7")
        fresh_db.record_polished_run(
            skill="dario-pitch-polished", client="c", v1_score=80, v2_score=88,
            final="v2", gate_decision="revised", model_used="claude-sonnet-4-6",
        )
        result = drift.scan(fresh_db, since_iso=None, dry_run=False)
        assert result["drift_detected"] == 1
        assert result["logged"] == 1
        events = fresh_db.get_drift_events()
        assert len(events) == 1
        assert events[0]["declared_model"] == "claude-opus-4-7"
        assert events[0]["actual_model"] == "claude-sonnet-4-6"

    def test_dry_run_does_not_persist(self, fresh_db, monkeypatch):
        import scripts.check_model_drift as drift
        monkeypatch.setattr(drift, "read_tested_with_model", lambda s: "claude-opus-4-7")
        fresh_db.record_polished_run(
            skill="dario-pitch-polished", client="c", v1_score=80, v2_score=88,
            final="v2", gate_decision="revised", model_used="claude-sonnet-4-6",
        )
        result = drift.scan(fresh_db, since_iso=None, dry_run=True)
        assert result["drift_detected"] == 1
        assert result["logged"] == 0
        assert fresh_db.get_drift_events() == []

    def test_skip_runs_without_model_used(self, fresh_db, monkeypatch):
        import scripts.check_model_drift as drift
        monkeypatch.setattr(drift, "read_tested_with_model", lambda s: "claude-opus-4-7")
        fresh_db.record_polished_run(
            skill="dario-pitch-polished", client="c", v1_score=80, v2_score=88,
            final="v2", gate_decision="revised",  # no model_used
        )
        result = drift.scan(fresh_db, since_iso=None, dry_run=False)
        assert result["skipped_no_model_used"] == 1
        assert result["drift_detected"] == 0

    def test_skip_skill_without_declaration(self, fresh_db, monkeypatch):
        import scripts.check_model_drift as drift
        monkeypatch.setattr(drift, "read_tested_with_model", lambda s: None)
        result = drift.scan(fresh_db, since_iso=None, dry_run=False)
        assert result["wrappers_with_declaration"] == 0


class TestReadTestedWithModel:
    def test_extracts_from_frontmatter(self, tmp_path, monkeypatch):
        fake_skill_dir = tmp_path / "skills" / "test-polished"
        fake_skill_dir.mkdir(parents=True)
        (fake_skill_dir / "SKILL.md").write_text(
            "---\nname: test-polished\ntested_with_model: claude-opus-4-7\n---\n# Body",
            encoding="utf-8",
        )
        import scripts.check_model_drift as drift
        monkeypatch.setattr(drift, "SKILLS_DIR", tmp_path / "skills")
        assert drift.read_tested_with_model("test-polished") == "claude-opus-4-7"

    def test_returns_none_when_missing(self, tmp_path, monkeypatch):
        fake_skill_dir = tmp_path / "skills" / "test-polished"
        fake_skill_dir.mkdir(parents=True)
        (fake_skill_dir / "SKILL.md").write_text(
            "---\nname: test-polished\n---\n# Body",
            encoding="utf-8",
        )
        import scripts.check_model_drift as drift
        monkeypatch.setattr(drift, "SKILLS_DIR", tmp_path / "skills")
        assert drift.read_tested_with_model("test-polished") is None

    def test_returns_none_when_skill_missing(self, tmp_path, monkeypatch):
        import scripts.check_model_drift as drift
        monkeypatch.setattr(drift, "SKILLS_DIR", tmp_path / "skills")
        assert drift.read_tested_with_model("nonexistent") is None


class TestLiveWrappersHaveDeclaration:
    """Drift guard: all 8 polished wrappers must declare tested_with_model."""

    def test_all_wrappers_declare(self):
        from scripts.check_model_drift import POLISHED_WRAPPERS, read_tested_with_model
        missing = [w for w in POLISHED_WRAPPERS if not read_tested_with_model(w)]
        assert not missing, (
            f"Wrappers missing tested_with_model frontmatter: {missing}. "
            "Run: scripts/_oneoff_inject_model_used_flag.py or add manually."
        )

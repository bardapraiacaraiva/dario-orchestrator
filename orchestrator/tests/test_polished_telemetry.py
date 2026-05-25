"""Tests for Padrão A telemetry scripts (record + aggregate)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from scripts.record_polished_run import VALID_GATE_DECISIONS, append_run
from scripts.aggregate_polished_metrics import aggregate, load_runs


@pytest.fixture
def temp_runs_file(tmp_path, monkeypatch):
    """Redirect RUNS_FILE to a tmp path AND point SQLite DB at a fresh tmp file
    so the aggregator's DB-first read doesn't pick up the production database."""
    fake = tmp_path / "polished_production_runs.yaml"
    fake_db = tmp_path / "test_orchestrator.db"
    monkeypatch.setattr("scripts.record_polished_run.RUNS_FILE", fake)
    monkeypatch.setattr("scripts.aggregate_polished_metrics.RUNS_FILE", fake)
    from core import db as _db_module
    monkeypatch.setattr(_db_module, "DB_PATH", fake_db)
    return fake


# ─────────────────────────────────────────────────────────────────────
# Recorder: validation
# ─────────────────────────────────────────────────────────────────────

class TestRecorderValidation:

    def test_valid_revised_entry(self, temp_runs_file):
        entry = append_run(
            skill="dario-pitch-polished", v1_score=80, v2_score=88,
            final="v2", client="test", gate_decision="revised",
        )
        assert entry["lift_pts"] == 8
        assert entry["final"] == "v2"

    def test_valid_ship_v1_entry(self, temp_runs_file):
        entry = append_run(
            skill="dario-brand-polished", v1_score=92, v2_score=None,
            final="v1", client="test", gate_decision="ship_v1",
        )
        assert entry["lift_pts"] == 0

    def test_valid_aborted_entry(self, temp_runs_file):
        entry = append_run(
            skill="dario-funnel-polished", v1_score=67, v2_score=None,
            final="aborted", client="test", gate_decision="aborted",
        )
        assert entry["gate_decision"] == "aborted"
        assert entry["lift_pts"] == 0

    def test_invalid_gate_decision_rejected(self, temp_runs_file):
        with pytest.raises(ValueError, match="gate_decision"):
            append_run(skill="x", v1_score=80, v2_score=88, final="v2",
                       client="t", gate_decision="bogus")

    def test_invalid_v1_score_rejected(self, temp_runs_file):
        with pytest.raises(ValueError, match="v1_score"):
            append_run(skill="x", v1_score=150, v2_score=None, final="v1",
                       client="t", gate_decision="ship_v1")

    def test_invalid_v2_score_rejected(self, temp_runs_file):
        with pytest.raises(ValueError, match="v2_score"):
            append_run(skill="x", v1_score=80, v2_score=-5, final="v2",
                       client="t", gate_decision="revised")

    def test_invalid_final_rejected(self, temp_runs_file):
        with pytest.raises(ValueError, match="final"):
            append_run(skill="x", v1_score=80, v2_score=88, final="vfinal",
                       client="t", gate_decision="revised")

    def test_aborted_with_non_aborted_final_rejected(self, temp_runs_file):
        with pytest.raises(ValueError, match="aborted"):
            append_run(skill="x", v1_score=70, v2_score=None, final="v1",
                       client="t", gate_decision="aborted")

    def test_ship_v1_with_v2_score_rejected(self, temp_runs_file):
        with pytest.raises(ValueError, match="ship_v1"):
            append_run(skill="x", v1_score=92, v2_score=88, final="v1",
                       client="t", gate_decision="ship_v1")


# ─────────────────────────────────────────────────────────────────────
# Recorder: append-only behavior
# ─────────────────────────────────────────────────────────────────────

class TestAppendOnly:

    def test_multiple_appends_accumulate(self, temp_runs_file):
        append_run(skill="dario-pitch-polished", v1_score=80, v2_score=88,
                   final="v2", client="c1", gate_decision="revised")
        append_run(skill="dario-pitch-polished", v1_score=82, v2_score=90,
                   final="v2", client="c2", gate_decision="revised")
        runs = load_runs()
        assert len(runs) == 2
        assert runs[0]["client"] == "c1"
        assert runs[1]["client"] == "c2"

    def test_optional_fields_persisted(self, temp_runs_file):
        append_run(skill="dario-brand-polished", v1_score=85, v2_score=92,
                   final="v2", client="test", gate_decision="revised",
                   status_mix="5/2/3", notes="test note")
        runs = load_runs()
        assert runs[0]["status_mix"] == "5/2/3"
        assert runs[0]["notes"] == "test note"

    def test_schema_version_preserved(self, temp_runs_file):
        append_run(skill="x", v1_score=80, v2_score=88, final="v2",
                   client="t", gate_decision="revised")
        import yaml
        data = yaml.safe_load(temp_runs_file.read_text(encoding="utf-8"))
        assert data["schema_version"] == 1


# ─────────────────────────────────────────────────────────────────────
# Aggregator
# ─────────────────────────────────────────────────────────────────────

class TestAggregator:

    def _seed(self, temp_runs_file, entries):
        for e in entries:
            append_run(**e)

    def test_empty_runs_returns_zero(self, temp_runs_file):
        agg = aggregate([])
        assert agg["overall"]["n_runs"] == 0
        assert agg["overall"]["gate_pass_rate"] == 0.0
        assert agg["overall"]["mean_lift_pts"] is None

    def test_single_passed_run(self, temp_runs_file):
        self._seed(temp_runs_file, [
            dict(skill="dario-pitch-polished", v1_score=80, v2_score=88,
                 final="v2", client="c1", gate_decision="revised"),
        ])
        agg = aggregate(load_runs())
        assert agg["overall"]["mean_lift_pts"] == 8.0
        assert agg["overall"]["gate_pass_rate"] == 1.0

    def test_mixed_passed_and_aborted(self, temp_runs_file):
        self._seed(temp_runs_file, [
            dict(skill="dario-pitch-polished", v1_score=80, v2_score=88,
                 final="v2", client="c1", gate_decision="revised"),
            dict(skill="dario-pitch-polished", v1_score=67, v2_score=None,
                 final="aborted", client="c2", gate_decision="aborted"),
            dict(skill="dario-pitch-polished", v1_score=82, v2_score=90,
                 final="v2", client="c3", gate_decision="revised"),
        ])
        agg = aggregate(load_runs())
        assert agg["overall"]["n_runs"] == 3
        assert agg["overall"]["n_passed"] == 2
        assert agg["overall"]["n_aborted"] == 1
        assert agg["overall"]["gate_pass_rate"] == round(2/3, 3)
        assert agg["overall"]["mean_lift_pts"] == 8.0  # mean(8, 8)

    def test_per_skill_segregation(self, temp_runs_file):
        self._seed(temp_runs_file, [
            dict(skill="dario-pitch-polished", v1_score=80, v2_score=88,
                 final="v2", client="c1", gate_decision="revised"),
            dict(skill="dario-funnel-polished", v1_score=82, v2_score=85,
                 final="v2", client="c2", gate_decision="revised"),
        ])
        agg = aggregate(load_runs())
        assert agg["per_skill"]["dario-pitch-polished"]["mean_lift_pts"] == 8.0
        assert agg["per_skill"]["dario-funnel-polished"]["mean_lift_pts"] == 3.0

    def test_window_filters_old_runs(self, temp_runs_file):
        # Insert one entry with a manually-old timestamp
        from datetime import UTC, datetime, timedelta
        import yaml
        old_ts = (datetime.now(UTC) - timedelta(days=60)).isoformat(timespec="seconds")
        data = {
            "schema_version": 1,
            "runs": [
                {"ts": old_ts, "skill": "dario-pitch-polished",
                 "client": "old", "gate_decision": "revised",
                 "v1_score": 80, "v2_score": 88, "final": "v2",
                 "lift_pts": 8},
            ],
        }
        temp_runs_file.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

        runs = load_runs()
        agg_30 = aggregate(runs, window_days=30)
        agg_all = aggregate(runs, window_days=None)
        assert agg_30["overall"]["n_runs"] == 0
        assert agg_all["overall"]["n_runs"] == 1


# ─────────────────────────────────────────────────────────────────────
# Constants sanity
# ─────────────────────────────────────────────────────────────────────

class TestConstants:

    def test_valid_gate_decisions_set(self):
        assert VALID_GATE_DECISIONS == {"revised", "ship_v1", "aborted"}

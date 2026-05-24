"""Tests for db.py v3 schema additions: polished_runs + api_spend tables.

Migration from YAML/JSONL to SQLite primary source of truth.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


@pytest.fixture
def fresh_db(tmp_path):
    """Fresh SQLite DB per test — no shared state."""
    from db import DB
    db_path = tmp_path / "test_orchestrator.db"
    return DB(db_path=str(db_path))


# ─────────────────────────────────────────────────────────────────────
# Schema migration
# ─────────────────────────────────────────────────────────────────────

class TestSchemaV3:

    def test_schema_version_3_present(self, fresh_db):
        with fresh_db._conn() as conn:
            rows = conn.execute(
                "SELECT version FROM schema_versions ORDER BY version"
            ).fetchall()
        versions = [r["version"] for r in rows]
        assert 3 in versions, f"v3 migration not applied, found: {versions}"

    def test_polished_runs_table_exists(self, fresh_db):
        with fresh_db._conn() as conn:
            row = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='polished_runs'"
            ).fetchone()
        assert row is not None

    def test_api_spend_table_exists(self, fresh_db):
        with fresh_db._conn() as conn:
            row = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='api_spend'"
            ).fetchone()
        assert row is not None

    def test_polished_runs_indexes_exist(self, fresh_db):
        with fresh_db._conn() as conn:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='polished_runs'"
            ).fetchall()
        index_names = {r["name"] for r in rows}
        assert "idx_polished_runs_skill" in index_names
        assert "idx_polished_runs_ts" in index_names

    def test_api_spend_indexes_exist(self, fresh_db):
        with fresh_db._conn() as conn:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='api_spend'"
            ).fetchall()
        index_names = {r["name"] for r in rows}
        assert "idx_api_spend_caller" in index_names
        assert "idx_api_spend_ts" in index_names


# ─────────────────────────────────────────────────────────────────────
# record_polished_run
# ─────────────────────────────────────────────────────────────────────

class TestPolishedRunsAPI:

    def test_insert_revised_run(self, fresh_db):
        row_id = fresh_db.record_polished_run(
            skill="dario-pitch-polished", client="cuidai",
            v1_score=80, v2_score=88, final="v2",
            gate_decision="revised",
        )
        assert row_id > 0

    def test_insert_aborted_run(self, fresh_db):
        row_id = fresh_db.record_polished_run(
            skill="dario-funnel-polished", client="test",
            v1_score=67, v2_score=None, final="aborted",
            gate_decision="aborted",
        )
        assert row_id > 0
        runs = fresh_db.get_polished_runs()
        assert runs[0]["lift_pts"] == 0
        assert runs[0]["v2_score"] is None

    def test_insert_ship_v1_run(self, fresh_db):
        row_id = fresh_db.record_polished_run(
            skill="dario-brand-polished", client="test",
            v1_score=92, v2_score=None, final="v1",
            gate_decision="ship_v1",
        )
        assert row_id > 0

    def test_invalid_gate_decision_rejected(self, fresh_db):
        with pytest.raises(ValueError, match="gate_decision"):
            fresh_db.record_polished_run(
                skill="x", client="y", v1_score=80, v2_score=88,
                final="v2", gate_decision="bogus",
            )

    def test_invalid_v1_score_rejected(self, fresh_db):
        with pytest.raises(ValueError, match="v1_score"):
            fresh_db.record_polished_run(
                skill="x", client="y", v1_score=150, v2_score=None,
                final="v1", gate_decision="ship_v1",
            )

    def test_aborted_with_non_aborted_final_rejected(self, fresh_db):
        with pytest.raises(ValueError, match="aborted"):
            fresh_db.record_polished_run(
                skill="x", client="y", v1_score=67, v2_score=None,
                final="v1", gate_decision="aborted",
            )


# ─────────────────────────────────────────────────────────────────────
# get_polished_runs filters
# ─────────────────────────────────────────────────────────────────────

class TestGetPolishedRuns:

    def _seed(self, db):
        db.record_polished_run("dario-pitch-polished", "cuidai",
                               80, 88, "v2", "revised",
                               ts="2026-05-24T10:00:00+00:00")
        db.record_polished_run("dario-pitch-polished", "saquei",
                               82, 90, "v2", "revised",
                               ts="2026-05-24T11:00:00+00:00")
        db.record_polished_run("dario-funnel-polished", "arrecada",
                               81, 89, "v2", "revised",
                               ts="2026-05-20T10:00:00+00:00")

    def test_empty_when_no_data(self, fresh_db):
        assert fresh_db.get_polished_runs() == []

    def test_filter_by_skill(self, fresh_db):
        self._seed(fresh_db)
        pitch_only = fresh_db.get_polished_runs(skill="dario-pitch-polished")
        assert len(pitch_only) == 2
        assert all(r["skill"] == "dario-pitch-polished" for r in pitch_only)

    def test_filter_by_since(self, fresh_db):
        self._seed(fresh_db)
        recent = fresh_db.get_polished_runs(since_iso="2026-05-24T00:00:00+00:00")
        assert len(recent) == 2

    def test_filter_by_month(self, fresh_db):
        self._seed(fresh_db)
        may = fresh_db.get_polished_runs(month="2026-05")
        assert len(may) == 3
        april = fresh_db.get_polished_runs(month="2026-04")
        assert len(april) == 0


# ─────────────────────────────────────────────────────────────────────
# api_spend
# ─────────────────────────────────────────────────────────────────────

class TestApiSpendAPI:

    def test_insert_spend(self, fresh_db):
        row_id = fresh_db.record_api_spend(
            caller="dspy/compile_sprint4",
            model="claude-opus-4-7",
            input_tokens=1000, output_tokens=500,
            cost_usd=0.0175,
        )
        assert row_id > 0
        rows = fresh_db.get_api_spend()
        assert len(rows) == 1
        assert rows[0]["total_tokens"] == 1500
        assert rows[0]["cost_usd"] == 0.0175

    def test_negative_tokens_rejected(self, fresh_db):
        with pytest.raises(ValueError, match="non-negative"):
            fresh_db.record_api_spend(caller="x", model="y",
                                     input_tokens=-1, output_tokens=0,
                                     cost_usd=0.01)

    def test_negative_cost_rejected(self, fresh_db):
        with pytest.raises(ValueError, match="non-negative"):
            fresh_db.record_api_spend(caller="x", model="y",
                                     input_tokens=0, output_tokens=0,
                                     cost_usd=-0.01)

    def test_empty_caller_rejected(self, fresh_db):
        with pytest.raises(ValueError, match="caller"):
            fresh_db.record_api_spend(caller="", model="y",
                                     input_tokens=0, output_tokens=0,
                                     cost_usd=0.01)

    def test_total_tokens_auto_computed(self, fresh_db):
        fresh_db.record_api_spend(caller="x", model="y",
                                  input_tokens=100, output_tokens=50,
                                  cost_usd=0.001)
        rows = fresh_db.get_api_spend()
        assert rows[0]["total_tokens"] == 150


class TestGetApiSpend:

    def _seed(self, db):
        db.record_api_spend(caller="dspy/compile", model="haiku",
                           input_tokens=100, output_tokens=50, cost_usd=0.0001,
                           ts="2026-05-24T10:00:00+00:00")
        db.record_api_spend(caller="dspy/compile", model="haiku",
                           input_tokens=200, output_tokens=100, cost_usd=0.0002,
                           ts="2026-05-24T11:00:00+00:00")
        db.record_api_spend(caller="judge/eval", model="opus",
                           input_tokens=500, output_tokens=250, cost_usd=0.0088,
                           ts="2026-05-20T10:00:00+00:00")

    def test_filter_by_caller(self, fresh_db):
        self._seed(fresh_db)
        dspy_only = fresh_db.get_api_spend(caller="dspy/compile")
        assert len(dspy_only) == 2

    def test_filter_by_month(self, fresh_db):
        self._seed(fresh_db)
        may = fresh_db.get_api_spend(month="2026-05")
        assert len(may) == 3

    def test_filter_by_since(self, fresh_db):
        self._seed(fresh_db)
        recent = fresh_db.get_api_spend(since_iso="2026-05-24T00:00:00+00:00")
        assert len(recent) == 2


# ─────────────────────────────────────────────────────────────────────
# Tenant isolation (multi-tenant readiness per RFC_MULTI_TENANT.md)
# ─────────────────────────────────────────────────────────────────────

class TestTenantIsolation:

    def test_polished_runs_isolated_by_tenant(self, fresh_db):
        fresh_db.record_polished_run("s", "c", 80, 88, "v2", "revised",
                                     tenant_id="tenant_a")
        fresh_db.record_polished_run("s", "c", 80, 88, "v2", "revised",
                                     tenant_id="tenant_b")
        assert len(fresh_db.get_polished_runs(tenant_id="tenant_a")) == 1
        assert len(fresh_db.get_polished_runs(tenant_id="tenant_b")) == 1
        assert len(fresh_db.get_polished_runs(tenant_id="default")) == 0

    def test_api_spend_isolated_by_tenant(self, fresh_db):
        fresh_db.record_api_spend(caller="x", model="y",
                                  input_tokens=0, output_tokens=0, cost_usd=0,
                                  tenant_id="tenant_a")
        fresh_db.record_api_spend(caller="x", model="y",
                                  input_tokens=0, output_tokens=0, cost_usd=0,
                                  tenant_id="tenant_b")
        assert len(fresh_db.get_api_spend(tenant_id="tenant_a")) == 1
        assert len(fresh_db.get_api_spend(tenant_id="tenant_b")) == 1


# ─────────────────────────────────────────────────────────────────────
# Concurrency — the original critique of YAML
# ─────────────────────────────────────────────────────────────────────

class TestConcurrentInsertsSafe:

    def test_100_sequential_inserts_no_loss(self, fresh_db):
        """SQLite + WAL handles rapid sequential inserts (the YAML failure mode)."""
        for i in range(100):
            fresh_db.record_api_spend(
                caller=f"caller_{i}",
                model="haiku",
                input_tokens=10, output_tokens=5,
                cost_usd=0.000015,
            )
        rows = fresh_db.get_api_spend()
        assert len(rows) == 100

    def test_concurrent_inserts_via_threads(self, fresh_db, tmp_path):
        """Multiple threads writing concurrently — sanity check WAL mode."""
        import threading
        from db import DB

        def worker(thread_id: int):
            local_db = DB(db_path=fresh_db.db_path)
            for i in range(10):
                local_db.record_api_spend(
                    caller=f"thread_{thread_id}",
                    model="haiku",
                    input_tokens=1, output_tokens=1,
                    cost_usd=0.0,
                )

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        rows = fresh_db.get_api_spend()
        assert len(rows) == 50, f"Expected 50 (5 threads × 10), got {len(rows)}"

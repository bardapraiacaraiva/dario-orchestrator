"""Behavior tests for the enforcement layer (Risk #1 thin layer).

These are REAL behavior tests, not content-of-markdown checks. Each
test exercises a code path and asserts a concrete outcome.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


# ─────────────────────────────────────────────────────────────────────
# Budget gate
# ─────────────────────────────────────────────────────────────────────

@pytest.fixture
def isolated_budget(tmp_path, monkeypatch):
    """Redirect budget dir + DB to tmp_path."""
    fake_budgets = tmp_path / "budgets"
    fake_budgets.mkdir()
    fake_db = tmp_path / "test_orch.db"
    monkeypatch.setattr("enforcement.budget_gate.BUDGETS_DIR", fake_budgets)
    import db as _db_module
    monkeypatch.setattr(_db_module, "DB_PATH", fake_db)
    return fake_budgets


class TestBudgetGate:

    def _write_budget(self, dir_path: Path, month: str, pct: float):
        (dir_path / f"{month}.yaml").write_text(
            yaml.safe_dump({"month": month, "percentage": pct,
                            "total_tokens_used": int(pct * 500_000),
                            "limit": 50_000_000}),
            encoding="utf-8",
        )

    def test_no_budget_file_returns_safe(self, isolated_budget):
        from enforcement.budget_gate import check_budget_or_raise
        result = check_budget_or_raise(month="2099-01")
        assert float(result.get("percentage", 0)) == 0.0

    def test_under_threshold_passes(self, isolated_budget):
        from enforcement.budget_gate import check_budget_or_raise
        self._write_budget(isolated_budget, "2099-02", pct=50.0)
        result = check_budget_or_raise(month="2099-02")
        assert result["percentage"] == 50.0

    def test_at_hardstop_raises(self, isolated_budget):
        from enforcement.budget_gate import check_budget_or_raise
        from enforcement import BudgetExceededError
        self._write_budget(isolated_budget, "2099-03", pct=95.0)
        with pytest.raises(BudgetExceededError, match="hard-stop"):
            check_budget_or_raise(month="2099-03")

    def test_above_hardstop_raises(self, isolated_budget):
        from enforcement.budget_gate import check_budget_or_raise
        from enforcement import BudgetExceededError
        self._write_budget(isolated_budget, "2099-04", pct=99.5)
        with pytest.raises(BudgetExceededError):
            check_budget_or_raise(month="2099-04")

    def test_custom_threshold(self, isolated_budget):
        """Custom hardstop_pct kwarg overrides default."""
        from enforcement.budget_gate import check_budget_or_raise
        from enforcement import BudgetExceededError
        self._write_budget(isolated_budget, "2099-05", pct=50.0)
        # Default would pass (50 < 95); custom 40 fails
        with pytest.raises(BudgetExceededError):
            check_budget_or_raise(month="2099-05", hardstop_pct=40)

    def test_is_budget_safe_returns_false_when_over(self, isolated_budget):
        from enforcement.budget_gate import is_budget_safe
        self._write_budget(isolated_budget, "2099-06", pct=99.0)
        assert is_budget_safe(month="2099-06") is False

    def test_picks_higher_source_value(self, isolated_budget):
        """Defensive: YAML says 50%, SQLite says 99% → must use 99%."""
        from enforcement.budget_gate import current_budget_state
        from db import DB
        self._write_budget(isolated_budget, "2099-07", pct=50.0)
        with DB()._conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO budget (month, tokens_used, token_limit, updated_at) "
                "VALUES (?, ?, ?, ?)",
                ("2099-07", 49_500_000, 50_000_000,
                 datetime.now(UTC).isoformat(timespec="seconds")),
            )
        state = current_budget_state(month="2099-07")
        assert state["percentage"] >= 99.0


# ─────────────────────────────────────────────────────────────────────
# Dispatch validator
# ─────────────────────────────────────────────────────────────────────

@pytest.fixture
def isolated_validator(tmp_path, monkeypatch):
    """Fake company.yaml + skills dir for validator tests."""
    fake_company = tmp_path / "company.yaml"
    fake_skills = tmp_path / "skills"
    fake_skills.mkdir()
    # Minimal workers config
    fake_company.write_text(yaml.safe_dump({
        "workers": {
            "worker-pitch": {
                "skill": "dario-pitch",
                "skill_client_facing": "dario-pitch-polished",
            },
            "worker-brand": {
                "skill": "dario-brand",
                "skill_client_facing": "dario-brand-polished",
                "requires_briefing_validation": True,
            },
            "worker-misc": {"skill": "some-skill"},
        }
    }), encoding="utf-8")
    # Create skill stubs
    for s in ("dario-pitch", "dario-pitch-polished", "dario-brand",
              "dario-brand-polished", "some-skill"):
        skill_dir = fake_skills / s
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(f"# {s}", encoding="utf-8")

    import enforcement.dispatch_validator as dv
    monkeypatch.setattr(dv, "COMPANY_YAML", fake_company)
    monkeypatch.setattr(dv, "SKILLS_DIR", fake_skills)
    dv.clear_cache()
    yield fake_company
    dv.clear_cache()


class TestDispatchValidator:

    def test_valid_task_passes(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        result = validate_task({
            "id": "CUIDAI-001",
            "assignee": "worker-pitch",
            "execution_policy": "default",
        })
        assert result["valid"], f"Should pass: {result['errors']}"
        assert result["resolved_skill"] == "dario-pitch"

    def test_missing_id_rejected(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        result = validate_task({
            "assignee": "worker-pitch",
        })
        assert not result["valid"]
        assert any("id" in e.lower() for e in result["errors"])

    def test_missing_skill_and_assignee_rejected(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        result = validate_task({"id": "CUIDAI-001"})
        assert not result["valid"]

    def test_invalid_execution_policy_rejected(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        result = validate_task({
            "id": "X-001", "assignee": "worker-pitch",
            "execution_policy": "bogus",
        })
        assert not result["valid"]

    def test_unknown_assignee_rejected(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        result = validate_task({
            "id": "X-001", "assignee": "worker-nonexistent",
        })
        assert not result["valid"]
        assert any("not found" in e for e in result["errors"])

    def test_client_facing_resolves_to_polished(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        result = validate_task({
            "id": "ATRIUM-001", "assignee": "worker-pitch",
            "execution_policy": "client_facing",
        })
        assert result["valid"]
        assert result["resolved_skill"] == "dario-pitch-polished"

    def test_tier2_client_facing_requires_briefing(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        # worker-brand is Tier 2 (requires_briefing_validation=true)
        result = validate_task({
            "id": "X-001", "assignee": "worker-brand",
            "execution_policy": "client_facing",
            # no briefing
        })
        assert not result["valid"]
        assert any("briefing" in e.lower() for e in result["errors"])

    def test_tier2_with_briefing_passes(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        result = validate_task({
            "id": "X-001", "assignee": "worker-brand",
            "execution_policy": "client_facing",
            "briefing": "A" * 100,  # >=50 chars
        })
        assert result["valid"], result["errors"]

    def test_id_convention_warning_when_lax(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        # lowercase id violates convention
        result = validate_task({
            "id": "lowercase-001", "assignee": "worker-misc",
        }, strict_id=False)
        # Should pass with warning, not fail
        assert result["valid"]
        assert any("convention" in w.lower() for w in result["warnings"])

    def test_id_convention_error_when_strict(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        result = validate_task({
            "id": "lowercase-001", "assignee": "worker-misc",
        }, strict_id=True)
        assert not result["valid"]

    def test_validate_or_raise_passes(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task_or_raise
        skill = validate_task_or_raise({
            "id": "CUIDAI-001", "assignee": "worker-pitch",
        })
        assert skill == "dario-pitch"

    def test_validate_or_raise_raises_on_bad(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task_or_raise
        from enforcement import TaskValidationError
        with pytest.raises(TaskValidationError):
            validate_task_or_raise({"id": "X-001"})  # no assignee/skill

    def test_non_dict_input_rejected(self, isolated_validator):
        from enforcement.dispatch_validator import validate_task
        result = validate_task("not a dict")  # type: ignore
        assert not result["valid"]


# ─────────────────────────────────────────────────────────────────────
# Parallelism guard
# ─────────────────────────────────────────────────────────────────────

@pytest.fixture
def isolated_slots(tmp_path, monkeypatch):
    """Redirect slot files to tmp_path."""
    import enforcement.parallelism_guard as pg
    fake_runtime = tmp_path / "runtime"
    fake_runtime.mkdir()
    monkeypatch.setattr(pg, "RUNTIME_DIR", fake_runtime)
    monkeypatch.setattr(pg, "SLOTS_FILE", fake_runtime / "active_dispatches.json")
    monkeypatch.setattr(pg, "LOCK_FILE", fake_runtime / "active_dispatches.lock")
    yield fake_runtime
    pg.reset_for_test()


class TestParallelismGuard:

    def test_first_slot_claimable(self, isolated_slots):
        from enforcement.parallelism_guard import claim_slot, active_count
        slot_id = claim_slot(caller="test1", max_parallel=3)
        assert slot_id
        assert active_count() == 1

    def test_release_decrements(self, isolated_slots):
        from enforcement.parallelism_guard import (
            claim_slot, release_slot, active_count,
        )
        slot_id = claim_slot(caller="test", max_parallel=3)
        assert active_count() == 1
        assert release_slot(slot_id) is True
        assert active_count() == 0

    def test_exceed_max_raises(self, isolated_slots):
        from enforcement.parallelism_guard import claim_slot
        from enforcement import ParallelismExceededError
        claim_slot(caller="a", max_parallel=2)
        claim_slot(caller="b", max_parallel=2)
        with pytest.raises(ParallelismExceededError):
            claim_slot(caller="c", max_parallel=2)

    def test_release_unknown_slot_returns_false(self, isolated_slots):
        from enforcement.parallelism_guard import release_slot
        assert release_slot("nonexistent-id") is False

    def test_context_manager_auto_releases(self, isolated_slots):
        from enforcement.parallelism_guard import slot, active_count
        with slot(caller="ctx-test", max_parallel=3):
            assert active_count() == 1
        assert active_count() == 0

    def test_context_manager_releases_on_exception(self, isolated_slots):
        from enforcement.parallelism_guard import slot, active_count
        with pytest.raises(RuntimeError, match="forced"):
            with slot(caller="exc-test", max_parallel=3):
                assert active_count() == 1
                raise RuntimeError("forced")
        assert active_count() == 0  # slot released despite exception

    def test_stale_slots_reaped(self, isolated_slots, monkeypatch):
        """Slots older than SLOT_TIMEOUT_SECONDS get auto-reaped on next claim."""
        import enforcement.parallelism_guard as pg
        # Force a tiny timeout so we can test reaping
        monkeypatch.setattr(pg, "SLOT_TIMEOUT_SECONDS", 1)
        # Write a stale slot directly
        pg._ensure_files()
        stale_ts = (datetime.now(UTC) - timedelta(seconds=10)).isoformat(timespec="seconds")
        pg.SLOTS_FILE.write_text(json.dumps([
            {"id": "stale", "caller": "ghost", "claimed_at": stale_ts, "pid": 99999},
        ]), encoding="utf-8")
        # Stale slot should be reaped on next claim
        slot_id = pg.claim_slot(caller="fresh", max_parallel=1)
        slots = pg.active_slots()
        assert len(slots) == 1
        assert slots[0]["id"] == slot_id  # only fresh remains
        assert slots[0]["caller"] == "fresh"

    def test_empty_caller_rejected(self, isolated_slots):
        from enforcement.parallelism_guard import claim_slot
        with pytest.raises(ValueError):
            claim_slot(caller="")

    def test_concurrent_claims_via_threads(self, isolated_slots):
        """5 threads racing to claim slots when max=3 — exactly 3 succeed."""
        import threading
        from enforcement.parallelism_guard import claim_slot
        from enforcement import ParallelismExceededError

        successes: list[str] = []
        failures: list[Exception] = []
        lock = threading.Lock()

        def worker(i: int):
            try:
                sid = claim_slot(caller=f"thread-{i}", max_parallel=3)
                with lock:
                    successes.append(sid)
            except ParallelismExceededError as e:
                with lock:
                    failures.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(successes) == 3, f"Expected 3 successes, got {len(successes)}"
        assert len(failures) == 2, f"Expected 2 failures, got {len(failures)}"


# ─────────────────────────────────────────────────────────────────────
# Integration: all 3 guards composed (real dispatch pre-flight)
# ─────────────────────────────────────────────────────────────────────

class TestIntegratedDispatchPreflight:
    """The whole point of the layer: chain budget + validator + slot."""

    def test_full_preflight_success(self, isolated_budget, isolated_validator,
                                     isolated_slots):
        """Healthy budget + valid task + slot available → dispatch may proceed."""
        from enforcement.budget_gate import check_budget_or_raise
        from enforcement.dispatch_validator import validate_task_or_raise
        from enforcement.parallelism_guard import slot

        # 50% budget → safe
        (isolated_budget / "2099-08.yaml").write_text(
            yaml.safe_dump({"percentage": 50.0, "month": "2099-08"}),
            encoding="utf-8",
        )

        check_budget_or_raise(month="2099-08")  # no raise
        resolved = validate_task_or_raise({
            "id": "TEST-001", "assignee": "worker-pitch",
        })
        with slot(caller="integration-test", max_parallel=3):
            assert resolved == "dario-pitch"
            # Inside slot: dispatch would happen here

    def test_full_preflight_budget_blocks(self, isolated_budget,
                                           isolated_validator, isolated_slots):
        from enforcement.budget_gate import check_budget_or_raise
        from enforcement import BudgetExceededError

        (isolated_budget / "2099-09.yaml").write_text(
            yaml.safe_dump({"percentage": 98.0, "month": "2099-09"}),
            encoding="utf-8",
        )
        with pytest.raises(BudgetExceededError):
            check_budget_or_raise(month="2099-09")

    def test_full_preflight_validation_blocks(self, isolated_budget,
                                               isolated_validator, isolated_slots):
        from enforcement.dispatch_validator import validate_task_or_raise
        from enforcement import TaskValidationError
        with pytest.raises(TaskValidationError):
            validate_task_or_raise({"id": "X"})  # missing skill+assignee

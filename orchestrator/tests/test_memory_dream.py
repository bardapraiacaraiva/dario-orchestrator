"""Tests for the Memory & Dreaming subsystem.

Covers:
- Episode CRUD + idempotency guard
- Procedural workflow detection (trailing match, project filter, min length)
- Convergence detection + promotion (including the sort-order regression bug)
- Pattern detector (quality regression, tool failures, correction clusters)
- Dream engine 4-phase pipeline end-to-end
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


@pytest.fixture
def isolated_memory(tmp_path, monkeypatch):
    """Redirect all memory subsystem paths to a temp directory for the test."""
    fake_orch = tmp_path / "orchestrator"
    (fake_orch / "memory" / "episodes").mkdir(parents=True)
    (fake_orch / "memory" / "semantic").mkdir(parents=True)
    (fake_orch / "memory" / "procedural").mkdir(parents=True)
    (fake_orch / "memory" / "cache").mkdir(parents=True)
    (fake_orch / "memory" / "retrieval").mkdir(parents=True)
    (fake_orch / "dream" / "reports").mkdir(parents=True)
    (fake_orch / "tasks" / "done").mkdir(parents=True)

    import dream.engine as engine_mod
    import memory.cache as cache_mod
    import memory.episodic as ep_mod
    import memory.procedural as proc_mod
    import memory.retrieval as ret_mod
    import memory.semantic as sem_mod

    monkeypatch.setattr(ep_mod, "EPISODES_DIR", fake_orch / "memory" / "episodes")
    monkeypatch.setattr(ep_mod, "EP_COUNTER_FILE", fake_orch / "memory" / "episodes" / ".counter")
    monkeypatch.setattr(sem_mod, "SEMANTIC_DIR", fake_orch / "memory" / "semantic")
    monkeypatch.setattr(proc_mod, "PROCEDURAL_DIR", fake_orch / "memory" / "procedural")
    monkeypatch.setattr(cache_mod, "CACHE_DIR", fake_orch / "memory" / "cache")
    monkeypatch.setattr(ret_mod, "RETRIEVAL_DIR", fake_orch / "memory" / "retrieval")
    monkeypatch.setattr(ret_mod, "LOG_FILE", fake_orch / "memory" / "retrieval" / "retrieval_log.jsonl")
    monkeypatch.setattr(engine_mod, "REPORTS_DIR", fake_orch / "dream" / "reports")
    monkeypatch.setattr(engine_mod, "DREAMS_DIR", fake_orch / "memory" / "dreams")
    monkeypatch.setattr(engine_mod, "LEGACY_DREAMS_DIR", fake_orch / "agent-memory" / "dreams")

    yield fake_orch


def _make_episode(skill, score, project="testproj", days_ago=0, outcome="success", **kwargs):
    from memory.schemas import Episode, Outcome
    ts = (datetime.now(UTC) - timedelta(days=days_ago)).isoformat()
    return Episode(
        episode_id="",
        task_id=kwargs.pop("task_id", f"T-{skill}-{days_ago}-{score}"),
        timestamp=ts,
        agent="worker-test",
        skill=skill,
        outcome=Outcome(outcome),
        score=score,
        project=project,
        duration_seconds=kwargs.pop("duration_seconds", 100),
        tokens_used=kwargs.pop("tokens_used", 1000),
        model="opus",
        **kwargs,
    )


class TestEpisodicIdempotency:
    def test_episode_exists_for_task_returns_false_when_empty(self, isolated_memory):
        from memory import episodic
        assert episodic.episode_exists_for_task("CUI-001") is False

    def test_episode_exists_after_write(self, isolated_memory):
        from memory import episodic
        ep = _make_episode("dario-brand", 85, task_id="CUI-001")
        episodic.write_episode(ep)
        assert episodic.episode_exists_for_task("CUI-001") is True
        assert episodic.episode_exists_for_task("CUI-999") is False


class TestProceduralDetection:
    def test_detect_completed_with_trailing_match(self, isolated_memory):
        from memory import procedural
        from memory.schemas import ProceduralWorkflow

        procedural.write_workflow(ProceduralWorkflow(
            workflow_id="PROC-test_a_b",
            name="test",
            skills_sequence=["skill-a", "skill-b"],
            discovered_from="test",
        ))
        matches = procedural.detect_completed(["other", "skill-a", "skill-b"])
        assert any(m.workflow_id == "PROC-test_a_b" for m in matches)

    def test_detect_completed_rejects_non_trailing(self, isolated_memory):
        from memory import procedural
        from memory.schemas import ProceduralWorkflow

        procedural.write_workflow(ProceduralWorkflow(
            workflow_id="PROC-test_a_b",
            name="test",
            skills_sequence=["skill-a", "skill-b"],
            discovered_from="test",
        ))
        matches = procedural.detect_completed(["skill-a", "skill-b", "skill-c"])
        assert not any(m.workflow_id == "PROC-test_a_b" for m in matches)

    def test_detect_completed_filters_by_project_hint(self, isolated_memory):
        from memory import procedural
        from memory.schemas import ProceduralWorkflow

        procedural.write_workflow(ProceduralWorkflow(
            workflow_id="PROC-test_scoped",
            name="test",
            skills_sequence=["a", "b"],
            project_hints=["onlyproject"],
            discovered_from="test",
        ))
        assert not procedural.detect_completed(["a", "b"], project="other")
        assert procedural.detect_completed(["a", "b"], project="onlyproject")

    def test_detect_completed_skips_single_skill_workflows(self, isolated_memory):
        from memory import procedural
        from memory.schemas import ProceduralWorkflow

        procedural.write_workflow(ProceduralWorkflow(
            workflow_id="PROC-single",
            name="test",
            skills_sequence=["a"],
            discovered_from="test",
        ))
        assert procedural.detect_completed(["a"]) == []

    def test_record_usage_increments(self, isolated_memory):
        from memory import procedural
        from memory.schemas import ProceduralWorkflow

        procedural.write_workflow(ProceduralWorkflow(
            workflow_id="PROC-rec",
            name="test",
            skills_sequence=["a", "b"],
            discovered_from="test",
        ))
        procedural.record_usage("PROC-rec", success=True, score=85)
        procedural.record_usage("PROC-rec", success=True, score=95)

        wf = procedural.read_workflow("PROC-rec")
        assert wf.use_count == 2
        assert wf.avg_score == 90.0
        assert wf.success_rate == 1.0


class TestConvergencePromotion:
    """Regression tests for the sort-order bug found 2026-05-18.

    BUG: `promote_convergent` was iterating episodes in insertion order
    (counter-based), while `detect_convergence` sorted by timestamp.
    The disagreement caused promotion to fail to confirm sequences that
    detection had correctly identified.

    FIX: Both functions now `sorted(episodes, key=lambda e: e.timestamp)`.
    """

    def test_promote_with_out_of_order_episodes_regression(self, isolated_memory):
        """Episodes provided in REVERSED timestamp order must still promote."""
        from dream.convergence import promote_convergent
        from dream.pattern_detector import detect_convergence
        from memory import episodic, procedural

        # 3 sessions, each with [skill-a, skill-b] trailing, on different projects today
        # but episodes are written with INCREASING task_ids that don't match temporal order
        episodes = []
        for i, proj in enumerate(["proj-a", "proj-b", "proj-c"]):
            # Write in reverse chronological order intentionally
            ep1 = _make_episode("skill-a", 80, project=proj, task_id=f"REV-{i}-1")
            ep2 = _make_episode("skill-b", 90, project=proj, task_id=f"REV-{i}-2")
            # Pin to mid-day UTC: detect_convergence groups sessions by day
            # (timestamp[:10]), so now()+10min straddles the day boundary when
            # the suite runs 23:50-00:00 UTC and the pair lands in two sessions
            ep1.timestamp = datetime.now(UTC).replace(hour=12, minute=0, second=0, microsecond=0).isoformat()
            # Force ep2 to have LATER timestamp than ep1
            ep2.timestamp = (datetime.fromisoformat(ep1.timestamp) + timedelta(minutes=10)).isoformat()
            episodic.write_episode(ep2)  # later timestamp written FIRST
            episodic.write_episode(ep1)  # earlier timestamp written SECOND
            episodes.extend([ep2, ep1])  # also pass in reverse order to functions

        candidates = detect_convergence(episodes)
        assert any(c["sequence"] == ["skill-a", "skill-b"] for c in candidates), \
            "detect_convergence should find skill-a -> skill-b in 3 sessions"

        promoted = promote_convergent(episodes, candidates, dry_run=False)
        assert promoted, f"promote_convergent must return at least one promoted workflow_id, got: {promoted}"

        # Verify workflow was actually created on disk
        wfs = procedural.list_workflows()
        conv = [w for w in wfs if w.discovered_from == "convergence"]
        assert conv, "At least one convergent workflow must exist"
        assert any(w.skills_sequence == ["skill-a", "skill-b"] for w in conv)
        assert all(w.sessions_observed >= 3 for w in conv)

    def test_promote_respects_min_sessions(self, isolated_memory):
        from dream.convergence import promote_convergent
        from memory import episodic

        # Only 1 session — should NOT promote (MIN_SESSIONS=2, DD finding A13)
        episodes = []
        for proj in ["a"]:
            for skill, score in [("x", 85), ("y", 90)]:
                ep = _make_episode(skill, score, project=proj)
                episodic.write_episode(ep)
                episodes.append(ep)

        candidates = [{"sequence": ["x", "y"], "session_count": 1, "projects": ["a"]}]
        promoted = promote_convergent(episodes, candidates, dry_run=False)
        assert promoted == []

    def test_promote_respects_min_score(self, isolated_memory):
        from dream.convergence import promote_convergent
        from memory import episodic

        # 3 sessions but all low scores (<70) — should NOT promote
        episodes = []
        for proj in ["a", "b", "c"]:
            for skill, score in [("x", 50), ("y", 55)]:
                ep = _make_episode(skill, score, project=proj)
                episodic.write_episode(ep)
                episodes.append(ep)

        candidates = [{"sequence": ["x", "y"], "session_count": 3, "projects": ["a", "b", "c"]}]
        promoted = promote_convergent(episodes, candidates, dry_run=False)
        assert promoted == []


class TestPatternDetector:
    def test_quality_regression_detected(self):
        from dream.pattern_detector import detect_patterns

        # Skill with 6 runs: first 3 high, last 3 low → regression
        eps = []
        for score in [95, 92, 90, 75, 72, 70]:
            eps.append(_make_episode("regressing-skill", score))

        patterns = detect_patterns(eps)
        assert any("regression" in p.lower() for p in patterns), \
            f"Expected regression pattern, got: {patterns}"

    def test_tool_failures_clustered(self):
        from dream.pattern_detector import detect_patterns
        from memory.schemas import FailedToolCall

        eps = []
        for _ in range(4):
            ep = _make_episode("any-skill", 80)
            ep.failed_tool_calls = [FailedToolCall(tool="FlakyTool", error="timeout")]
            eps.append(ep)

        patterns = detect_patterns(eps)
        assert any("FlakyTool" in p for p in patterns), \
            f"Expected FlakyTool in patterns, got: {patterns}"


class TestDreamEngineEndToEnd:
    def test_dream_runs_without_errors_on_empty_state(self, isolated_memory):
        from dream.engine import run_dream
        report = run_dream(window_days=7, dry_run=False)
        assert report.episodes_processed == 0
        assert report.phase_1_orient is not None
        assert report.phase_2_prune is not None
        assert report.phase_3_merge is not None
        assert report.phase_4_reorganize is not None

    def test_dream_promotes_workflow_when_convergent(self, isolated_memory):
        from dream.engine import run_dream
        from memory import episodic

        # Seed 3 sessions with [a, b] sequence
        for i, proj in enumerate(["x", "y", "z"]):
            for skill, score in [("alpha", 85), ("beta", 90)]:
                ep = _make_episode(skill, score, project=proj, days_ago=0,
                                    task_id=f"SEED-{i}-{skill}")
                episodic.write_episode(ep)

        report = run_dream(window_days=7, dry_run=False)
        assert report.episodes_processed == 6
        assert len(report.convergent_workflows) >= 1

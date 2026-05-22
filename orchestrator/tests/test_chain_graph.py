"""Tests for Onda 1 #3 — chain_graph.py LangGraph-native execution."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import chain_graph as cg

# ─── Test executors ──────────────────────────────────────────────────────────


def _make_executor(scores_by_skill: dict[str, int] | None = None):
    """Deterministic executor: each skill returns a fake artifact with a score."""
    scores = scores_by_skill or {}

    def executor(skill: str, step_def: dict, state: cg.ChainState) -> dict:
        return {
            "_score": scores.get(skill, 80),
            "output": f"{skill}-output",
            "saw_artifacts": list(state.get("artifacts", {}).keys()),
        }

    return executor


@pytest.fixture
def tmp_checkpoint_db():
    """Per-test SQLite DB for the checkpointer."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp) / "chain_graph.db"


# ─── Linear chain ────────────────────────────────────────────────────────────


class TestLinearChain:
    def test_three_step_linear(self, tmp_checkpoint_db):
        chain_def = {
            "steps": [
                {"skill": "step-a", "order": 1},
                {"skill": "step-b", "order": 2},
                {"skill": "step-c", "order": 3},
            ]
        }
        graph = cg.ChainGraph(
            chain_name="linear",
            chain_def=chain_def,
            executor=_make_executor(),
            checkpoint_db=tmp_checkpoint_db,
        )
        result = graph.invoke(project="test", context="ctx", thread_id="t1")
        assert result["status"] == "completed"
        assert result["current_step"] == 3
        assert set(result["artifacts"].keys()) == {"step-a", "step-b", "step-c"}
        assert len(result["step_scores"]) == 3

    def test_later_step_sees_earlier_artifacts(self, tmp_checkpoint_db):
        chain_def = {
            "steps": [
                {"skill": "first", "order": 1},
                {"skill": "second", "order": 2},
            ]
        }
        graph = cg.ChainGraph(
            chain_name="seq",
            chain_def=chain_def,
            executor=_make_executor(),
            checkpoint_db=tmp_checkpoint_db,
        )
        result = graph.invoke(project="t", context="c", thread_id="t2")
        second_artifact = result["artifacts"]["second"]
        assert "first" in second_artifact["saw_artifacts"]


# ─── Parallel fan-out ────────────────────────────────────────────────────────


class TestParallelChain:
    def test_two_parallel_branches_merge(self, tmp_checkpoint_db):
        chain_def = {
            "steps": [
                {"skill": "start", "order": 1},
                {"skill": "branch-a", "order": 2},
                {"skill": "branch-b", "order": 2},  # same order → parallel
                {"skill": "join", "order": 3},
            ]
        }
        graph = cg.ChainGraph(
            chain_name="parallel",
            chain_def=chain_def,
            executor=_make_executor(),
            checkpoint_db=tmp_checkpoint_db,
        )
        result = graph.invoke(project="p", context="c", thread_id="t3")
        # Both branches must have produced artifacts (reducer merges them)
        assert "branch-a" in result["artifacts"]
        assert "branch-b" in result["artifacts"]
        # Join step sees both upstream artifacts
        join_art = result["artifacts"]["join"]
        assert "branch-a" in join_art["saw_artifacts"]
        assert "branch-b" in join_art["saw_artifacts"]


# ─── Durable checkpointing ───────────────────────────────────────────────────


class TestCheckpointing:
    def test_checkpoint_persists_across_instances(self, tmp_checkpoint_db):
        chain_def = {
            "steps": [
                {"skill": "alpha", "order": 1},
                {"skill": "beta", "order": 2},
            ]
        }
        # First run completes
        g1 = cg.ChainGraph(
            chain_name="resume_demo",
            chain_def=chain_def,
            executor=_make_executor(),
            checkpoint_db=tmp_checkpoint_db,
        )
        g1.invoke(project="p", context="c", thread_id="resume_thread")

        # New instance reads the same checkpoint DB → state is still there
        g2 = cg.ChainGraph(
            chain_name="resume_demo",
            chain_def=chain_def,
            executor=_make_executor(),
            checkpoint_db=tmp_checkpoint_db,
        )
        state = g2.get_state("resume_thread")
        assert state is not None
        assert "alpha" in state.get("artifacts", {})
        assert "beta" in state.get("artifacts", {})

    def test_list_threads(self, tmp_checkpoint_db):
        chain_def = {"steps": [{"skill": "x", "order": 1}]}
        graph = cg.ChainGraph(
            chain_name="thread_list",
            chain_def=chain_def,
            executor=_make_executor(),
            checkpoint_db=tmp_checkpoint_db,
        )
        graph.invoke(project="p", context="c", thread_id="thread_alpha")
        graph.invoke(project="p", context="c", thread_id="thread_beta")
        threads = graph.list_threads()
        assert "thread_alpha" in threads
        assert "thread_beta" in threads


# ─── Edge cases ──────────────────────────────────────────────────────────────


class TestEdgeCases:
    def test_empty_chain_rejected(self, tmp_checkpoint_db):
        with pytest.raises(ValueError):
            cg.ChainGraph(
                chain_name="empty",
                chain_def={"steps": []},
                executor=_make_executor(),
                checkpoint_db=tmp_checkpoint_db,
            )

    def test_single_step(self, tmp_checkpoint_db):
        chain_def = {"steps": [{"skill": "only", "order": 1}]}
        graph = cg.ChainGraph(
            chain_name="single",
            chain_def=chain_def,
            executor=_make_executor({"only": 95}),
            checkpoint_db=tmp_checkpoint_db,
        )
        result = graph.invoke(project="p", context="c", thread_id="solo")
        assert result["artifacts"]["only"]["_score"] == 95
        assert len(result["step_scores"]) == 1

    def test_executor_can_inspect_state(self, tmp_checkpoint_db):
        """Executor receives the live state — needed for context injection."""
        seen_context = {}

        def inspecting_executor(skill, step_def, state):
            seen_context[skill] = state["initial_context"]
            return {"_score": 80, "output": "ok"}

        chain_def = {"steps": [{"skill": "s1", "order": 1}, {"skill": "s2", "order": 2}]}
        graph = cg.ChainGraph(
            chain_name="ctx",
            chain_def=chain_def,
            executor=inspecting_executor,
            checkpoint_db=tmp_checkpoint_db,
        )
        graph.invoke(project="p", context="HELLO_CONTEXT", thread_id="ctx_thread")
        assert seen_context["s1"] == "HELLO_CONTEXT"
        assert seen_context["s2"] == "HELLO_CONTEXT"

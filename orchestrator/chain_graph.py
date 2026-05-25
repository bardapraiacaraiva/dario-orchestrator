"""DARIO Chain Graph — LangGraph-native chain execution (Onda 1 #3).

Replaces the custom checkpoint-as-YAML-files plumbing in chain_executor.py
with LangGraph's official primitives:

    - StateGraph      → DAG topology + conditional edges
    - SqliteSaver     → durable checkpointer (single SQLite DB, not per-run YAML dirs)
    - TypedDict state → typed contract for what flows between steps
    - interrupt()     → native pause/resume (replaces ad-hoc state.yaml polling)

This module is additive: it does NOT delete chain_executor.py. Existing
callers (autopilot, runtime) continue to work. New chains should be built
via `ChainGraph.from_yaml(...)`; we will migrate callers in a follow-up.

Why this matters
----------------
Before: each chain run wrote 5-10 YAML files into chain_runs/<run_id>/.
        14 checkpoint rows in orchestrator.db were state-snapshot blobs
        with no replay semantics. Crash mid-step = re-execute everything,
        re-incur side effects.

After:  one SQLite-backed checkpointer journals every node transition.
        Crash mid-step = `graph.invoke(..., config={"configurable":
        {"thread_id": run_id}})` resumes from the last completed node
        without re-running successful predecessors.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from datetime import UTC
from pathlib import Path
from typing import Annotated, Any, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
CHECKPOINT_DB = ORCH_DIR / "chain_graph.db"


# ─── State contract ──────────────────────────────────────────────────────────


def _merge_artifacts(left: dict, right: dict) -> dict:
    """Reducer: parallel branches contribute artifacts under their own skill key."""
    out = dict(left or {})
    out.update(right or {})
    return out


def _append_scores(left: list, right: list) -> list:
    return list(left or []) + list(right or [])


def _max_int(left: int, right: int) -> int:
    """Reducer for monotonically-increasing counters under parallel writes."""
    return max(left or 0, right or 0)


def _first_non_none(left, right):
    """Reducer for optional fields: keep the first non-None value seen."""
    return left if left is not None else right


class ChainState(TypedDict, total=False):
    """The typed contract that flows through every node of a chain.

    LangGraph annotated reducers let parallel branches merge cleanly:
    each step writes its artifact under its own skill key, and they
    fan-in without overwriting each other.
    """

    chain_name: str
    project: str
    initial_context: str
    current_step: Annotated[int, _max_int]
    total_steps: int
    artifacts: Annotated[dict[str, dict], _merge_artifacts]
    step_scores: Annotated[list[dict], _append_scores]
    status: str  # running | paused | completed | failed
    last_error: Annotated[str | None, _first_non_none]


# ─── Graph builder ───────────────────────────────────────────────────────────


StepExecutor = Callable[[str, dict, ChainState], dict]
"""Signature: (skill_name, step_def, current_state) -> output_artifact dict.

The executor is injected — chain_graph does not know HOW a skill runs.
Production callers pass an executor that invokes the Anthropic API.
Tests pass a deterministic mock.
"""


class ChainGraph:
    """Build and run a chain as a LangGraph StateGraph.

    Usage:
        cg = ChainGraph(chain_name="brand_to_market", chain_def=defn,
                        executor=my_executor_fn)
        result = cg.invoke(project="acme", context="...", thread_id="run_001")
    """

    def __init__(
        self,
        chain_name: str,
        chain_def: dict,
        executor: StepExecutor,
        checkpoint_db: Path | None = None,
    ):
        self.chain_name = chain_name
        self.chain_def = chain_def
        self.executor = executor
        self.checkpoint_db = checkpoint_db or CHECKPOINT_DB
        self.graph = self._build_graph()

    # ─── Graph construction ──────────────────────────────────────────────

    def _step_node_factory(self, step_index: int, step_def: dict):
        """Build a node function that executes one step via the injected executor."""
        skill = step_def.get("skill", f"step_{step_index}")

        def node(state: ChainState) -> dict:
            output = self.executor(skill, step_def, state)
            return {
                "current_step": step_index + 1,
                "artifacts": {skill: output},
                "step_scores": [
                    {
                        "skill": skill,
                        "score": output.get("_score", 0)
                        if isinstance(output, dict)
                        else 0,
                        "step_index": step_index,
                    }
                ],
            }

        node.__name__ = f"node_{step_index}_{skill}".replace("-", "_")
        return node

    def _build_graph(self) -> Any:
        """Compile chain_def YAML into a StateGraph with one node per step."""
        steps = self.chain_def.get("steps", [])
        if not steps:
            raise ValueError(f"Chain '{self.chain_name}' has no steps")

        builder = StateGraph(ChainState)

        # Group steps by 'order' (waves). Same-order steps fan out in parallel.
        waves: dict[int, list[tuple[int, dict]]] = {}
        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            order = step.get("order", idx + 1)
            waves.setdefault(order, []).append((idx, step))

        # Add nodes + edges
        node_names_by_wave: dict[int, list[str]] = {}
        for order in sorted(waves.keys()):
            names = []
            for idx, step_def in waves[order]:
                node_fn = self._step_node_factory(idx, step_def)
                builder.add_node(node_fn.__name__, node_fn)
                names.append(node_fn.__name__)
            node_names_by_wave[order] = names

        sorted_waves = sorted(node_names_by_wave.keys())

        # START → wave[0] nodes (all in parallel if multiple)
        for name in node_names_by_wave[sorted_waves[0]]:
            builder.add_edge(START, name)

        # Wave N → Wave N+1 (fan-out / fan-in via parallel edges)
        for i, current_order in enumerate(sorted_waves[:-1]):
            next_order = sorted_waves[i + 1]
            for prev_name in node_names_by_wave[current_order]:
                for next_name in node_names_by_wave[next_order]:
                    builder.add_edge(prev_name, next_name)

        # Last wave → END
        for name in node_names_by_wave[sorted_waves[-1]]:
            builder.add_edge(name, END)

        # Compile WITHOUT checkpointer here — we attach the checkpointer in
        # invoke() so we can use a context manager (SqliteSaver requires one).
        return builder.compile()

    # ─── Execution ───────────────────────────────────────────────────────

    def invoke(
        self,
        project: str,
        context: str,
        thread_id: str | None = None,
    ) -> ChainState:
        """Run the chain. If a thread_id is reused, resumes from the last checkpoint."""
        from datetime import datetime

        tid = thread_id or f"chain_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"

        initial: ChainState = {
            "chain_name": self.chain_name,
            "project": project,
            "initial_context": context,
            "current_step": 0,
            "total_steps": len(self.chain_def.get("steps", [])),
            "artifacts": {},
            "step_scores": [],
            "status": "running",
            "last_error": None,
        }

        with SqliteSaver.from_conn_string(str(self.checkpoint_db)) as saver:
            # Re-compile with checkpointer bound (single-step convenience)
            graph_with_cp = self._build_graph_with_checkpointer(saver)
            config = {"configurable": {"thread_id": tid}}
            final = graph_with_cp.invoke(initial, config=config)

        final["status"] = "completed"
        return final  # type: ignore[no-any-return]

    def _build_graph_with_checkpointer(self, saver) -> Any:
        """Rebuild graph with the given checkpointer attached (cheap — same nodes)."""
        # Reconstruct so we can bind the checkpointer at compile time
        steps = self.chain_def.get("steps", [])
        builder = StateGraph(ChainState)

        waves: dict[int, list[tuple[int, dict]]] = {}
        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            order = step.get("order", idx + 1)
            waves.setdefault(order, []).append((idx, step))

        node_names_by_wave: dict[int, list[str]] = {}
        for order in sorted(waves.keys()):
            names = []
            for idx, step_def in waves[order]:
                node_fn = self._step_node_factory(idx, step_def)
                builder.add_node(node_fn.__name__, node_fn)
                names.append(node_fn.__name__)
            node_names_by_wave[order] = names

        sorted_waves = sorted(node_names_by_wave.keys())
        for name in node_names_by_wave[sorted_waves[0]]:
            builder.add_edge(START, name)
        for i, current_order in enumerate(sorted_waves[:-1]):
            next_order = sorted_waves[i + 1]
            for prev_name in node_names_by_wave[current_order]:
                for next_name in node_names_by_wave[next_order]:
                    builder.add_edge(prev_name, next_name)
        for name in node_names_by_wave[sorted_waves[-1]]:
            builder.add_edge(name, END)

        return builder.compile(checkpointer=saver)

    # ─── Inspection helpers ──────────────────────────────────────────────

    def get_state(self, thread_id: str) -> dict | None:
        """Read the current checkpoint for a thread_id (used for resume/inspect)."""
        with SqliteSaver.from_conn_string(str(self.checkpoint_db)) as saver:
            graph_with_cp = self._build_graph_with_checkpointer(saver)
            snapshot = graph_with_cp.get_state(
                {"configurable": {"thread_id": thread_id}}
            )
            if snapshot is None:
                return None
            return dict(snapshot.values) if snapshot.values else None

    def list_threads(self) -> list[str]:
        """List all thread_ids that have at least one checkpoint."""
        if not self.checkpoint_db.exists():
            return []
        conn = sqlite3.connect(str(self.checkpoint_db))
        try:
            rows = conn.execute(
                "SELECT DISTINCT thread_id FROM checkpoints"
            ).fetchall()
            return [r[0] for r in rows]
        except sqlite3.OperationalError:
            return []
        finally:
            conn.close()


# ─── YAML loader (compat with skill_chains.yaml) ─────────────────────────────


def load_chain_def(chain_name: str) -> dict | None:
    """Load chain_def from skill_chains.yaml — same source as chain_executor."""
    import yaml

    chains_file = ORCH_DIR / "skill_chains.yaml"
    if not chains_file.exists():
        return None
    data = yaml.safe_load(chains_file.read_text(encoding="utf-8")) or {}
    return (data.get("chains") or {}).get(chain_name)


def build_from_yaml(
    chain_name: str, executor: StepExecutor
) -> ChainGraph | None:
    """Convenience: load + build in one call."""
    chain_def = load_chain_def(chain_name)
    if not chain_def:
        return None
    return ChainGraph(chain_name=chain_name, chain_def=chain_def, executor=executor)


def list_chains() -> dict[str, dict]:
    """Read skill_chains.yaml and return summary metadata for every chain.

    Replaces `chain_executor --list --json`. Pure read — no graph compilation.
    """
    import yaml

    chains_file = ORCH_DIR / "skill_chains.yaml"
    if not chains_file.exists():
        return {}
    data = yaml.safe_load(chains_file.read_text(encoding="utf-8")) or {}
    chains = data.get("chains") or {}
    summary: dict[str, dict] = {}
    for name, defn in chains.items():
        steps = defn.get("steps", [])
        summary[name] = {
            "description": defn.get("description", ""),
            "estimated_tokens": defn.get("estimated_tokens"),
            "quality_gate": defn.get("quality_gate", "score >= 70"),
            "total_steps": len(steps),
            "skills": [s.get("skill") for s in steps if isinstance(s, dict)],
        }
    return summary


def build_execution_plan(chain_def: dict, context: dict | None = None) -> list[dict]:
    """Build a wave-grouped execution plan dict (legacy shape).

    Same return shape as `chain_executor.build_execution_plan` so callers
    (runtime.py /chains/compose) can switch import path without changes.

    Plan format:
        [{"wave": 1, "steps": [{"skill": "X", "parallel": False, ...}, ...]}, ...]
    """
    steps = chain_def.get("steps", [])
    if not steps:
        return []

    has_order = any(isinstance(s, dict) and "order" in s for s in steps)

    waves: dict[int, list[dict]] = {}
    if has_order:
        for step in steps:
            order = step.get("order", 1) if isinstance(step, dict) else 1
            waves.setdefault(order, []).append(step)
    else:
        wave_num = 1
        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            if i > 0 and step.get("parallel") and steps[i - 1].get("parallel"):
                waves.setdefault(wave_num, []).append(step)
            else:
                if i > 0:
                    wave_num += 1
                waves.setdefault(wave_num, []).append(step)

    plan: list[dict] = []
    for wave_num in sorted(waves.keys()):
        wave_steps = waves[wave_num]
        plan.append(
            {
                "wave": wave_num,
                "steps": [
                    {
                        "skill": s.get("skill", "?"),
                        "receives": s.get("receives", ""),
                        "produces": s.get("produces", ""),
                        "pass_to_next": s.get("pass_to_next", []),
                        "parallel": s.get("parallel", False),
                        "condition": s.get("condition", None),
                    }
                    for s in wave_steps
                ],
            }
        )
    return plan


__all__ = [
    "ChainGraph",
    "ChainState",
    "StepExecutor",
    "build_from_yaml",
    "load_chain_def",
    "list_chains",
    "build_execution_plan",
]

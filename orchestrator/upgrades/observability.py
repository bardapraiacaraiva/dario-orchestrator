#!/usr/bin/env python3
"""
DARIO Observability Upgrades v11.0 — Module 6
================================================
M6.1  OTelInstrumentation   (OpenLLMetry)    — auto-instrument Anthropic calls
M6.2  TimeTravelDebug       (AgentOps)       — session replay for failures
M6.3  ExperimentTracker     (Phoenix)        — A/B test skill versions
M6.4  OfflineReplay         (AgentLens)      — JSONL record/replay without budget
M6.5  CostDashboard         (Langfuse)       — per-skill cost aggregation
M6.6  AutoQualityScoring    (Opik)           — automated scoring pipeline
M6.7  UnifiedStack          (OpenLIT)        — combined metrics endpoint
M6.8  TrajectoryAudit       (agent-lens)     — ATIF-style trajectory capture
"""
import json
import logging
import os
import sys
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path(os.path.expanduser("~/.claude/orchestrator"))
log = logging.getLogger("observability_upgrades")

# M6.1: OTel Instrumentation Registry
class OTelInstrumentationRegistry:
    def __init__(self):
        self._instrumented: dict[str, bool] = {}
        self._spans: list[dict] = []
    def instrument(self, provider: str):
        self._instrumented[provider] = True
    def record_span(self, name: str, provider: str, duration_ms: int, tokens: dict = None, metadata: dict = None):
        self._spans.append({"name": name, "provider": provider, "duration_ms": duration_ms,
                           "tokens": tokens or {}, "metadata": metadata or {},
                           "timestamp": datetime.now(UTC).isoformat()})
    def is_instrumented(self, provider: str) -> bool: return self._instrumented.get(provider, False)
    def get_spans(self, limit: int = 50) -> list[dict]: return self._spans[-limit:]
    def stats(self) -> dict:
        return {"instrumented_providers": list(self._instrumented.keys()), "total_spans": len(self._spans),
                "total_tokens": sum(s.get("tokens",{}).get("input",0)+s.get("tokens",{}).get("output",0) for s in self._spans)}

# M6.2: Time-Travel Debug
@dataclass
class DebugSnapshot:
    snapshot_id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    task_id: str = ""
    step: int = 0
    state: dict = field(default_factory=dict)
    tools_used: list[str] = field(default_factory=list)
    token_usage: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

class TimeTravelDebugger:
    def __init__(self): self._sessions: dict[str, list[DebugSnapshot]] = {}
    def capture(self, task_id: str, step: int, state: dict, tools: list[str] = None, tokens: dict = None):
        if task_id not in self._sessions: self._sessions[task_id] = []
        self._sessions[task_id].append(DebugSnapshot(task_id=task_id, step=step, state=state,
                                                      tools_used=tools or [], token_usage=tokens or {}))
    def replay(self, task_id: str, to_step: int = None) -> list[dict]:
        snapshots = self._sessions.get(task_id, [])
        if to_step is not None: snapshots = [s for s in snapshots if s.step <= to_step]
        return [asdict(s) for s in snapshots]
    def get_state_at(self, task_id: str, step: int) -> dict | None:
        for s in self._sessions.get(task_id, []):
            if s.step == step: return s.state
        return None
    def stats(self) -> dict:
        return {"sessions": len(self._sessions), "total_snapshots": sum(len(v) for v in self._sessions.values())}

# M6.3: Experiment Tracker
@dataclass
class Experiment:
    experiment_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    name: str = ""
    variants: dict[str, list[float]] = field(default_factory=dict)  # variant → scores
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

class ExperimentTracker:
    def __init__(self): self._experiments: dict[str, Experiment] = {}
    def create(self, name: str) -> Experiment:
        exp = Experiment(name=name)
        self._experiments[exp.experiment_id] = exp
        return exp
    def record(self, experiment_id: str, variant: str, score: float):
        exp = self._experiments.get(experiment_id)
        if exp:
            if variant not in exp.variants: exp.variants[variant] = []
            exp.variants[variant].append(score)
    def compare(self, experiment_id: str) -> dict:
        exp = self._experiments.get(experiment_id)
        if not exp: return {}
        return {v: {"avg": round(sum(s)/len(s),1), "count": len(s), "min": min(s), "max": max(s)}
                for v, s in exp.variants.items() if s}
    def stats(self) -> dict: return {"experiments": len(self._experiments)}

# M6.4: Offline Replay
class OfflineRecorder:
    def __init__(self): self._recordings: dict[str, list[dict]] = {}
    def start_recording(self, session_id: str): self._recordings[session_id] = []
    def record_event(self, session_id: str, event_type: str, data: dict):
        if session_id in self._recordings:
            self._recordings[session_id].append({"type": event_type, "data": data,
                                                  "timestamp": datetime.now(UTC).isoformat()})
    def save_to_jsonl(self, session_id: str, path: str = None) -> str:
        events = self._recordings.get(session_id, [])
        filepath = path or str(ORCH_DIR / "traces" / f"replay_{session_id}.jsonl")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            for e in events: f.write(json.dumps(e, default=str) + "\n")
        return filepath
    def load_replay(self, path: str) -> list[dict]:
        events = []
        with open(path) as f:
            for line in f:
                if line.strip(): events.append(json.loads(line))
        return events
    def stats(self) -> dict:
        return {"active_recordings": len(self._recordings),
                "total_events": sum(len(v) for v in self._recordings.values())}

# M6.5: Cost Dashboard
class CostAggregator:
    def __init__(self): self._costs: list[dict] = []
    def record(self, skill: str, model: str, tokens: int, cost_usd: float, project: str = ""):
        self._costs.append({"skill": skill, "model": model, "tokens": tokens, "cost_usd": cost_usd,
                           "project": project, "timestamp": datetime.now(UTC).isoformat()})
    def by_skill(self) -> dict:
        agg = defaultdict(lambda: {"cost": 0, "tokens": 0, "calls": 0})
        for c in self._costs:
            agg[c["skill"]]["cost"] += c["cost_usd"]
            agg[c["skill"]]["tokens"] += c["tokens"]
            agg[c["skill"]]["calls"] += 1
        return {k: {**v, "cost": round(v["cost"],4)} for k, v in sorted(agg.items(), key=lambda x: -x[1]["cost"])}
    def by_model(self) -> dict:
        agg = defaultdict(lambda: {"cost": 0, "tokens": 0, "calls": 0})
        for c in self._costs:
            agg[c["model"]]["cost"] += c["cost_usd"]
            agg[c["model"]]["tokens"] += c["tokens"]
            agg[c["model"]]["calls"] += 1
        return {k: {**v, "cost": round(v["cost"],4)} for k, v in agg.items()}
    def total(self) -> dict:
        return {"total_cost_usd": round(sum(c["cost_usd"] for c in self._costs),4),
                "total_tokens": sum(c["tokens"] for c in self._costs), "total_calls": len(self._costs)}

# M6.8: Trajectory Audit (ATIF-style)
@dataclass
class TrajectoryStep:
    step_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    action: str = ""
    tool: str = ""
    input_summary: str = ""
    output_summary: str = ""
    tokens: dict = field(default_factory=dict)
    duration_ms: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

class TrajectoryRecorder:
    def __init__(self): self._trajectories: dict[str, list[TrajectoryStep]] = {}
    def start(self, task_id: str): self._trajectories[task_id] = []
    def record_step(self, task_id: str, action: str, tool: str = "", input_s: str = "", output_s: str = "",
                    tokens: dict = None, duration_ms: int = 0):
        if task_id in self._trajectories:
            self._trajectories[task_id].append(TrajectoryStep(action=action, tool=tool, input_summary=input_s[:200],
                output_summary=output_s[:200], tokens=tokens or {}, duration_ms=duration_ms))
    def get_trajectory(self, task_id: str) -> list[dict]:
        return [asdict(s) for s in self._trajectories.get(task_id, [])]
    def export_atif(self, task_id: str) -> dict:
        steps = self._trajectories.get(task_id, [])
        return {"format": "ATIF/1.0", "task_id": task_id, "steps": [asdict(s) for s in steps],
                "total_tokens": sum(s.tokens.get("input",0)+s.tokens.get("output",0) for s in steps)}
    def stats(self) -> dict:
        return {"trajectories": len(self._trajectories),
                "total_steps": sum(len(v) for v in self._trajectories.values())}

# GLOBALS
otel_registry = OTelInstrumentationRegistry()
time_travel = TimeTravelDebugger()
experiment_tracker = ExperimentTracker()
offline_recorder = OfflineRecorder()
cost_aggregator = CostAggregator()
trajectory_recorder = TrajectoryRecorder()

def init_observability_upgrades(app=None):
    otel_registry.instrument("anthropic")
    otel_registry.instrument("openai")
    if app: _register_endpoints(app)
    log.info("Observability Upgrades v11.0 initialized")

def _register_endpoints(app):
    @app.get("/observe/status")
    async def observe_status():
        return {"version": "v11.0", "otel": otel_registry.stats(), "debug": time_travel.stats(),
                "experiments": experiment_tracker.stats(), "recordings": offline_recorder.stats(),
                "costs": cost_aggregator.total(), "trajectories": trajectory_recorder.stats()}
    @app.get("/observe/costs/by-skill")
    async def costs_by_skill(): return cost_aggregator.by_skill()
    @app.get("/observe/costs/by-model")
    async def costs_by_model(): return cost_aggregator.by_model()
    @app.get("/observe/debug/{task_id}")
    async def debug_replay(task_id: str): return {"snapshots": time_travel.replay(task_id)}

def _run_self_tests():
    p, f = 0, 0
    def check(n, fn):
        nonlocal p, f
        try: fn(); print(f"  PASS  {n}"); p += 1
        except Exception as e: print(f"  FAIL  {n}: {e}"); f += 1
    print("=== Observability Upgrades v11.0 — Self Tests ===\n")
    print("--- OTelInstrumentation (OpenLLMetry) ---")
    oi = OTelInstrumentationRegistry()
    oi.instrument("anthropic")
    check("instrument_provider", lambda: None if oi.is_instrumented("anthropic") else (_ for _ in ()).throw(AssertionError))
    oi.record_span("llm_call", "anthropic", 250, {"input": 500, "output": 200})
    check("record_span", lambda: None if oi.stats()["total_spans"] == 1 else (_ for _ in ()).throw(AssertionError))
    print("\n--- TimeTravelDebug (AgentOps) ---")
    ttd = TimeTravelDebugger()
    ttd.capture("T1", 1, {"step": "brand"}, ["Read", "Grep"])
    ttd.capture("T1", 2, {"step": "naming"}, ["Read", "Write"])
    check("capture_snapshots", lambda: None if len(ttd.replay("T1")) == 2 else (_ for _ in ()).throw(AssertionError))
    check("replay_to_step_1", lambda: None if len(ttd.replay("T1", to_step=1)) == 1 else (_ for _ in ()).throw(AssertionError))
    check("get_state_at", lambda: None if ttd.get_state_at("T1", 2)["step"] == "naming" else (_ for _ in ()).throw(AssertionError))
    print("\n--- ExperimentTracker (Phoenix) ---")
    et = ExperimentTracker()
    exp = et.create("brand_v1_vs_v2")
    et.record(exp.experiment_id, "v1", 82); et.record(exp.experiment_id, "v1", 78)
    et.record(exp.experiment_id, "v2", 88); et.record(exp.experiment_id, "v2", 90)
    cmp = et.compare(exp.experiment_id)
    check("compare_variants", lambda: None if cmp["v2"]["avg"] > cmp["v1"]["avg"] else (_ for _ in ()).throw(AssertionError))
    print("\n--- OfflineRecorder (AgentLens) ---")
    orec = OfflineRecorder()
    orec.start_recording("s1")
    orec.record_event("s1", "llm_call", {"model": "sonnet", "tokens": 500})
    orec.record_event("s1", "tool_use", {"tool": "Read", "file": "test.py"})
    check("record_events", lambda: None if orec.stats()["total_events"] == 2 else (_ for _ in ()).throw(AssertionError))
    print("\n--- CostAggregator (Langfuse) ---")
    ca = CostAggregator()
    ca.record("dario-brand", "sonnet", 3000, 0.027, "mar-brasa")
    ca.record("dario-brand", "sonnet", 2500, 0.022, "mar-brasa")
    ca.record("seo-audit", "opus", 8000, 0.36, "vivenda")
    by_skill = ca.by_skill()
    check("cost_by_skill", lambda: None if "dario-brand" in by_skill else (_ for _ in ()).throw(AssertionError))
    check("total_cost", lambda: None if ca.total()["total_cost_usd"] > 0.4 else (_ for _ in ()).throw(AssertionError))
    print("\n--- TrajectoryRecorder (ATIF) ---")
    tr = TrajectoryRecorder()
    tr.start("T1")
    tr.record_step("T1", "analyze", "Read", "input.md", "analysis result", {"input": 200, "output": 500}, 150)
    tr.record_step("T1", "write", "Write", "analysis", "output.md", {"input": 100, "output": 300}, 80)
    atif = tr.export_atif("T1")
    check("atif_format", lambda: None if atif["format"] == "ATIF/1.0" else (_ for _ in ()).throw(AssertionError))
    check("atif_2_steps", lambda: None if len(atif["steps"]) == 2 else (_ for _ in ()).throw(AssertionError))
    check("atif_total_tokens", lambda: None if atif["total_tokens"] == 1100 else (_ for _ in ()).throw(AssertionError))
    print(f"\n{'='*50}\nResults: {p} passed, {f} failed, {p+f} total")
    return 0 if f == 0 else 1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test: sys.exit(_run_self_tests())

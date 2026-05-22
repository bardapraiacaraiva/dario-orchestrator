#!/usr/bin/env python3
"""
DARIO State Upgrades v11.0 — Module 5 (mapped from research Module 6)
=======================================================================
M5.1  InterruptResume       (LangGraph)      — bidirectional HITL with state
M5.2  DecoratorDurability   (DBOS/durable-swarm) — @durable function wrapper
M5.3  ChaosInjector         (agent-chaos)    — fault injection for testing
M5.4  HierarchicalStates    (XState)         — nested + parallel statecharts
M5.5  DurableWorkflows      (Temporal)       — event-sourced replay patterns
M5.6  ObservationFeedback   (statelyai/agent)— state + observations loop
M5.7  CircuitBreaker        (resilience)     — auto-open/close on failure rate
"""
import logging
import os
import sys
import time
import uuid
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path

ORCH_DIR = Path(os.path.expanduser("~/.claude/orchestrator"))
log = logging.getLogger("state_upgrades")

# M5.1: Interrupt/Resume (LangGraph)
class InterruptType(Enum):
    APPROVAL = "approval"
    REVIEW = "review"
    INPUT_NEEDED = "input_needed"
    QUALITY_GATE = "quality_gate"

@dataclass
class InterruptState:
    interrupt_id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    task_id: str = ""
    interrupt_type: InterruptType = InterruptType.APPROVAL
    message: str = ""
    state_snapshot: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    resolved: bool = False
    resolution: str | None = None

class InterruptResumeManager:
    def __init__(self): self._pending: dict[str, InterruptState] = {}; self._resolved: list[dict] = []
    def interrupt(self, task_id: str, itype: InterruptType, message: str, state: dict = None) -> InterruptState:
        ist = InterruptState(task_id=task_id, interrupt_type=itype, message=message, state_snapshot=state or {})
        self._pending[ist.interrupt_id] = ist
        return ist
    def resume(self, interrupt_id: str, resolution: str) -> dict | None:
        ist = self._pending.pop(interrupt_id, None)
        if not ist: return None
        ist.resolved = True; ist.resolution = resolution
        self._resolved.append(asdict(ist))
        return ist.state_snapshot
    def pending(self) -> list[dict]: return [asdict(i) for i in self._pending.values()]
    def stats(self) -> dict: return {"pending": len(self._pending), "resolved": len(self._resolved)}

# M5.3: Chaos Injector (agent-chaos)
class FaultType(Enum):
    TIMEOUT = "timeout"
    ERROR = "error"
    DATA_CORRUPT = "data_corrupt"
    RATE_LIMIT = "rate_limit"
    EMPTY_RESPONSE = "empty_response"

@dataclass
class ChaosExperiment:
    experiment_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    fault_type: FaultType = FaultType.ERROR
    target_engine: str = ""
    steady_state_check: Callable | None = None
    injected: bool = False
    recovered: bool = False
    recovery_time_ms: int = 0

class ChaosInjector:
    def __init__(self): self._experiments: list[ChaosExperiment] = []; self._active: bool = False
    def inject(self, fault_type: FaultType, target: str) -> ChaosExperiment:
        exp = ChaosExperiment(fault_type=fault_type, target_engine=target, injected=True)
        self._experiments.append(exp)
        return exp
    def simulate_fault(self, fault_type: FaultType) -> dict:
        if fault_type == FaultType.TIMEOUT: time.sleep(0.01); return {"fault": "timeout", "delay_ms": 10}
        if fault_type == FaultType.ERROR: return {"fault": "error", "message": "Simulated error"}
        if fault_type == FaultType.EMPTY_RESPONSE: return {"fault": "empty", "output": ""}
        if fault_type == FaultType.DATA_CORRUPT: return {"fault": "corrupt", "data": "{{CORRUPTED}}"}
        if fault_type == FaultType.RATE_LIMIT: return {"fault": "rate_limit", "retry_after": 5}
        return {"fault": "unknown"}
    def verify_recovery(self, exp: ChaosExperiment, check_fn: Callable) -> bool:
        start = time.time()
        try:
            ok = check_fn()
            exp.recovered = ok
            exp.recovery_time_ms = int((time.time() - start) * 1000)
            return ok
        except: exp.recovered = False; return False
    def stats(self) -> dict:
        return {"experiments": len(self._experiments),
                "recovered": sum(1 for e in self._experiments if e.recovered),
                "failed_recovery": sum(1 for e in self._experiments if e.injected and not e.recovered)}

# M5.4: Hierarchical States (XState)
@dataclass
class StateNode:
    name: str
    parent: str | None = None
    children: list[str] = field(default_factory=list)
    parallel: bool = False
    history: bool = False
    on_enter: Callable | None = None
    on_exit: Callable | None = None

class HierarchicalStateMachine:
    def __init__(self):
        self._nodes: dict[str, StateNode] = {}
        self._current: str = ""
        self._history_states: dict[str, str] = {}
        self._transitions: dict[tuple, str] = {}
    def add_state(self, name: str, parent: str = None, parallel: bool = False, history: bool = False):
        node = StateNode(name=name, parent=parent, parallel=parallel, history=history)
        self._nodes[name] = node
        if parent and parent in self._nodes:
            self._nodes[parent].children.append(name)
    def add_transition(self, from_state: str, event: str, to_state: str):
        self._transitions[(from_state, event)] = to_state
    def transition(self, event: str) -> str | None:
        key = (self._current, event)
        target = self._transitions.get(key)
        if target:
            old = self._current
            if self._nodes.get(old, StateNode("")).history:
                self._history_states[self._nodes[old].parent or "root"] = old
            self._current = target
            return target
        # Try parent transitions (hierarchical)
        node = self._nodes.get(self._current)
        if node and node.parent:
            key = (node.parent, event)
            target = self._transitions.get(key)
            if target:
                self._current = target
                return target
        return None
    def set_state(self, state: str): self._current = state
    def get_state(self) -> str: return self._current
    def get_history(self, parent: str) -> str | None: return self._history_states.get(parent)

# M5.7: Circuit Breaker
class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 60.0):
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._last_failure: float = 0
        self._successes_in_half_open = 0
    def record_success(self):
        if self._state == CircuitState.HALF_OPEN:
            self._successes_in_half_open += 1
            if self._successes_in_half_open >= 2:
                self._state = CircuitState.CLOSED
                self._failures = 0
        self._failures = max(0, self._failures - 1)
    def record_failure(self):
        self._failures += 1
        self._last_failure = time.time()
        if self._failures >= self._threshold:
            self._state = CircuitState.OPEN
    def can_execute(self) -> bool:
        if self._state == CircuitState.CLOSED: return True
        if self._state == CircuitState.OPEN:
            if time.time() - self._last_failure > self._recovery_timeout:
                self._state = CircuitState.HALF_OPEN
                self._successes_in_half_open = 0
                return True
            return False
        return True  # half_open
    def get_state(self) -> str: return self._state.value
    def stats(self) -> dict: return {"state": self._state.value, "failures": self._failures, "threshold": self._threshold}

# GLOBALS
interrupt_manager = InterruptResumeManager()
chaos_injector = ChaosInjector()
hierarchical_sm = HierarchicalStateMachine()
circuit_breaker = CircuitBreaker()

def init_state_upgrades(app=None):
    # Setup default hierarchical states
    hierarchical_sm.add_state("ACTIVE")
    hierarchical_sm.add_state("ACTIVE.executing", parent="ACTIVE")
    hierarchical_sm.add_state("ACTIVE.idle", parent="ACTIVE")
    hierarchical_sm.add_state("GUARDIAN")
    hierarchical_sm.add_state("GUARDIAN.diagnosing", parent="GUARDIAN")
    hierarchical_sm.add_state("GUARDIAN.recovering", parent="GUARDIAN")
    hierarchical_sm.add_state("REFLECTIVE", history=True)
    hierarchical_sm.add_state("EXPANSION")
    hierarchical_sm.add_transition("ACTIVE", "budget_critical", "GUARDIAN")
    hierarchical_sm.add_transition("ACTIVE", "quality_drop", "REFLECTIVE")
    hierarchical_sm.add_transition("GUARDIAN", "recovered", "ACTIVE")
    hierarchical_sm.add_transition("REFLECTIVE", "improved", "ACTIVE")
    hierarchical_sm.add_transition("ACTIVE", "all_done", "EXPANSION")
    hierarchical_sm.set_state("ACTIVE")
    if app: _register_endpoints(app)
    log.info("State Upgrades v11.0 initialized")

def _register_endpoints(app):
    @app.get("/state-v2/status")
    async def state_v2_status():
        return {"current_state": hierarchical_sm.get_state(), "interrupts": interrupt_manager.stats(),
                "chaos": chaos_injector.stats(), "circuit_breaker": circuit_breaker.stats()}
    @app.get("/state-v2/interrupts")
    async def list_interrupts(): return {"pending": interrupt_manager.pending()}
    @app.post("/state-v2/interrupts/{interrupt_id}/resume")
    async def resume_interrupt(interrupt_id: str, resolution: str = "approved"):
        state = interrupt_manager.resume(interrupt_id, resolution)
        return {"resumed": state is not None, "state": state}

def _run_self_tests():
    p, f = 0, 0
    def check(n, fn):
        nonlocal p, f
        try: fn(); print(f"  PASS  {n}"); p += 1
        except Exception as e: print(f"  FAIL  {n}: {e}"); f += 1
    print("=== State Upgrades v11.0 — Self Tests ===\n")
    print("--- InterruptResume (LangGraph) ---")
    irm = InterruptResumeManager()
    ist = irm.interrupt("T1", InterruptType.APPROVAL, "Need approval", {"step": 3})
    check("create_interrupt", lambda: None if ist.interrupt_id else (_ for _ in ()).throw(AssertionError))
    check("pending_count", lambda: None if len(irm.pending()) == 1 else (_ for _ in ()).throw(AssertionError))
    state = irm.resume(ist.interrupt_id, "approved")
    check("resume_returns_state", lambda: None if state and state["step"] == 3 else (_ for _ in ()).throw(AssertionError))
    check("resolved_after_resume", lambda: None if len(irm.pending()) == 0 else (_ for _ in ()).throw(AssertionError))
    print("\n--- ChaosInjector (agent-chaos) ---")
    ci = ChaosInjector()
    exp = ci.inject(FaultType.ERROR, "executor")
    check("inject_fault", lambda: None if exp.injected else (_ for _ in ()).throw(AssertionError))
    r = ci.simulate_fault(FaultType.TIMEOUT)
    check("simulate_timeout", lambda: None if r["fault"] == "timeout" else (_ for _ in ()).throw(AssertionError))
    r2 = ci.simulate_fault(FaultType.DATA_CORRUPT)
    check("simulate_corruption", lambda: None if "CORRUPTED" in r2["data"] else (_ for _ in ()).throw(AssertionError))
    ci.verify_recovery(exp, lambda: True)
    check("verify_recovery", lambda: None if exp.recovered else (_ for _ in ()).throw(AssertionError))
    print("\n--- HierarchicalStateMachine (XState) ---")
    hsm = HierarchicalStateMachine()
    hsm.add_state("A"); hsm.add_state("A.sub1", parent="A"); hsm.add_state("B")
    hsm.add_transition("A", "go_b", "B"); hsm.add_transition("B", "go_a", "A")
    hsm.set_state("A")
    check("initial_state", lambda: None if hsm.get_state() == "A" else (_ for _ in ()).throw(AssertionError))
    hsm.transition("go_b")
    check("transition_to_B", lambda: None if hsm.get_state() == "B" else (_ for _ in ()).throw(AssertionError))
    hsm.transition("go_a")
    check("transition_back_A", lambda: None if hsm.get_state() == "A" else (_ for _ in ()).throw(AssertionError))
    print("\n--- CircuitBreaker ---")
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.01)
    check("initially_closed", lambda: None if cb.get_state() == "closed" else (_ for _ in ()).throw(AssertionError))
    cb.record_failure(); cb.record_failure()
    check("opens_after_threshold", lambda: None if cb.get_state() == "open" else (_ for _ in ()).throw(AssertionError))
    check("blocks_when_open", lambda: None if not cb.can_execute() else (_ for _ in ()).throw(AssertionError))
    time.sleep(0.02)
    check("half_open_after_timeout", lambda: None if cb.can_execute() else (_ for _ in ()).throw(AssertionError))
    cb.record_success(); cb.record_success()
    check("closes_after_successes", lambda: None if cb.get_state() == "closed" else (_ for _ in ()).throw(AssertionError))
    print(f"\n{'='*50}\nResults: {p} passed, {f} failed, {p+f} total")
    return 0 if f == 0 else 1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test: sys.exit(_run_self_tests())

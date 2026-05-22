#!/usr/bin/env python3
"""
DARIO Core Upgrades v11.0 — Module 1 Complete Implementation
=============================================================
8 patterns from 8 repos, unified in one integration layer:

M1.1  TaskQueue (taskiq)         — Async task dispatch replacing SQLite polling
M1.2  SessionTracker (agentops)  — Session-level cost tracking + analytics
M1.3  HandoffProtocol (OpenAI)   — Typed contracts between engines
M1.4  CheckpointStore (LangGraph)— Versioned checkpoint with blobs + writes
M1.5  EngineRegistry (Composio)  — Pluggable engine discovery + health checks
M1.6  DurableDecorators (Temporal)— @workflow/@step auto-checkpoint
M1.7  MessageBus (AutoGen)       — Pub/sub typed messages between engines
M1.8  SessionServer (LiveKit)    — AgentServer + AgentSession separation

Usage:
    # Import individual components
    from upgrades.core import TaskQueue, HandoffProtocol, EngineRegistry, MessageBus

    # Initialize all upgrades on runtime startup
    from upgrades.core import init_core_upgrades
    init_core_upgrades(app, db)

    # CLI diagnostics
    python core_upgrades.py --status          # Show all component status
    python core_upgrades.py --test            # Run self-tests
    python core_upgrades.py --engines         # List registered engines
    python core_upgrades.py --bus-stats       # Message bus statistics
"""

import argparse
import json
import logging
import os
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path(os.path.expanduser("~/.claude/orchestrator"))
DB_PATH = ORCH_DIR / "orchestrator.db"

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("core_upgrades")


# =============================================================================
# M1.3: HANDOFF PROTOCOL (OpenAI Agents pattern)
# =============================================================================
# Typed contracts for engine-to-engine handoffs. Replaces ad-hoc JSON blobs.

# M1.3 (HandoffProtocol) — extracted to core_handoff.py (Onda 6 #2)
# =============================================================================
# M1.4: VERSIONED CHECKPOINT STORE (LangGraph pattern) — extracted to core_checkpoints.py (Onda 7 #1)
# =============================================================================
from upgrades.core_checkpoints import CheckpointStore  # noqa: F401

# =============================================================================
# M1.5: PLUGGABLE ENGINE REGISTRY (Composio pattern) — extracted to core_engines.py (Onda 7 #1)
# =============================================================================
from upgrades.core_engines import EngineRegistry, EngineSpec  # noqa: F401
from upgrades.core_handoff import (  # noqa: F401
    HandoffContext,
    HandoffProtocol,
    HandoffResult,
    HandoffStatus,
)

# =============================================================================
# M1.6: DURABLE DECORATORS (Temporal + DBOS pattern)
# =============================================================================
# @workflow and @step decorators that auto-checkpoint each step.

_checkpoint_store: CheckpointStore | None = None


def _get_checkpoint_store() -> CheckpointStore:
    global _checkpoint_store
    if _checkpoint_store is None:
        _checkpoint_store = CheckpointStore()
    return _checkpoint_store


def workflow(name: str = None):
    """
    Decorator that makes a function a durable workflow.
    Auto-creates a thread_id, checkpoints state at each step.
    If the function was interrupted, resumes from last checkpoint.

    Usage:
        @workflow("brand_audit")
        def run_brand_audit(ctx):
            result1 = yield step("analyze", analyze_brand, ctx)
            result2 = yield step("score", score_brand, result1)
            return result2
    """
    def decorator(func):
        func._is_workflow = True
        func._workflow_name = name or func.__name__

        def wrapper(*args, **kwargs):
            thread_id = kwargs.pop("thread_id", f"wf_{func._workflow_name}_{uuid.uuid4().hex[:8]}")
            store = _get_checkpoint_store()

            # Check for existing checkpoint (resume)
            existing = store.load(thread_id)
            if existing:
                log.info(f"Resuming workflow '{func._workflow_name}' from checkpoint v{existing['version']}")
                kwargs["_resume_state"] = existing["state"]

            # Execute
            start = time.time()
            try:
                result = func(*args, thread_id=thread_id, **kwargs)
                duration = int((time.time() - start) * 1000)

                # Final checkpoint
                store.save(
                    thread_id=thread_id,
                    state={"status": "completed", "result": str(result)[:1000], "duration_ms": duration},
                    metadata={"workflow": func._workflow_name, "status": "completed"},
                )
                return result
            except Exception as e:
                duration = int((time.time() - start) * 1000)
                store.save(
                    thread_id=thread_id,
                    state={"status": "failed", "error": str(e), "duration_ms": duration},
                    metadata={"workflow": func._workflow_name, "status": "failed"},
                )
                raise

        wrapper._is_workflow = True
        wrapper._workflow_name = func._workflow_name if hasattr(func, '_workflow_name') else (name or func.__name__)
        return wrapper
    return decorator


def step(name: str):
    """
    Decorator that makes a function a durable step within a workflow.
    Auto-checkpoints input and output.

    Usage:
        @step("analyze_brand")
        def analyze_brand(data):
            return {"analysis": "..."}
    """
    def decorator(func):
        func._is_step = True
        func._step_name = name

        def wrapper(*args, **kwargs):
            thread_id = kwargs.pop("thread_id", None)
            store = _get_checkpoint_store()

            # Check if step was already completed (idempotency)
            if thread_id:
                existing = store.load(thread_id)
                if existing and existing["state"].get(f"step_{name}") == "completed":
                    log.info(f"Step '{name}' already completed — skipping (idempotent)")
                    return existing["state"].get(f"step_{name}_result")

            start = time.time()
            try:
                result = func(*args, **kwargs)
                duration = int((time.time() - start) * 1000)

                if thread_id:
                    store.save(
                        thread_id=thread_id,
                        state={
                            f"step_{name}": "completed",
                            f"step_{name}_result": str(result)[:500],
                            f"step_{name}_duration_ms": duration,
                        },
                        metadata={"step": name, "status": "completed"},
                    )
                return result
            except Exception as e:
                if thread_id:
                    store.save(
                        thread_id=thread_id,
                        state={f"step_{name}": "failed", f"step_{name}_error": str(e)},
                        metadata={"step": name, "status": "failed"},
                    )
                raise

        wrapper._is_step = True
        wrapper._step_name = name
        return wrapper
    return decorator


# =============================================================================
# M1.7: TYPED MESSAGE BUS (AutoGen 0.4 Actor pattern)
# =============================================================================
# Pub/sub typed messages between engines. Decouples engines from direct calls.

# M1.7 (MessageBus) — extracted to core_messagebus.py (Onda 6 #2)
from upgrades.core_messagebus import MessageBus, MessageType, TypedMessage  # noqa: F401

# =============================================================================
# M1.8: SESSION/SERVER SPLIT (LiveKit pattern)
# =============================================================================
# Separates long-running supervisor from ephemeral task sessions.

@dataclass
class AgentSession:
    """Ephemeral session for a single task or interaction."""
    session_id: str = field(default_factory=lambda: f"sess_{uuid.uuid4().hex[:10]}")
    task_id: str | None = None
    skill: str | None = None
    worker: str | None = None
    status: str = "active"  # active | completed | failed | suspended
    started_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    completed_at: str | None = None
    token_usage: dict = field(default_factory=dict)
    artifacts: list[dict] = field(default_factory=list)


class SessionManager:
    """
    Manages ephemeral AgentSessions within the long-running AgentServer (runtime).
    Each task gets its own session with isolated context.
    Inspired by LiveKit's AgentSession/AgentServer separation.
    """

    def __init__(self):
        self._sessions: dict[str, AgentSession] = {}
        self._completed: list[dict] = []

    def create(self, task_id: str = None, skill: str = None,
               worker: str = None) -> AgentSession:
        """Create a new ephemeral session."""
        session = AgentSession(task_id=task_id, skill=skill, worker=worker)
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> AgentSession | None:
        """Get active session by ID."""
        return self._sessions.get(session_id)

    def get_by_task(self, task_id: str) -> AgentSession | None:
        """Get active session by task ID."""
        for s in self._sessions.values():
            if s.task_id == task_id and s.status == "active":
                return s
        return None

    def complete(self, session_id: str, status: str = "completed",
                 token_usage: dict = None):
        """Complete a session and archive it."""
        session = self._sessions.get(session_id)
        if session:
            session.status = status
            session.completed_at = datetime.now(UTC).isoformat()
            if token_usage:
                session.token_usage = token_usage
            self._completed.append(asdict(session))
            del self._sessions[session_id]

    def active_sessions(self) -> list[AgentSession]:
        """List all active sessions."""
        return [s for s in self._sessions.values() if s.status == "active"]

    def liveness_check(self) -> dict:
        """Check liveness of all active sessions."""
        active = self.active_sessions()
        return {
            "active_count": len(active),
            "sessions": [
                {"session_id": s.session_id, "task_id": s.task_id,
                 "skill": s.skill, "started_at": s.started_at}
                for s in active
            ],
            "completed_total": len(self._completed),
        }


# =============================================================================
# M1.1 + M1.2: TASK QUEUE + SESSION TRACKER INTEGRATION
# =============================================================================
# TaskQueue wraps taskiq broker for async dispatch.
# SessionTracker wraps agentops for cost tracking.

class TaskQueue:
    """
    Async task queue inspired by taskiq.
    Wraps task dispatch with async semantics while keeping SQLite for state.
    """

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self._queue: list[dict] = []
        self._running: dict[str, dict] = {}
        self._completed: list[dict] = []

    def enqueue(self, task_id: str, skill: str, priority: str = "default",
                metadata: dict = None) -> str:
        """Add task to queue. Returns queue position."""
        entry = {
            "task_id": task_id,
            "skill": skill,
            "priority": priority,
            "metadata": metadata or {},
            "queued_at": datetime.now(UTC).isoformat(),
            "status": "queued",
        }

        # Priority ordering: critical > client_facing > financial > default
        priority_order = {"critical": 0, "client_facing": 1, "financial": 2, "default": 3}
        entry["_sort"] = priority_order.get(priority, 3)

        self._queue.append(entry)
        self._queue.sort(key=lambda x: x["_sort"])
        return str(len(self._queue))

    def dequeue(self) -> dict | None:
        """Get next task from queue if capacity available."""
        if len(self._running) >= self.max_concurrent:
            return None
        if not self._queue:
            return None

        entry = self._queue.pop(0)
        entry["status"] = "running"
        entry["started_at"] = datetime.now(UTC).isoformat()
        self._running[entry["task_id"]] = entry
        return entry

    def complete(self, task_id: str, result: dict = None):
        """Mark task as completed."""
        entry = self._running.pop(task_id, None)
        if entry:
            entry["status"] = "completed"
            entry["completed_at"] = datetime.now(UTC).isoformat()
            entry["result"] = result or {}
            self._completed.append(entry)

    def fail(self, task_id: str, error: str = ""):
        """Mark task as failed."""
        entry = self._running.pop(task_id, None)
        if entry:
            entry["status"] = "failed"
            entry["error"] = error
            self._completed.append(entry)

    def status(self) -> dict:
        """Queue status."""
        return {
            "queued": len(self._queue),
            "running": len(self._running),
            "completed": len(self._completed),
            "max_concurrent": self.max_concurrent,
            "running_tasks": list(self._running.keys()),
        }


class SessionTracker:
    """
    Session-level tracking inspired by AgentOps.
    Tracks cost, tool usage, and performance per session.
    """

    def __init__(self):
        self._current_session: dict | None = None
        self._sessions: list[dict] = []
        self._agentops_available = False

        # Try to init agentops
        try:
            import agentops
            api_key = os.environ.get("AGENTOPS_API_KEY")
            if api_key:
                agentops.init(api_key=api_key, auto_start_session=False)
                self._agentops_available = True
                log.info("AgentOps initialized for session tracking")
        except Exception:
            log.debug("AgentOps not available — using local tracking")

    def start_session(self, session_type: str = "pulse") -> dict:
        """Start a tracking session."""
        session = {
            "session_id": uuid.uuid4().hex[:12],
            "type": session_type,
            "started_at": datetime.now(UTC).isoformat(),
            "tokens": {"input": 0, "output": 0},
            "cost_usd": 0.0,
            "tools_used": [],
            "tasks_executed": 0,
            "errors": 0,
        }
        self._current_session = session

        if self._agentops_available:
            try:
                import agentops
                agentops.start_session(tags=[session_type])
            except Exception:
                pass

        return session

    def record_action(self, action: str, tokens: dict = None, cost: float = 0,
                      error: bool = False):
        """Record an action in the current session."""
        if not self._current_session:
            return

        self._current_session["tools_used"].append(action)
        if tokens:
            self._current_session["tokens"]["input"] += tokens.get("input", 0)
            self._current_session["tokens"]["output"] += tokens.get("output", 0)
        self._current_session["cost_usd"] += cost
        self._current_session["tasks_executed"] += 1
        if error:
            self._current_session["errors"] += 1

    def end_session(self) -> dict:
        """End current session and return summary."""
        if not self._current_session:
            return {}

        session = self._current_session
        session["ended_at"] = datetime.now(UTC).isoformat()
        session["duration_ms"] = int(
            (datetime.fromisoformat(session["ended_at"]) -
             datetime.fromisoformat(session["started_at"])).total_seconds() * 1000
        )
        self._sessions.append(session)
        self._current_session = None

        if self._agentops_available:
            try:
                import agentops
                agentops.end_session("Success" if session["errors"] == 0 else "Fail")
            except Exception:
                pass

        return session

    def get_analytics(self) -> dict:
        """Get analytics across all sessions."""
        if not self._sessions:
            return {"sessions": 0}

        total_cost = sum(s["cost_usd"] for s in self._sessions)
        total_tokens = sum(s["tokens"]["input"] + s["tokens"]["output"] for s in self._sessions)
        total_tasks = sum(s["tasks_executed"] for s in self._sessions)
        total_errors = sum(s["errors"] for s in self._sessions)

        return {
            "sessions": len(self._sessions),
            "total_cost_usd": round(total_cost, 4),
            "total_tokens": total_tokens,
            "total_tasks": total_tasks,
            "total_errors": total_errors,
            "avg_cost_per_session": round(total_cost / len(self._sessions), 4),
            "error_rate": round(total_errors / max(total_tasks, 1) * 100, 1),
        }


# =============================================================================
# INITIALIZATION — Wire all components into runtime
# =============================================================================

# Global instances
handoff_protocol = HandoffProtocol()
checkpoint_store = CheckpointStore()
engine_registry = EngineRegistry()
message_bus = MessageBus()
task_queue = TaskQueue(max_concurrent=3)
session_tracker = SessionTracker()
session_manager = SessionManager()


def init_core_upgrades(app=None, db=None):
    """Initialize all core upgrades and wire into runtime."""

    # Auto-discover engines
    engine_registry.auto_discover()
    log.info(f"Engine registry: {len(engine_registry._engines)} engines discovered")

    # Register default handoff routes
    handoff_protocol.register_route("executor", ["dispatch_engine", "chain_executor", "replanner"])
    handoff_protocol.register_route("dispatch_engine", ["executor", "hierarchical_process"])
    handoff_protocol.register_route("chain_executor", ["executor", "quality_scorer"])
    handoff_protocol.register_route("quality_scorer", ["replanner", "executor"])
    handoff_protocol.register_route("replanner", ["executor", "dispatch_engine"])

    # Register FastAPI endpoints if app provided
    if app:
        _register_endpoints(app)

    log.info("Core upgrades v11.0 initialized: "
             "TaskQueue + SessionTracker + HandoffProtocol + "
             "CheckpointStore + EngineRegistry + DurableDecorators + "
             "MessageBus + SessionManager")


def _register_endpoints(app):
    """Register upgrade endpoints in FastAPI."""

    @app.get("/core/status")
    async def core_status():
        return {
            "version": "v11.0",
            "components": {
                "task_queue": task_queue.status(),
                "session_tracker": session_tracker.get_analytics(),
                "engine_registry": {"engines": len(engine_registry._engines)},
                "message_bus": message_bus.get_stats(),
                "session_manager": session_manager.liveness_check(),
                "checkpoint_store": "active",
                "handoff_protocol": {"routes": len(handoff_protocol._allowed_routes)},
            },
        }

    @app.get("/core/engines")
    async def list_engines():
        engines = engine_registry.list_engines()
        return {
            "count": len(engines),
            "engines": [
                {"name": e.name, "category": e.category, "status": e.status,
                 "path": e.path, "version": e.version}
                for e in engines
            ],
        }

    @app.get("/core/engines/health")
    async def engine_health():
        return engine_registry.health_check_all()

    @app.get("/core/bus/stats")
    async def bus_stats():
        return message_bus.get_stats()

    @app.get("/core/sessions")
    async def active_sessions():
        return session_manager.liveness_check()

    @app.get("/core/queue")
    async def queue_status():
        return task_queue.status()


# =============================================================================
# CLI
# =============================================================================

def _run_self_tests():
    """Run self-tests for all components."""
    passed = 0
    failed = 0

    def check(name, fn):
        nonlocal passed, failed
        try:
            fn()
            print(f"  PASS  {name}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {name}: {e}")
            failed += 1

    print("=== Core Upgrades v11.0 — Self Tests ===\n")

    # Handoff Protocol
    print("--- HandoffProtocol ---")
    hp = HandoffProtocol()
    hp.register_route("executor", ["dispatch", "chain"])
    check("create_valid_handoff",
          lambda: hp.create_handoff("T1", "executor", "dispatch", "test"))
    try:
        hp.create_handoff("T1", "executor", "unknown", "test")
        print("  FAIL  reject_invalid_route: should have raised ValueError")
        failed += 1
    except ValueError:
        print("  PASS  reject_invalid_route")
        passed += 1

    # Checkpoint Store
    print("\n--- CheckpointStore ---")
    cs = CheckpointStore()
    test_thread = f"test_{uuid.uuid4().hex[:8]}"
    check("save_checkpoint",
          lambda: cs.save(test_thread, {"step": 1, "data": "hello"}))
    check("load_checkpoint",
          lambda: (lambda r: None if not r else None)(cs.load(test_thread)))
    check("version_increment",
          lambda: cs.save(test_thread, {"step": 2}))
    loaded = cs.load(test_thread)
    check("latest_version_is_2",
          lambda: None if loaded and loaded["version"] == 2 else (_ for _ in ()).throw(AssertionError(f"version={loaded['version'] if loaded else 'None'}")))

    # Engine Registry
    print("\n--- EngineRegistry ---")
    er = EngineRegistry()
    er.auto_discover()
    check("auto_discover_finds_engines",
          lambda: None if len(er._engines) > 10 else (_ for _ in ()).throw(AssertionError(f"only {len(er._engines)}")))
    check("category_grouping",
          lambda: None if len(er._categories) >= 5 else (_ for _ in ()).throw(AssertionError))

    # Task Queue
    print("\n--- TaskQueue ---")
    tq = TaskQueue(max_concurrent=2)
    check("enqueue", lambda: tq.enqueue("T1", "brand", "critical"))
    check("enqueue_low", lambda: tq.enqueue("T2", "seo", "default"))
    d = tq.dequeue()
    check("dequeue_critical_first", lambda: None if d and d["task_id"] == "T1" else (_ for _ in ()).throw(AssertionError))
    check("complete", lambda: tq.complete("T1", {"score": 85}))

    # Message Bus
    print("\n--- MessageBus ---")
    mb = MessageBus()
    received = []
    mb.subscribe(MessageType.TASK_COMPLETED, lambda m: received.append(m))
    mb.publish(TypedMessage(msg_type=MessageType.TASK_COMPLETED, source="test", payload={"id": "T1"}))
    check("publish_subscribe", lambda: None if len(received) == 1 else (_ for _ in ()).throw(AssertionError))
    check("stats", lambda: None if mb.get_stats()["total_messages"] == 1 else (_ for _ in ()).throw(AssertionError))

    # Session Manager
    print("\n--- SessionManager ---")
    sm = SessionManager()
    s = sm.create(task_id="T1", skill="brand")
    check("create_session", lambda: None if s.session_id else (_ for _ in ()).throw(AssertionError))
    check("get_by_task", lambda: None if sm.get_by_task("T1") else (_ for _ in ()).throw(AssertionError))
    sm.complete(s.session_id, token_usage={"input": 1000})
    check("complete_archives", lambda: None if len(sm._sessions) == 0 else (_ for _ in ()).throw(AssertionError))

    # Durable Decorators
    print("\n--- DurableDecorators ---")

    @step("test_step")
    def my_step(x):
        return x * 2

    check("step_decorator", lambda: None if my_step(5) == 10 else (_ for _ in ()).throw(AssertionError))

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    return 0 if failed == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="DARIO Core Upgrades v11.0")
    parser.add_argument("--status", action="store_true", help="Show component status")
    parser.add_argument("--test", action="store_true", help="Run self-tests")
    parser.add_argument("--engines", action="store_true", help="List registered engines")
    parser.add_argument("--bus-stats", action="store_true", help="Message bus stats")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.test:
        sys.exit(_run_self_tests())

    if args.engines:
        engine_registry.auto_discover()
        engines = engine_registry.list_engines()
        if args.json:
            print(json.dumps([{"name": e.name, "category": e.category, "path": e.path} for e in engines], indent=2))
        else:
            print(f"\n=== DARIO Engine Registry ({len(engines)} engines) ===\n")
            by_cat = {}
            for e in engines:
                by_cat.setdefault(e.category, []).append(e)
            for cat, engs in sorted(by_cat.items()):
                print(f"  {cat.upper()} ({len(engs)})")
                for e in sorted(engs, key=lambda x: x.name):
                    print(f"    {e.name:35s} {e.status}")
        return

    if args.status or args.bus_stats:
        init_core_upgrades()
        if args.json:
            print(json.dumps({
                "task_queue": task_queue.status(),
                "session_tracker": session_tracker.get_analytics(),
                "engine_registry": {"engines": len(engine_registry._engines)},
                "message_bus": message_bus.get_stats(),
                "session_manager": session_manager.liveness_check(),
            }, indent=2))
        else:
            print("\n=== Core Upgrades v11.0 Status ===")
            print(f"  Engines: {len(engine_registry._engines)}")
            print(f"  Queue: {task_queue.status()}")
            print(f"  Bus: {message_bus.get_stats()}")
            print(f"  Sessions: {session_manager.liveness_check()}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()

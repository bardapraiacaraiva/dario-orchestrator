#!/usr/bin/env python3
"""
DARIO Runtime Engine — Persistent FastAPI server for the orchestrator.
======================================================================
Runs independently of Claude sessions. Provides REST API for all ops.
Internal scheduler replaces cron hacks. WebSocket for live updates.

Start:
    python runtime.py                    # Port 8422
    python runtime.py --port 8422        # Custom port
    python runtime.py --no-scheduler     # Without heartbeat scheduler

API Endpoints:
    GET  /health              — System health + state
    GET  /tasks               — List tasks (query: ?status=todo&project=X)
    POST /tasks               — Create task
    POST /tasks/{id}/assign   — Assign task to worker
    POST /tasks/{id}/complete — Complete task with score
    GET  /dispatch            — Run dispatch (dry-run by default)
    POST /dispatch            — Execute dispatch (assign tasks)
    GET  /state              — Current state machine status
    POST /state/transition    — Force state transition
    GET  /audit              — Audit log (query: ?limit=50&actor=X)
    GET  /budget             — Current budget
    GET  /scores             — Skill performance stats
    POST /pulse              — Trigger heartbeat pulse manually
    GET  /chains             — List chain runs
    POST /chains/{name}/start — Start a skill chain

Scheduler:
    - Heartbeat every 30 minutes (calls dispatch + state check)
    - AutoDiag every hour
    - Evolution cycle daily at 03:00

Port: 8422 (to not conflict with RAG on 8420, Runtime on 8421)
"""

import asyncio
import json
import logging
import subprocess
import sys
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add orchestrator dir to path for imports
ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from core.db import DB

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("runtime")

# ─── Globals ─────────────────────────────────────────────────────────────────
db = DB()
PYTHON = sys.executable
scheduler_enabled = True


# ─── Scheduler ───────────────────────────────────────────────────────────────

class Scheduler:
    """Internal heartbeat scheduler (replaces cron hacks)."""

    def __init__(self):
        self.running = False
        self._task = None
        self.pulse_count = 0
        self.last_pulse = None

    async def start(self):
        self.running = True
        self._task = asyncio.create_task(self._loop())
        log.info("Scheduler started (30min heartbeat)")

    async def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()

    async def _loop(self):
        while self.running:
            try:
                await self._pulse()
                self.pulse_count += 1
                self.last_pulse = datetime.now(UTC).isoformat()
            except Exception as e:
                log.error(f"Pulse error: {e}")
            await asyncio.sleep(1800)  # 30 minutes

    async def _pulse(self):
        """Execute heartbeat pulse via subprocess."""
        # Zombie task reaper
        self._reap_zombies()
        # State check
        _run_engine("core/state_machine.py", ["--evaluate", "--json"])
        # Dispatch
        _run_engine("dispatch_engine.py", ["--json"])
        # AutoDiag
        _run_engine("core/autodiag_runner.py", ["--fix", "--json"])
        # Evolution cycle (was ORPHAN — the system's differentiator, never ran)
        if self.pulse_count > 0 and self.pulse_count % 48 == 0:  # Every ~24h (48 * 30min)
            _run_engine("execution/evolution_runner.py", ["--json"])
            log.info("[EVOLUTION] Daily cycle executed")
        # Budget tracker (root budget_tracker.py died in the 84→2 refactor; the scripts/ shim is the survivor)
        _run_engine("scripts/budget_tracker.py", ["--check", "--quiet"])
        # Dashboard refresh (was ORPHAN — dashboard went stale between manual runs)
        _run_engine("observability/generate_dashboard.py", [])
        log.info(f"Pulse #{self.pulse_count + 1} complete")

    def _reap_zombies(self, max_age_minutes: int = 60):
        """Find tasks stuck in in_progress and block them (new: zombie reaper)."""
        try:
            from core.db import DB
            db = DB()
            tasks = db.get_tasks(status="in_progress")
            now = datetime.now(UTC)
            reaped = 0
            for t in tasks:
                checked_out = t.get("checked_out_at", "")
                if not checked_out:
                    continue
                try:
                    co_time = datetime.fromisoformat(checked_out.replace("Z", "+00:00"))
                    age_min = (now - co_time).total_seconds() / 60
                    if age_min > max_age_minutes:
                        db.block_task(t["id"], f"Zombie reaper: in_progress for {age_min:.0f} min (max {max_age_minutes})")
                        db.log_event("zombie_reaper", "task_reaped", task_id=t["id"],
                                    details=f"Stuck {age_min:.0f} min")
                        reaped += 1
                except Exception:
                    pass
            if reaped:
                log.warning(f"[REAPER] Reaped {reaped} zombie tasks")
        except Exception as e:
            log.error(f"[REAPER] Error: {e}")


scheduler = Scheduler()


def _run_engine(script: str, args: list) -> dict:
    """Run an orchestrator engine and return parsed JSON."""
    script_path = ORCH_DIR / script
    if not script_path.exists():
        log.error(f"[ENGINE] {script} not found — pulse step silently skipped until path is fixed")
        return {"error": f"{script} not found"}
    try:
        result = subprocess.run(
            [PYTHON, str(script_path)] + args,
            capture_output=True, text=True, timeout=30, cwd=str(ORCH_DIR)
        )
        if result.stdout.strip():
            try:
                return json.loads(result.stdout.strip())
            except json.JSONDecodeError:
                return {"raw": result.stdout.strip()[:500]}
        return {"exit_code": result.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)[:200]}


# ─── Lifespan ────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # LICENSE CHECK (was ORPHAN — never enforced, anyone could run indefinitely)
    try:
        from licensing.license_manager import check_license
        lic = check_license()
        if not lic.get("valid"):
            log.error(f"[LICENSE] {lic.get('reason', 'Invalid')}. Runtime blocked.")
            log.error("[LICENSE] Activate: python license_manager.py --activate DARIO-XXXX-XXXX-XXXX-PRO")
            # Don't sys.exit — allow health endpoint but block task execution
            app.state.license_valid = False
        else:
            app.state.license_valid = True
            tier = lic.get("tier", "?")
            days = lic.get("days_remaining", "permanent")
            log.info(f"[LICENSE] {tier.upper()} — {'permanent' if lic.get('permanent') else f'{days} days remaining'}")
    except Exception as e:
        log.warning(f"[LICENSE] Check failed: {e} — allowing startup")
        app.state.license_valid = True  # Fail-open for dev

    # STARTUP: Resume suspended tasks
    try:
        _run_engine("suspend_resume.py", ["--restart-all", "--json"])
        log.info("[STARTUP] Suspended tasks resumed")
    except Exception as e:
        log.warning(f"[STARTUP] Resume failed: {e}")

    if scheduler_enabled:
        await scheduler.start()

    yield

    # SHUTDOWN: Suspend all in_progress tasks (new: was not wired)
    try:
        _run_engine("suspend_resume.py", ["--suspend-all", "--json"])
        log.info("[SHUTDOWN] Active tasks suspended")
    except Exception as e:
        log.warning(f"[SHUTDOWN] Suspend failed: {e}")

    if scheduler_enabled:
        await scheduler.stop()


# ─── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="DARIO Orchestrator Runtime",
    version="3.1.0",
    description="Persistent runtime engine for the DARIO orchestrator ecosystem",
    lifespan=lifespan,
)

# CORS — dashboards served from :8766 (http) or opened via file:// (origin=null)
# fetch this API on :8422. Without CORS, every browser XHR is blocked and the UI
# stays in "awaiting telemetry" forever. Localhost-only by design.
#
# `allow_origins=["null"]` is intentional: browsers send `Origin: null` for
# file:// pages. Risk is acceptable since the API listens only on 127.0.0.1
# (loopback) — no external attacker can reach it. The threat is "user opens
# malicious local .html that calls our API" which already implies prior
# compromise of the user's filesystem.
try:
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["null"],
        allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    log.info("[CORS] Middleware installed (localhost/127.0.0.1 any port + file:// null origin)")
except Exception as e:
    log.warning(f"[CORS] Middleware install failed: {e}")

# OpenTelemetry tracing (v12.1 / Onda 1 #4 — real OTel, exports to Langfuse if env set)
try:
    from observability.otel_setup import instrument_fastapi, setup_tracing
    setup_tracing(service_name="dario-orchestrator-runtime")
    instrument_fastapi(app)
except Exception as e:
    log.warning(f"[OTel] tracing setup failed: {e} — runtime running without tracing")

# License middleware (v11.1+ hardening — 2026-05-19)
# Guards ALL endpoints except whitelist (/health, /license/*, /docs, /openapi.json).
# Returns 402 Payment Required when trial expired or no license.
# Bypass requires DARIO_LICENSE_BYPASS=1 env AND dev.flag file (double-gate).
try:
    from licensing.license_guard import fastapi_middleware as license_middleware
    license_middleware(app)
    log.info("[LICENSE] Middleware installed — all non-whitelisted endpoints guarded")
except Exception as e:
    log.warning(f"[LICENSE] Middleware install failed: {e} — runtime running in fail-open mode")

# Auth middleware (was ORPHAN — all endpoints were unauthenticated)
try:
    from fastapi import Request
    from starlette.middleware.base import BaseHTTPMiddleware

    from licensing.auth import verify_key  # check_permission imported elsewhere on demand

    class AuthMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            # Skip auth for health and docs
            if request.url.path in ("/health", "/docs", "/openapi.json", "/dashboard"):
                return await call_next(request)
            # Check API key header
            api_key = request.headers.get("X-API-Key", "")
            if api_key:
                auth_result = verify_key(api_key)
                if not auth_result.get("valid"):
                    from fastapi.responses import JSONResponse
                    return JSONResponse({"detail": "Invalid API key"}, status_code=401)
                request.state.role = auth_result.get("role", "viewer")
            # Allow unauthenticated for localhost (dev mode)
            elif request.client and request.client.host in ("127.0.0.1", "localhost", "::1"):
                request.state.role = "admin"
            else:
                request.state.role = "viewer"  # Read-only for unknown callers
            return await call_next(request)

    app.add_middleware(AuthMiddleware)
    log.info("[AUTH] Middleware active (was orphaned)")
except ImportError:
    log.warning("[AUTH] auth.py not available — endpoints unauthenticated")


# ─── Models ──────────────────────────────────────────────────────────────────
# v12.1 — TaskCreate and TaskComplete now live in schemas.contracts (central
# Pydantic layer). The two request-only models below stay here because they
# are only used by this HTTP surface.

from schemas import (  # noqa: E402  (kept after middleware setup)
    AssignResponse,
    AuditResponse,
    BudgetResponse,
    CheckoutResponse,
    CompleteResponse,
    DispatchResponse,
    EventStatsResponse,
    HealthResponse,
    ParsedDocumentResponse,
    PulseResponse,
    RubricResponse,
    ScoresResponse,
    StateResponse,
    TaskComplete,
    TaskCreate,
    TaskListResponse,
    TaxAlertResponse,
    TemplateInstantiateResponse,
    TemplateListResponse,
    ValidationCheckResponse,
    WebhookListResponse,
    WebhookTestResponse,
)


class AssignRequest(BaseModel):
    worker_id: str
    reason: str = ""


class TransitionRequest(BaseModel):
    target_state: str


# ─── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
async def health():
    state_result = _run_engine("core/state_machine.py", ["--json"])
    return HealthResponse(
        status="ok",
        state=state_result.get("state", "?"),
        autonomy=state_result.get("autonomy_level", "?"),
        health=state_result.get("system_health", 0),
        timestamp=datetime.now(UTC).isoformat(),
        scheduler={"running": scheduler.running, "pulses": scheduler.pulse_count},
        db=db.stats(),
    )


@app.get("/tasks", response_model=TaskListResponse)
async def list_tasks(status: str = None, project: str = None,
                     assignee: str = None, unassigned: bool = False):
    tasks = db.get_tasks(status=status, project=project,
                         assignee=assignee, unassigned=unassigned)
    return TaskListResponse(count=len(tasks), tasks=tasks)


@app.post("/tasks")
async def create_task(task: TaskCreate):
    result = db.create_task(
        id=task.id, title=task.title, project=task.project,
        skill=task.skill, priority=task.priority, description=task.description,
        execution_policy=task.execution_policy, depends_on=task.depends_on,
        estimated_tokens=task.estimated_tokens
    )
    return result


@app.post("/tasks/{task_id}/assign", response_model=AssignResponse)
async def assign_task(task_id: str, req: AssignRequest):
    success = db.assign_task(task_id, req.worker_id, req.reason)
    if not success:
        raise HTTPException(400, "Assignment failed (task not in todo state or already assigned)")
    return AssignResponse(assigned=True, task_id=task_id, worker=req.worker_id)


@app.post("/tasks/{task_id}/checkout", response_model=CheckoutResponse)
async def checkout_task(task_id: str):
    success = db.checkout_task(task_id)
    if not success:
        raise HTTPException(400, "Checkout failed (not assigned or not in todo)")
    return CheckoutResponse(checked_out=True, task_id=task_id)


@app.post("/tasks/{task_id}/complete", response_model=CompleteResponse)
async def complete_task(task_id: str, req: TaskComplete):
    success = db.complete_task(task_id, req.score, req.tokens, req.output, req.status)
    if not success:
        raise HTTPException(400, "Complete failed (task not in_progress)")
    if req.score > 0:
        task = db.get_task(task_id)
        if task:
            db.record_score(task_id, task.get("skill", ""), req.score, task.get("project", ""))
    return CompleteResponse(completed=True, task_id=task_id, score=req.score)


@app.get("/dispatch", response_model=DispatchResponse)
async def dispatch_dry_run():
    result = _run_engine("dispatch_engine.py", ["--dry-run", "--json"])
    return result


@app.post("/dispatch", response_model=DispatchResponse)
async def dispatch_execute():
    result = _run_engine("dispatch_engine.py", ["--json"])
    return result


@app.get("/state", response_model=StateResponse)
async def get_state():
    return _run_engine("core/state_machine.py", ["--json"])


@app.get("/org")
async def get_org_tree():
    """Return the org hierarchy from company.yaml with live task load.

    Powers agent-visualizer.html — replaces the previously hardcoded tree.
    Status (`active`/`idle`) per node derives from active tasks of workers
    under that subtree. Single source of truth: company.yaml + orchestrator.db.
    """
    try:
        from core.org_tree import build_tree
        return build_tree()
    except Exception as e:
        return {"error": str(e)[:200], "tree": None, "nodes": [], "stats": {}}


@app.post("/state/transition", response_model=StateResponse)
async def force_transition(req: TransitionRequest):
    result = _run_engine("core/state_machine.py", ["--transition", req.target_state, "--json"])
    return result


@app.get("/audit", response_model=AuditResponse)
async def get_audit(limit: int = 50, actor: str = None, task_id: str = None):
    entries = db.get_audit(limit=limit, actor=actor, task_id=task_id)
    return AuditResponse(count=len(entries), entries=entries)


@app.get("/budget", response_model=BudgetResponse)
async def get_budget(month: str = None):
    return db.get_budget(month)


@app.get("/scores", response_model=ScoresResponse)
async def get_scores():
    stats = db.get_skill_stats()
    # Wrap into ScoresResponse — extra='allow' preserves the 'skills' dict.
    return ScoresResponse(total_scored=len(stats), skills=stats)


@app.post("/pulse", response_model=PulseResponse)
async def trigger_pulse(request: Request = None):
    """Manually trigger a heartbeat pulse."""
    # License guard on execution (was ORPHAN — no enforcement)
    if hasattr(app.state, 'license_valid') and not app.state.license_valid:
        # Surfaced as a non-200 via HTTPException so the Pydantic envelope stays sane
        raise HTTPException(402, "License expired or invalid. Activate VIP key.")
    await scheduler._pulse()
    scheduler.pulse_count += 1
    scheduler.last_pulse = datetime.now(UTC).isoformat()
    return PulseResponse(pulse=scheduler.pulse_count, status="executed")


@app.get("/chains")
async def list_chains():
    """List available chains — now via chain_graph directly (Onda 3 #3)."""
    from cognitive.chain_graph import list_chains as _list_chains
    return _list_chains()


@app.post("/chains/{chain_name}/start")
async def start_chain(chain_name: str, project: str = "", context: str = ""):
    """Initialise a chain run via the chain_graph durable runtime (Onda 5 #2).

    Each step is dispatched to an executor callable that records the
    invocation but defers actual LLM execution to the caller (autopilot
    receives the run_id and runs each skill via its existing path). The
    chain_graph SqliteSaver persists state across crashes — same contract
    that chain_executor.py provided, now backed by LangGraph primitives.
    """
    from datetime import datetime

    from cognitive.chain_graph import ChainGraph, load_chain_def

    chain_def = load_chain_def(chain_name)
    if chain_def is None:
        raise HTTPException(404, f"Chain '{chain_name}' not found")

    # Lightweight executor: records the step + returns a placeholder artifact.
    # Real per-step LLM execution is dispatched separately by the autopilot
    # (which already owns the model_router + budget enforcement path).
    def deferred_executor(skill: str, step_def: dict, state) -> dict:
        return {
            "skill": skill,
            "status": "queued",
            "_score": 0,
            "queued_at": datetime.now(UTC).isoformat(),
        }

    graph = ChainGraph(
        chain_name=chain_name,
        chain_def=chain_def,
        executor=deferred_executor,
    )
    thread_id = f"chain_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    final = graph.invoke(project=project, context=context, thread_id=thread_id)
    return {
        "run_id": thread_id,
        "chain": chain_name,
        "status": final.get("status", "queued"),
        "total_steps": final.get("total_steps", 0),
        "current_step": final.get("current_step", 0),
        "artifacts_queued": list(final.get("artifacts", {}).keys()),
    }


# ─── #15: Real-Time SSE Event Stream ─────────────────────────────────────────

from fastapi.responses import StreamingResponse

# SSE Streaming — now uses full EventBus (was ORPHAN inline version)
try:
    from streaming.sse_streaming import get_bus, stream_task_events
    _sse_bus = get_bus()
    log.info("[SSE] EventBus active (was inline orphan)")
except ImportError:
    _sse_bus = None
    log.warning("[SSE] sse_streaming.py not available")


@app.get("/events")
async def sse_stream(task_id: str = "", modes: str = "updates,scores"):
    """Server-Sent Events stream with filtering (upgraded from inline to full EventBus)."""
    if not _sse_bus:
        return {"error": "SSE not available"}
    mode_list = [m.strip() for m in modes.split(",")]
    return StreamingResponse(
        stream_task_events(_sse_bus, task_id, mode_list),
        media_type="text/event-stream"
    )


@app.get("/events/history/{task_id}")
async def sse_history(task_id: str, limit: int = 50):
    """Get recent events for a task (new endpoint)."""
    if not _sse_bus:
        return []
    return _sse_bus.get_history(task_id, limit)


@app.get("/events/stats", response_model=EventStatsResponse)
async def sse_stats():
    """SSE bus statistics (new endpoint)."""
    if not _sse_bus:
        return EventStatsResponse()
    return _sse_bus.stats()


# Override task endpoints to emit SSE events
_orig_complete = complete_task
@app.post("/tasks/{task_id}/complete", response_model=None)
async def complete_task_with_event(task_id: str, req: TaskComplete):
    result = await _orig_complete(task_id, req)
    if _sse_bus:
        _sse_bus.emit(task_id, "task_complete", {"score": req.score})
    return result


# ─── #16: Skill Composer API ─────────────────────────────────────────────────

class ComposeRequest(BaseModel):
    name: str
    description: str = ""
    steps: list  # [{"skill": "X", "parallel": False, "condition": None}, ...]
    estimated_tokens: int = 0
    quality_gate: str = "score >= 70"


@app.post("/chains/compose")
async def compose_chain(req: ComposeRequest):
    """Dynamically compose a skill chain. Validates schemas and saves."""
    # Onda 5 #2: DEFAULT_SCHEMAS now lives in chain_schemas.py (extracted).
    # build_execution_plan lives in chain_graph (Onda 3 #3).
    from cognitive.chain_graph import build_execution_plan
    from execution.chain_schemas import DEFAULT_SCHEMAS

    # Validate all skills have schemas
    validated = []
    warnings = []
    for step in req.steps:
        skill = step.get("skill", "")
        has_schema = skill in DEFAULT_SCHEMAS
        validated.append({**step, "schema_valid": has_schema})
        if not has_schema:
            warnings.append(f"'{skill}' has no artifact schema — outputs won't be validated")

    # Build chain definition
    chain_def = {
        "name": req.name,
        "description": req.description,
        "trigger_keywords": [],
        "steps": [{
            "skill": s.get("skill"),
            "parallel": s.get("parallel", False),
            "condition": s.get("condition"),
            "receives": s.get("receives", "output from previous"),
            "produces": s.get("produces", "structured output"),
            "pass_to_next": s.get("pass_to_next", []),
        } for s in req.steps],
        "estimated_tokens": req.estimated_tokens,
        "quality_gate": req.quality_gate,
    }

    plan = build_execution_plan(chain_def)

    return {
        "chain_name": req.name,
        "steps": len(req.steps),
        "waves": len(plan),
        "schemas_valid": sum(1 for s in validated if s["schema_valid"]),
        "warnings": warnings,
        "plan": plan,
        "chain_def": chain_def,
    }


# ─── #17: Smart Context Window ──────────────────────────────────────────────

@app.get("/context/{task_id}")
async def get_smart_context(task_id: str, token_budget: int = 4000):
    """Get relevance-ranked context for a task, trimmed to token budget."""
    result = _run_engine("context_injector.py", ["--task", task_id, "--json"])

    if not isinstance(result, dict) or "sections" not in result:
        return result

    # Rank by priority and trim to budget
    priority_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    sections = sorted(result.get("sections", []),
                      key=lambda s: priority_rank.get(s.get("priority", "low"), 3))

    trimmed = []
    tokens_used = 0
    for section in sections:
        content = section.get("content", "")
        section_tokens = len(content) // 4
        if tokens_used + section_tokens <= token_budget:
            trimmed.append(section)
            tokens_used += section_tokens
        else:
            # Partial include: trim content to fit remaining budget
            remaining = (token_budget - tokens_used) * 4
            if remaining > 100:
                section["content"] = content[:remaining] + "... [trimmed]"
                section["trimmed"] = True
                trimmed.append(section)
                tokens_used = token_budget
            break

    return {
        "task_id": task_id,
        "token_budget": token_budget,
        "tokens_used": tokens_used,
        "sections_included": len(trimmed),
        "sections_total": len(result.get("sections", [])),
        "sections": trimmed,
    }


# ─── #18: Webhook Integrations ──────────────────────────────────────────────

import urllib.request

WEBHOOKS_FILE = ORCH_DIR / "webhooks.yaml"


def load_webhooks() -> dict:
    if not WEBHOOKS_FILE.exists():
        return {"hooks": []}
    try:
        import yaml as _yaml
        with open(WEBHOOKS_FILE, encoding="utf-8") as f:
            return _yaml.safe_load(f) or {"hooks": []}
    except Exception:
        return {"hooks": []}


async def fire_webhooks(event_type: str, payload: dict):
    """Send outbound webhook for an event."""
    config = load_webhooks()
    for hook in config.get("hooks", []):
        if event_type in hook.get("events", []) or "*" in hook.get("events", []):
            url = hook.get("url", "")
            if not url:
                continue
            try:
                data = json.dumps({"event": event_type, "payload": payload, "source": "dario-runtime"}).encode()
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(req, timeout=5)
            except Exception as e:
                log.warning(f"Webhook failed ({url}): {e}")


@app.get("/webhooks", response_model=WebhookListResponse)
async def list_webhooks():
    hooks = load_webhooks() or []
    if isinstance(hooks, dict):
        hooks = list(hooks.values())
    return WebhookListResponse(count=len(hooks), webhooks=hooks)


@app.post("/webhooks/test", response_model=WebhookTestResponse)
async def test_webhook(url: str, event: str = "test"):
    """Fire a test webhook."""
    try:
        await fire_webhooks(event, {"test": True, "url": url})
        return WebhookTestResponse(ok=True, url=url, status_code=200)
    except Exception as e:
        return WebhookTestResponse(ok=False, url=url, status_code=0, error=str(e)[:200])


# ─── #20: Visual DAG Dashboard ──────────────────────────────────────────────

from fastapi.responses import HTMLResponse


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """NASA Mission Control dashboard — serves dashboard.html with live API data."""
    dashboard_file = ORCH_DIR / "dashboard.html"
    if dashboard_file.exists():
        return HTMLResponse(content=dashboard_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Dashboard file not found. Run: python db.py --init</h1>", status_code=404)


@app.get("/dashboard/agents", response_class=HTMLResponse)
async def dashboard_agents():
    """Live Agent Operations Center — real-time execution display."""
    agent_file = ORCH_DIR / "agent_display.html"
    if agent_file.exists():
        return HTMLResponse(content=agent_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Agent display file not found.</h1>", status_code=404)


@app.get("/dashboard/data")
async def dashboard_data():
    """Full DAG data for dashboard consumption."""
    tasks = db.get_tasks()
    counts = db.get_task_counts()
    audit = db.get_audit(limit=50)
    scores = db.get_skill_stats()
    budget = db.get_budget()
    return {
        "tasks": tasks,
        "counts": counts,
        "audit": audit,
        "scores": scores,
        "budget": budget,
        "timestamp": datetime.now(UTC).isoformat(),
    }


# ─── Templates API ───────────────────────────────────────────────────────────

@app.get("/templates", response_model=TemplateListResponse)
async def list_templates():
    result = _run_engine("task_templates.py", ["--list", "--json"])
    if isinstance(result, list):
        return TemplateListResponse(count=len(result), templates=result)
    return result


@app.post("/templates/{name}/instantiate", response_model=TemplateInstantiateResponse)
async def instantiate_template(name: str, variables: dict = {}, create: bool = False):
    args = ["--template", name, "--vars", json.dumps(variables)]
    if create:
        args.append("--create")
    args.append("--json")
    result = _run_engine("task_templates.py", args)
    return result


# ─── Adaptive Rubric API ────────────────────────────────────────────────────

@app.get("/rubric/{task_id}", response_model=RubricResponse)
async def get_rubric(task_id: str):
    result = _run_engine("quality/adaptive_rubric.py", ["--task", task_id, "--json"])
    if "task_id" not in result:
        result["task_id"] = task_id
    return result


# ─── Core Upgrades v11.0 ────────────────────────────────────────────────────

try:
    from upgrades.core import init_core_upgrades
    init_core_upgrades(app, db)
    log.info("Core Upgrades v11.0 loaded: TaskQueue + MessageBus + EngineRegistry + HandoffProtocol + CheckpointStore + DurableDecorators + SessionManager")
except ImportError as e:
    log.warning(f"Core Upgrades not loaded: {e}")

try:
    from upgrades.execution import init_execution_upgrades
    init_execution_upgrades(app)
    log.info("Execution Upgrades v11.0 loaded: ParallelAgent + AgentCards + DualOrchestrator + TeamCoordinator + Blackboard + AgentToolbox + RaceExecutor + WaveScheduler")
except ImportError as e:
    log.warning(f"Execution Upgrades not loaded: {e}")

try:
    from upgrades.intelligence import init_intelligence_upgrades
    init_intelligence_upgrades(app)
    log.info("Intelligence Upgrades v11.0 loaded: TieredMemory + QValueMemory + KnowledgeGraph + LearnedRouter + ToolMemory + BenchmarkEvolution + MetricsRegistry")
except ImportError as e:
    log.warning(f"Intelligence Upgrades not loaded: {e}")

try:
    from upgrades.quality import init_quality_upgrades
    init_quality_upgrades(app)
    log.info("Quality Upgrades v11.0 loaded")
except ImportError as e:
    log.warning(f"Quality Upgrades not loaded: {e}")

try:
    from upgrades.state import init_state_upgrades
    init_state_upgrades(app)
    log.info("State Upgrades v11.0 loaded")
except ImportError as e:
    log.warning(f"State Upgrades not loaded: {e}")

try:
    from upgrades.observability import init_observability_upgrades
    init_observability_upgrades(app)
    log.info("Observability Upgrades v11.0 loaded")
except ImportError as e:
    log.warning(f"Observability Upgrades not loaded: {e}")

try:
    from upgrades.security import init_security_upgrades
    init_security_upgrades(app)
    log.info("Security Upgrades v11.0 loaded")
except ImportError as e:
    log.warning(f"Security Upgrades not loaded: {e}")

try:
    from upgrades.financial import init_financial_upgrades
    init_financial_upgrades(app)
    log.info("Financial Upgrades v11.0 loaded")
except ImportError as e:
    log.warning(f"Financial Upgrades not loaded: {e}")


# ─── Production Data Connectors ────────────────────────────────────────────

@app.post("/prod/parse-bank-statement", response_model=ParsedDocumentResponse)
async def parse_bank_statement(file_path: str, bank: str = None):
    """Parse a bank statement CSV and return structured transactions."""
    args = ["--file", file_path, "--output", "json"]
    if bank:
        args.extend(["--bank", bank])
    result = _run_engine("bank_parser.py", args)
    if "parsed" not in result:
        result["parsed"] = "error" not in result
    result.setdefault("document_type", "bank_statement")
    return result


@app.post("/prod/parse-saft", response_model=ParsedDocumentResponse)
async def parse_saft(file_path: str, update: bool = False):
    """Parse a SAF-T XML and return structured invoice/customer data."""
    args = ["--file", file_path, "--json"]
    if update:
        args.append("--update")
    result = _run_engine("saft_parser.py", args)
    if "parsed" not in result:
        result["parsed"] = "error" not in result
    result.setdefault("document_type", "saft")
    return result


@app.get("/prod/tax-alerts", response_model=TaxAlertResponse)
async def tax_alerts():
    """Get current tax calendar alerts."""
    result = _run_engine("tax_calendar.py", ["--alerts", "--json"])
    if isinstance(result, list):
        return TaxAlertResponse(count=len(result), alerts=result)
    result.setdefault("count", len(result.get("alerts", [])))
    return result


@app.post("/prod/validate-pt", response_model=ValidationCheckResponse)
async def validate_pt(data: dict):
    """Validate Portuguese financial data (NIF, ATCUD, SNC, IVA, IBAN)."""
    result = _run_engine("pt_validators.py", ["--validate-all", json.dumps(data)])
    return ValidationCheckResponse(
        valid=bool(result.get("valid", False)),
        field=str(result.get("field", "")),
        value=str(result.get("value", "")),
        reason=result.get("reason"),
    )

@app.get("/prod/chain/onboarding")
async def get_onboarding_chain():
    """Get the client onboarding E2E chain definition."""
    import yaml
    chain_file = ORCH_DIR / "chains" / "client_onboarding.yaml"
    if chain_file.exists():
        with open(chain_file) as f:
            return yaml.safe_load(f)
    return {"error": "Chain not found"}

log.info("Production Data Connectors loaded: bank_parser + saft_parser + tax_alerts + pt_validators + onboarding_chain")


# ─── CFO Financial Dashboard ────────────────────────────────────────────────

@app.get("/cfo", response_class=HTMLResponse)
async def cfo_dashboard():
    """CFO Financial Dashboard — unified 360 view."""
    try:
        result = subprocess.run(
            [sys.executable, str(ORCH_DIR / "financial_dashboard.py"), "--html"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            return HTMLResponse(content=result.stdout)
    except Exception:
        pass
    # Fallback to saved file
    cfo_file = ORCH_DIR / "cfo_dashboard.html"
    if cfo_file.exists():
        return HTMLResponse(content=cfo_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>CFO Dashboard not available. Run: python financial_dashboard.py --save-html</h1>", status_code=404)


@app.get("/cfo/data")
async def cfo_data():
    """CFO data API — JSON for integrations."""
    try:
        result = subprocess.run(
            [sys.executable, str(ORCH_DIR / "financial_dashboard.py"), "--json"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e)}


# ─── TIER 3 Registration ────────────────────────────────────────────────────

try:
    from core.tier3 import register_tier3_endpoints
    register_tier3_endpoints(app)
    log.info("TIER 3 endpoints registered (10 differentiation features)")
except ImportError as e:
    log.warning(f"TIER 3 not loaded: {e}")


# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    import uvicorn

    parser = argparse.ArgumentParser(description="DARIO Runtime Engine")
    parser.add_argument("--port", type=int, default=8422)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--no-scheduler", action="store_true")
    args = parser.parse_args()

    if args.no_scheduler:
        scheduler_enabled = False

    log.info(f"DARIO Runtime v9.0 starting on {args.host}:{args.port}")
    log.info(f"Scheduler: {'enabled (30min pulse)' if not args.no_scheduler else 'disabled'}")

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

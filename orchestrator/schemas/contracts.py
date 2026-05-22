"""Central Pydantic contracts for the DARIO Orchestrator (Onda 1 #2).

Every cross-process I/O — HTTP request bodies, agent invocations, tool calls,
and tool results — should be one of these models. Untyped dicts crossing
process boundaries are the #1 silent failure mode this layer prevents.

Conventions:
    - Pydantic v2 (`model_validate`, `model_dump`).
    - Enums are str-backed so JSON serialisation is human-readable.
    - Timestamps are ISO-8601 UTC strings (matches memory.schemas).
    - `extra='forbid'` on cross-process contracts; `extra='allow'` only on
      enrichment payloads that intentionally pass through unstructured data.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _utcnow() -> str:
    return datetime.now(UTC).isoformat()


# ─── Enums ───────────────────────────────────────────────────────────────────


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(str, Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    BLOCKED = "blocked"


class ExecutionPolicy(str, Enum):
    DEFAULT = "default"
    CRITICAL = "critical"
    CLIENT_FACING = "client_facing"
    FINANCIAL = "financial"


class ExecutorType(str, Enum):
    AGENT = "agente"
    WORKER = "worker"
    HUMAN = "humano"
    CLONE = "clone"


# ─── Task contracts ──────────────────────────────────────────────────────────


class TaskCreate(BaseModel):
    """HTTP body for POST /tasks. Subset of TaskSpec required at creation."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, description="Task ID, e.g. ATR-001")
    title: str = Field(min_length=1)
    project: str = ""
    skill: str = ""
    priority: Priority = Priority.MEDIUM
    description: str = ""
    execution_policy: ExecutionPolicy = ExecutionPolicy.DEFAULT
    depends_on: list[str] = Field(default_factory=list)
    estimated_tokens: int = Field(default=0, ge=0)

    @field_validator("id")
    @classmethod
    def _id_is_uppercase_prefix(cls, v: str) -> str:
        # Must match PROJECT-NNN pattern (forgiving on the number portion)
        if "-" not in v or not v.split("-", 1)[0].isupper():
            raise ValueError(
                "Task ID must be 'PROJECT-NNN' with uppercase project prefix"
            )
        return v


class TaskComplete(BaseModel):
    """HTTP body for POST /tasks/{id}/complete."""

    model_config = ConfigDict(extra="forbid")

    score: int = Field(default=0, ge=0, le=100)
    tokens: int = Field(default=0, ge=0)
    output: str = ""
    status: TaskStatus = TaskStatus.DONE


class TaskSpec(BaseModel):
    """Full task specification (TASK-FORMAT-SPEC-V1).

    Used by `task_spec.validate_task` to replace ad-hoc dict validation.
    `extra='allow'` because downstream skills may attach domain-specific fields
    (e.g. `inputs`, `outputs`, `methodology`) that are not part of the core
    contract but should not be rejected.
    """

    model_config = ConfigDict(extra="allow")

    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    skill: str = Field(min_length=1)
    project: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    execution_policy: ExecutionPolicy = ExecutionPolicy.DEFAULT
    executor_type: ExecutorType = ExecutorType.AGENT
    assignee: str | None = None
    depends_on: list[str] = Field(default_factory=list)
    estimated_tokens: int = Field(default=0, ge=0)
    actual_tokens: int = Field(default=0, ge=0)
    score: int = Field(default=0, ge=0, le=100)
    created_at: str = Field(default_factory=_utcnow)


# ─── Agent contracts ─────────────────────────────────────────────────────────


class AgentInput(BaseModel):
    """Input passed to an agent invocation (executor, runner, chain step)."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    skill: str
    prompt: str
    context: dict[str, Any] = Field(default_factory=dict)
    model_override: str | None = None
    max_tokens: int | None = Field(default=None, gt=0)
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    dry_run: bool = False


class AgentOutput(BaseModel):
    """Output produced by an agent invocation."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    skill: str
    success: bool
    output: str = ""
    tokens_used: int = Field(default=0, ge=0)
    duration_seconds: float = Field(default=0.0, ge=0.0)
    model_used: str | None = None
    cost_usd: float | None = Field(default=None, ge=0.0)
    error: str | None = None
    score: int | None = Field(default=None, ge=0, le=100)


# ─── Tool contracts ──────────────────────────────────────────────────────────


class ToolCall(BaseModel):
    """A single tool invocation by an agent."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)
    call_id: str | None = None
    invoked_at: str = Field(default_factory=_utcnow)


class ToolResult(BaseModel):
    """The result returned to the agent from a tool invocation."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str
    call_id: str | None = None
    success: bool
    output: Any = None
    error: str | None = None
    duration_ms: int = Field(default=0, ge=0)
    completed_at: str = Field(default_factory=_utcnow)


# ─── Validation reports ──────────────────────────────────────────────────────


class ValidationReport(BaseModel):
    """Generic validation envelope used by task_spec, guardrails, chain_validator."""

    model_config = ConfigDict(extra="forbid")

    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    spec_version: str = "TASK-FORMAT-SPEC-V1"


# ─── HTTP response envelopes (Onda 3 #4) ─────────────────────────────────────


class HealthResponse(BaseModel):
    """GET /health envelope."""

    model_config = ConfigDict(extra="allow")  # tolerate runtime-added fields

    status: str
    state: str = "?"
    autonomy: str = "?"
    health: int = 0
    timestamp: str


class TaskListResponse(BaseModel):
    """GET /tasks envelope."""

    model_config = ConfigDict(extra="forbid")

    count: int = Field(ge=0)
    tasks: list[dict[str, Any]] = Field(default_factory=list)


class AssignResponse(BaseModel):
    """POST /tasks/{id}/assign envelope."""

    model_config = ConfigDict(extra="forbid")

    assigned: bool
    task_id: str
    worker: str


class CheckoutResponse(BaseModel):
    """POST /tasks/{id}/checkout envelope."""

    model_config = ConfigDict(extra="forbid")

    checked_out: bool
    task_id: str


class CompleteResponse(BaseModel):
    """POST /tasks/{id}/complete envelope."""

    model_config = ConfigDict(extra="forbid")

    completed: bool
    task_id: str
    score: int = Field(ge=0, le=100)


class BudgetResponse(BaseModel):
    """GET /budget envelope. Mirrors the budget YAML shape."""

    model_config = ConfigDict(extra="allow")

    total_tokens_used: int = Field(default=0, ge=0)
    limit: int = Field(default=0, ge=0)
    percentage: float = Field(default=0.0, ge=0.0)


class PulseResponse(BaseModel):
    """POST /pulse envelope."""

    model_config = ConfigDict(extra="forbid")

    pulse: int = Field(ge=0)
    status: str


class DispatchResponse(BaseModel):
    """GET/POST /dispatch envelope. Returned by dispatch_engine.py --json."""

    model_config = ConfigDict(extra="allow")  # dispatch_engine adds varied fields

    dispatched: list[Any] = Field(default_factory=list)
    queued: list[Any] = Field(default_factory=list)


class StateResponse(BaseModel):
    """GET /state envelope."""

    model_config = ConfigDict(extra="allow")

    state: str = "?"
    autonomy_level: str = "?"
    system_health: int = Field(default=0, ge=0, le=100)


class AuditEntry(BaseModel):
    """A single audit row."""

    model_config = ConfigDict(extra="allow")

    timestamp: str
    actor: str = ""
    action: str = ""
    entity_type: str = ""
    entity_id: str = ""


class AuditResponse(BaseModel):
    """GET /audit envelope."""

    model_config = ConfigDict(extra="forbid")

    entries: list[AuditEntry] = Field(default_factory=list)
    count: int = Field(default=0, ge=0)


class ScoresResponse(BaseModel):
    """GET /scores envelope."""

    model_config = ConfigDict(extra="allow")

    total_scored: int = Field(default=0, ge=0)


class EventStatsResponse(BaseModel):
    """GET /events/stats envelope."""

    model_config = ConfigDict(extra="allow")

    total_events: int = Field(default=0, ge=0)
    active_subscribers: int = Field(default=0, ge=0)


class WebhookEntry(BaseModel):
    """One configured webhook target."""

    model_config = ConfigDict(extra="allow")

    name: str
    url: str = ""
    events: list[str] = Field(default_factory=list)


class WebhookListResponse(BaseModel):
    """GET /webhooks envelope."""

    model_config = ConfigDict(extra="forbid")

    count: int = Field(default=0, ge=0)
    webhooks: list[WebhookEntry] = Field(default_factory=list)


class ChainsListResponse(BaseModel):
    """GET /chains envelope (Onda 3 #3 hook)."""

    model_config = ConfigDict(extra="allow")  # chain_graph.list_chains dict shape

    # Dict keyed by chain name → metadata
    # Pydantic accepts arbitrary dict at root via extra='allow' when parent
    # uses RootModel; for backwards compat we keep dict response and validate
    # via FastAPI's response_model coercion to ChainsListResponse only if
    # consumer needs strict shape. For now leave permissive.


# ─── Templates + webhooks + prod endpoints (Onda 6 #5) ──────────────────────


class TemplateListResponse(BaseModel):
    """GET /templates envelope."""

    model_config = ConfigDict(extra="allow")

    count: int = Field(default=0, ge=0)
    templates: list[dict[str, Any]] = Field(default_factory=list)


class TemplateInstantiateResponse(BaseModel):
    """POST /templates/{name}/instantiate envelope."""

    model_config = ConfigDict(extra="allow")

    template: str
    instantiated: bool
    tasks_created: list[str] = Field(default_factory=list)


class WebhookTestResponse(BaseModel):
    """POST /webhooks/test envelope."""

    model_config = ConfigDict(extra="forbid")

    ok: bool
    url: str
    status_code: int = Field(default=0, ge=0)
    error: str | None = None


class ChainComposeResponse(BaseModel):
    """POST /chains/compose envelope."""

    model_config = ConfigDict(extra="allow")

    name: str
    composed: bool
    total_steps: int = Field(default=0, ge=0)
    warnings: list[str] = Field(default_factory=list)


class ParsedDocumentResponse(BaseModel):
    """Generic envelope for POST /prod/parse-* endpoints."""

    model_config = ConfigDict(extra="allow")

    parsed: bool
    document_type: str = ""
    records: list[dict[str, Any]] = Field(default_factory=list)
    error: str | None = None


class ValidationCheckResponse(BaseModel):
    """POST /prod/validate-pt envelope."""

    model_config = ConfigDict(extra="forbid")

    valid: bool
    field: str
    value: str
    reason: str | None = None


class TaxAlertResponse(BaseModel):
    """GET /prod/tax-alerts envelope."""

    model_config = ConfigDict(extra="allow")

    count: int = Field(default=0, ge=0)
    alerts: list[dict[str, Any]] = Field(default_factory=list)


class OnboardingChainResponse(BaseModel):
    """GET /prod/chain/onboarding envelope."""

    model_config = ConfigDict(extra="allow")

    chain: str = "onboarding"
    steps: list[dict[str, Any]] = Field(default_factory=list)


class RubricResponse(BaseModel):
    """GET /rubric/{task_id} envelope."""

    model_config = ConfigDict(extra="allow")

    task_id: str
    skill: str = ""
    dimensions: list[dict[str, Any]] = Field(default_factory=list)
    pass_threshold: int = Field(default=70, ge=0, le=100)

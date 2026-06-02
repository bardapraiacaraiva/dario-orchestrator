"""
DARIO Memory Schemas — Pydantic models for all memory types.
Inspired by Anthropic "Memory and Dreaming for Self-Learning Agents" (Code w/ Claude 2026).
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


def utcnow() -> str:
    return datetime.now(UTC).isoformat()


class Outcome(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    REVISION = "revision"
    BLOCKED = "blocked"


class MemoryLayer(str, Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    CACHE = "cache"


class RetrievedMemory(BaseModel):
    memory_id: str
    layer: MemoryLayer
    relevance: str = "medium"
    used_in_output: bool = False


class Correction(BaseModel):
    timestamp: str = Field(default_factory=utcnow)
    user_input: str
    delta: str = ""
    severity: str = "low"


class FailedToolCall(BaseModel):
    tool: str
    error: str
    retry_count: int = 0


class Episode(BaseModel):
    episode_id: str
    task_id: str | None = None
    timestamp: str = Field(default_factory=utcnow)
    agent: str = "dario-ceo"
    skill: str = ""
    outcome: Outcome = Outcome.SUCCESS
    duration_seconds: float = 0.0
    score: int | None = None
    corrections: list[Correction] = Field(default_factory=list)
    failed_tool_calls: list[FailedToolCall] = Field(default_factory=list)
    retrieved_memories: list[RetrievedMemory] = Field(default_factory=list)
    tokens_used: int = 0
    model: str = ""
    output_summary: str = ""
    project: str = ""
    tags: list[str] = Field(default_factory=list)


class SemanticMemory(BaseModel):
    memory_id: str
    name: str
    description: str = ""
    type: str = "project"
    content: str = ""
    created_at: str = Field(default_factory=utcnow)
    updated_at: str = Field(default_factory=utcnow)
    retrieval_count: int = 0
    last_retrieved: str | None = None
    promoted_from_episodes: list[str] = Field(default_factory=list)
    confidence: float = 0.7
    links: list[str] = Field(default_factory=list)


class ProceduralWorkflow(BaseModel):
    # extra="allow" preserves the convergence schema (steps[], convergence_evidence{},
    # confidence, client_validated, …) on load/round-trip. Without it, record_usage()'s
    # read→write cycle would silently erase those fields the first time a convergence
    # workflow is used.
    model_config = ConfigDict(extra="allow")

    workflow_id: str
    name: str
    discovered_from: str = "convergence"
    sessions_observed: int = 1
    skills_sequence: list[str] = Field(default_factory=list)
    avg_score: float = 0.0
    avg_duration_seconds: float = 0.0
    applicable_when: str = ""
    project_hints: list[str] = Field(default_factory=list)
    promoted_at: str = Field(default_factory=utcnow)
    last_used: str | None = None
    use_count: int = 0
    success_rate: float = 0.0

    @model_validator(mode="before")
    @classmethod
    def _unify_convergence_schema(cls, data):
        """Materialize the legacy dispatch fields from the convergence schema.

        Convergence-discovered workflows store their chain under `steps[]` and their
        evidence under `convergence_evidence{}`. Dispatch matching (find_applicable,
        detect_completed) reads `skills_sequence` / `project_hints` / `avg_score`, so
        derive those here when the legacy fields are empty. Existing values win — once
        materialized (and re-saved), this is a no-op.
        """
        if not isinstance(data, dict):
            return data
        steps = data.get("steps") or []
        ce = data.get("convergence_evidence") or {}
        if not data.get("skills_sequence") and steps:
            seq = [s.get("skill") for s in steps
                   if isinstance(s, dict) and s.get("skill")]
            if seq:
                data["skills_sequence"] = seq
        if not data.get("project_hints") and ce.get("projects"):
            data["project_hints"] = list(ce["projects"])
        if not data.get("avg_score") and ce.get("avg_score"):
            data["avg_score"] = ce["avg_score"]
        if not data.get("sessions_observed") and ce.get("runs"):
            data["sessions_observed"] = ce["runs"]
        return data


class CacheEntry(BaseModel):
    cache_id: str
    key_hash: str
    skill: str
    input_summary: str = ""
    output: str
    created_at: str = Field(default_factory=utcnow)
    expires_at: str = ""
    hit_count: int = 0
    tokens_saved: int = 0


class RetrievalLogEntry(BaseModel):
    timestamp: str = Field(default_factory=utcnow)
    episode_id: str
    memory_id: str
    layer: MemoryLayer
    relevance: str = "medium"


class PhaseReport(BaseModel):
    name: str
    duration_seconds: float = 0.0
    actions: list[str] = Field(default_factory=list)
    counts: dict[str, int] = Field(default_factory=dict)


class DreamReport(BaseModel):
    dream_id: str
    started_at: str = Field(default_factory=utcnow)
    finished_at: str = ""
    duration_seconds: float = 0.0
    agent: str = "dario-ceo"
    window_days: int = 7
    episodes_processed: int = 0
    memories_before: int = 0
    memories_after: int = 0
    tokens_saved_estimate: int = 0
    phase_1_orient: PhaseReport | None = None
    phase_2_prune: PhaseReport | None = None
    phase_3_merge: PhaseReport | None = None
    phase_4_reorganize: PhaseReport | None = None
    patterns_detected: list[str] = Field(default_factory=list)
    convergent_workflows: list[str] = Field(default_factory=list)
    promotions: dict[str, int] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


def to_yaml_safe(model: BaseModel) -> dict[str, Any]:
    dumped: dict[str, Any] = model.model_dump(mode="json", exclude_none=True)
    return dumped

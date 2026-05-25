"""Engine Registry (extracted from `upgrades/core.py` — Onda 7 #1).

Composio-inspired pluggable engine catalog. Engines register their spec
(name, path, category, health check); registry can list, look up by name,
and run health checks across all of them.

Parent `upgrades/core.py` re-imports these for backward-compat.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path(os.path.expanduser("~/.claude/orchestrator"))

log = logging.getLogger("upgrades.core_engines")


@dataclass
class EngineSpec:
    """Specification for a registered engine."""

    name: str
    path: str
    description: str
    version: str = "1.0"
    category: str = "core"
    health_check: Callable | None = None
    input_schema: dict = field(default_factory=dict)
    output_schema: dict = field(default_factory=dict)
    dependencies: list[str] = field(default_factory=list)
    status: str = "active"  # active | degraded | disabled
    last_health: str | None = None


class EngineRegistry:
    """Pluggable engine registry inspired by Composio's 8-slot architecture.

    Each engine has a defined interface contract and health check.
    """

    def __init__(self):
        self._engines: dict[str, EngineSpec] = {}
        self._categories: dict[str, list[str]] = {}

    def register(self, spec: EngineSpec):
        """Register an engine with its specification."""
        self._engines[spec.name] = spec
        cat = spec.category
        if cat not in self._categories:
            self._categories[cat] = []
        if spec.name not in self._categories[cat]:
            self._categories[cat].append(spec.name)
        log.debug(f"Engine registered: {spec.name} ({spec.category})")

    def get(self, name: str) -> EngineSpec | None:
        """Get engine spec by name."""
        return self._engines.get(name)

    def list_engines(self, category: str | None = None) -> list[EngineSpec]:
        """List all engines, optionally filtered by category."""
        if category:
            names = self._categories.get(category, [])
            return [self._engines[n] for n in names if n in self._engines]
        return list(self._engines.values())

    def health_check_all(self) -> dict:
        """Run health checks on all registered engines."""
        results: dict = {}
        for name, spec in self._engines.items():
            if spec.health_check:
                try:
                    ok = spec.health_check()
                    spec.status = "active" if ok else "degraded"
                    spec.last_health = datetime.now(UTC).isoformat()
                    results[name] = {"status": spec.status, "checked": spec.last_health}
                except Exception as e:
                    spec.status = "degraded"
                    results[name] = {"status": "error", "error": str(e)}
            else:
                if os.path.exists(spec.path):
                    results[name] = {"status": "active", "checked": "file_exists"}
                else:
                    spec.status = "disabled"
                    results[name] = {"status": "missing", "path": spec.path}
        return results

    def auto_discover(self, directory: str | None = None):
        """Auto-discover engines from Python files in orchestrator dir."""
        scan_dir = Path(directory) if directory else ORCH_DIR
        engine_categories = {
            "runtime": "core", "db": "core", "session_boot": "core",
            "executor": "execution", "api_executor": "execution",
            "dispatch_engine": "execution", "chain_executor": "execution",
            "hierarchical_process": "execution", "workflow_graph": "execution",
            "filter_pipeline": "execution", "reactive_subscriptions": "execution",
            "evolution_runner": "intelligence", "adaptive_rubric": "intelligence",
            "context_injector": "intelligence", "memory_blocks": "intelligence",
            "model_router": "intelligence", "predictor": "intelligence",
            "llm_judge": "intelligence", "llm_evaluators": "intelligence",
            "quality_scorer": "quality", "eval_suite": "quality",
            "artifact_schemas": "quality", "output_guardrails": "quality",
            "guardrails": "quality",
            "financial_dashboard": "financial", "tax_calendar": "financial",
            "pt_validators": "financial", "budget_tracker": "financial",
            "token_meter": "financial",
            "state_machine": "state", "autodiag_runner": "state",
            "termination": "state", "checkpoint_interrupt": "state",
            "error_handlers": "state", "replanner": "state",
            "suspend_resume": "state",
            "span_tracer": "observability", "tracer": "observability",
            "audit_logger": "observability", "sse_streaming": "observability",
            "lifecycle_hooks": "observability",
            "auth": "security", "approval_gates": "security",
            "filelock": "security", "license_manager": "security",
        }

        for py_file in scan_dir.glob("*.py"):
            stem = py_file.stem
            if stem.startswith("_") or stem == "core_upgrades":
                continue
            if stem in self._engines:
                continue

            category = engine_categories.get(stem, "utility")
            with open(py_file, encoding="utf-8", errors="ignore") as f:
                lines = sum(1 for _ in f)

            self.register(
                EngineSpec(
                    name=stem,
                    path=str(py_file),
                    description=f"Auto-discovered: {stem}.py ({lines} lines)",
                    category=category,
                    version="auto",
                )
            )


__all__ = ["EngineSpec", "EngineRegistry"]

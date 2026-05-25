"""Dispatch validator (Risk #1 thin layer module 2/3).

Before this module, "validate task against company.yaml rules before
dispatching" was Claude's job from SKILL.md. Now: any caller invoking
`validate_task_or_raise(task)` actually fails when schema invalid.

Validates:
  1. Required fields present (id, skill OR assignee/worker)
  2. id follows CLIENT-NNN convention (configurable strictness)
  3. execution_policy in known enum
  4. If assignee given: worker exists in company.yaml
  5. If skill given: skill directory exists under ~/.claude/skills/
  6. If execution_policy in {client_facing, critical, financial}: worker
     has skill_client_facing field (per dispatch routing post Padrão A)
  7. For Tier 2 workers (requires_briefing_validation=true), the
     task.briefing must pass the briefing validator

Designed for cheap pre-dispatch checks. Each validation is O(1) or
O(small constant).
"""

from __future__ import annotations

import logging
import re
from typing import Any
from pathlib import Path

import yaml

from enforcement import TaskValidationError

log = logging.getLogger("enforcement.dispatch_validator")

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SKILLS_DIR = Path.home() / ".claude" / "skills"
COMPANY_YAML = ORCH_DIR / "company.yaml"

VALID_EXECUTION_POLICIES = {"default", "client_facing", "critical", "financial"}

# Task ID convention: <PROJECT_SLUG_UPPER>-<NNN> per CONVENTIONS.md
TASK_ID_RE = re.compile(r"^[A-Z][A-Z0-9_]{1,30}-\d{1,5}$")


_workers_cache: dict[str, Any] | None = None
_workers_cache_mtime: float = 0.0


def _load_workers() -> dict[str, Any]:
    """Load workers section from company.yaml. Cached by mtime."""
    global _workers_cache, _workers_cache_mtime
    if not COMPANY_YAML.exists():
        return {}
    mtime = COMPANY_YAML.stat().st_mtime
    if _workers_cache is not None and mtime == _workers_cache_mtime:
        return _workers_cache
    try:
        data = yaml.safe_load(COMPANY_YAML.read_text(encoding="utf-8")) or {}
        _workers_cache = data.get("workers") or {}
        _workers_cache_mtime = mtime
        return _workers_cache
    except (OSError, yaml.YAMLError) as e:
        log.error(f"Failed to load company.yaml: {e}")
        return {}


def _skill_exists(skill: str) -> bool:
    return (SKILLS_DIR / skill / "SKILL.md").is_file()


def validate_task(task: Any, strict_id: bool = False) -> dict[str, Any]:
    """Validate a task dict. Returns {valid, errors, warnings, resolved_skill}.

    Non-raising — caller decides what to do with the result.
    For raising variant, use `validate_task_or_raise()`.
    """
    errors: list[str] = []
    warnings: list[str] = []
    resolved_skill: str | None = None

    # Runtime guard against callers that bypass the type annotation.
    if not isinstance(task, dict):
        return {
            "valid": False,
            "errors": [f"task must be dict, got {type(task).__name__}"],
            "warnings": [],
            "resolved_skill": None,
        }

    # ─── Required fields ──────────────────────────────────────────────
    task_id = (task.get("id") or "").strip()
    if not task_id:
        errors.append("Missing required field: id")

    # Skill resolution: explicit `skill`, OR via worker→skill mapping
    explicit_skill = (task.get("skill") or "").strip()
    assignee = (task.get("assignee") or "").strip()
    execution_policy = (task.get("execution_policy") or "default").strip()

    if execution_policy not in VALID_EXECUTION_POLICIES:
        errors.append(
            f"Invalid execution_policy: {execution_policy!r}. "
            f"Must be one of {sorted(VALID_EXECUTION_POLICIES)}"
        )

    if not explicit_skill and not assignee:
        errors.append("Task must specify either 'skill' or 'assignee'")

    # ─── ID convention ────────────────────────────────────────────────
    if task_id:
        if not TASK_ID_RE.match(task_id):
            msg = (
                f"Task id {task_id!r} doesn't match convention "
                "<PROJECT_SLUG_UPPER>-NNN (e.g. CUIDAI-001)"
            )
            if strict_id:
                errors.append(msg)
            else:
                warnings.append(msg)

    # ─── Worker / skill resolution ────────────────────────────────────
    workers = _load_workers()
    worker_def = None
    if assignee:
        worker_def = workers.get(assignee)
        if not worker_def:
            errors.append(
                f"Assignee {assignee!r} not found in company.yaml workers"
            )

    if not errors:  # only resolve skill if no fatal errors so far
        # Apply dispatch routing per company.yaml skill_client_facing
        if worker_def and execution_policy in {"client_facing", "critical", "financial"}:
            polished = worker_def.get("skill_client_facing")
            if polished:
                # Tier 2 worker: requires briefing validation
                if worker_def.get("requires_briefing_validation"):
                    briefing = (task.get("briefing") or "").strip()
                    if not briefing or len(briefing) < 50:
                        errors.append(
                            f"Tier 2 worker {assignee} requires non-empty briefing "
                            f"(>=50 chars) for {execution_policy} execution. "
                            "Use scripts.padrao_a_briefing_validator to verify content."
                        )
                resolved_skill = polished
            else:
                resolved_skill = worker_def.get("skill")
        elif worker_def:
            resolved_skill = worker_def.get("skill")
        else:
            resolved_skill = explicit_skill

    # ─── Skill existence check ────────────────────────────────────────
    if resolved_skill and not _skill_exists(resolved_skill):
        errors.append(
            f"Resolved skill {resolved_skill!r} has no SKILL.md at "
            f"~/.claude/skills/{resolved_skill}/SKILL.md"
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "resolved_skill": resolved_skill,
    }


def validate_task_or_raise(task: Any, strict_id: bool = False) -> str:
    """Validate task; raise TaskValidationError on failure.

    Returns the resolved skill name on success.
    """
    result = validate_task(task, strict_id=strict_id)
    if not result["valid"]:
        raise TaskValidationError(
            f"Task validation failed for {task.get('id', '?')!r}:\n  - " +
            "\n  - ".join(result["errors"])
        )
    if result["warnings"]:
        for w in result["warnings"]:
            log.warning(w)
    return result["resolved_skill"] or ""


def clear_cache() -> None:
    """Reset cached workers (for tests + after company.yaml hot-reload)."""
    global _workers_cache, _workers_cache_mtime
    _workers_cache = None
    _workers_cache_mtime = 0.0

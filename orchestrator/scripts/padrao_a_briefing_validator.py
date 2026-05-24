#!/usr/bin/env python3
"""Padrão A — Pre-flight briefing validator for Tier 2 polished wrappers.

Tier 2 wrappers (dario-brand-polished, dario-sales-letter-polished) are
sensitive to sparse briefings — A/B test 2026-05-24 showed they aborted
on 2 of 3 briefings each. This validator runs BEFORE dispatch to detect
missing required inputs and let the caller ask the user for clarification
instead of dispatching a wrapper that will then hit its internal gate.

Usage:
    # CLI mode (orchestrator dispatch calls this via Bash):
    python -m scripts.padrao_a_briefing_validator \\
        --worker worker-brand \\
        --briefing "Cuidaí brand positioning — caregiver SaaS BR..."

    # JSON output mode (for programmatic use):
    python -m scripts.padrao_a_briefing_validator \\
        --worker worker-sales-letter \\
        --briefing-file briefing.txt \\
        --json

Exit codes:
    0 — briefing valid, dispatch can proceed
    1 — briefing missing required inputs (see stdout for details)
    2 — worker not subject to validation (Tier 1 or non-Padrão-A worker)
    3 — error (missing config, bad input, etc.)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
VALIDATORS_CONFIG = ORCH_DIR / "config" / "padrao_a_briefing_validators.yaml"


# ─────────────────────────────────────────────────────────────────────
# Data classes
# ─────────────────────────────────────────────────────────────────────

@dataclass
class InputCheck:
    name: str
    description: str
    matched_keywords: list[str] = field(default_factory=list)
    matched_patterns: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return bool(self.matched_keywords or self.matched_patterns)


@dataclass
class ValidationResult:
    worker: str
    skill_client_facing: str | None
    is_tier_2: bool
    required_checks: list[InputCheck] = field(default_factory=list)
    optional_checks: list[InputCheck] = field(default_factory=list)
    rationale: str | None = None
    error: str | None = None

    @property
    def passed(self) -> bool:
        return self.error is None and all(c.passed for c in self.required_checks)

    @property
    def missing_required(self) -> list[InputCheck]:
        return [c for c in self.required_checks if not c.passed]

    def to_dict(self) -> dict:
        return {
            "worker": self.worker,
            "skill_client_facing": self.skill_client_facing,
            "is_tier_2": self.is_tier_2,
            "passed": self.passed,
            "rationale": self.rationale,
            "error": self.error,
            "required_inputs": [
                {
                    "name": c.name,
                    "description": c.description,
                    "passed": c.passed,
                    "matched_keywords": c.matched_keywords,
                    "matched_patterns": c.matched_patterns,
                }
                for c in self.required_checks
            ],
            "optional_inputs_present": [
                {"name": c.name, "matched_keywords": c.matched_keywords}
                for c in self.optional_checks if c.passed
            ],
            "missing_required": [
                {"name": c.name, "description": c.description}
                for c in self.missing_required
            ],
        }


# ─────────────────────────────────────────────────────────────────────
# Core validation
# ─────────────────────────────────────────────────────────────────────

def load_validators_config() -> dict:
    if not VALIDATORS_CONFIG.exists():
        raise FileNotFoundError(f"Validators config not found at {VALIDATORS_CONFIG}")
    with open(VALIDATORS_CONFIG, encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_input(briefing: str, input_def: dict, name: str) -> InputCheck:
    """Run keyword + pattern checks against the briefing for a single input."""
    briefing_lower = briefing.lower()
    check = InputCheck(name=name, description=input_def.get("description", ""))

    for kw in input_def.get("keywords", []) or []:
        if kw.lower() in briefing_lower:
            check.matched_keywords.append(kw)

    for pat in input_def.get("patterns", []) or []:
        try:
            if re.search(pat, briefing, re.IGNORECASE):
                check.matched_patterns.append(pat)
        except re.error:
            # Bad pattern in config — skip but don't fail validation
            continue

    return check


def validate_briefing(worker: str, briefing: str) -> ValidationResult:
    """Top-level entry: validate a briefing for a given worker."""
    try:
        cfg = load_validators_config()
    except FileNotFoundError as e:
        return ValidationResult(
            worker=worker, skill_client_facing=None, is_tier_2=False,
            error=str(e),
        )

    tier_1 = cfg.get("tier_1_no_validation_required") or []
    validators = cfg.get("validators") or {}

    if worker in tier_1:
        return ValidationResult(
            worker=worker, skill_client_facing=None, is_tier_2=False,
            rationale="Tier 1 worker — no pre-flight validation required",
        )

    if worker not in validators:
        return ValidationResult(
            worker=worker, skill_client_facing=None, is_tier_2=False,
            rationale="Worker not subject to Padrão A validation (not Tier 2)",
        )

    spec = validators[worker]
    result = ValidationResult(
        worker=worker,
        skill_client_facing=spec.get("skill_client_facing"),
        is_tier_2=True,
        rationale=spec.get("rationale"),
    )

    for name, defn in (spec.get("required_inputs") or {}).items():
        result.required_checks.append(check_input(briefing, defn, name))

    for name, defn in (spec.get("optional_inputs") or {}).items():
        result.optional_checks.append(check_input(briefing, defn, name))

    return result


# ─────────────────────────────────────────────────────────────────────
# Human-readable output
# ─────────────────────────────────────────────────────────────────────

def render_human(result: ValidationResult) -> str:
    if result.error:
        return f"[ERROR] {result.error}"

    if not result.is_tier_2:
        return f"[SKIP] {result.worker}: {result.rationale}"

    lines = [
        f"=== Padrão A briefing validation — {result.worker} ===",
        f"Polished skill: {result.skill_client_facing}",
        f"Why this matters: {result.rationale}",
        "",
        "Required inputs:",
    ]
    for c in result.required_checks:
        status = "OK" if c.passed else "MISSING"
        lines.append(f"  [{status}] {c.name} — {c.description}")
        if c.passed:
            evidence = c.matched_keywords[:3] + c.matched_patterns[:1]
            lines.append(f"           matched: {evidence}")

    if result.optional_checks:
        lines.append("")
        lines.append("Optional inputs (skill picks default if absent):")
        for c in result.optional_checks:
            status = "present" if c.passed else "absent"
            lines.append(f"  [{status}] {c.name}")

    lines.append("")
    if result.passed:
        lines.append("VERDICT: PASS — dispatch may proceed")
    else:
        lines.append("VERDICT: FAIL — ask user to provide:")
        for c in result.missing_required:
            lines.append(f"  - {c.name}: {c.description}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# CLI entrypoint
# ─────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="Padrão A briefing validator")
    ap.add_argument("--worker", required=True, help="Worker ID (e.g. worker-brand)")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--briefing", help="Briefing text inline")
    src.add_argument("--briefing-file", help="Path to file containing briefing text")
    ap.add_argument("--json", action="store_true", help="JSON output instead of human")
    args = ap.parse_args()

    if args.briefing_file:
        path = Path(args.briefing_file)
        if not path.is_file():
            print(f"Briefing file not found: {path}", file=sys.stderr)
            return 3
        briefing = path.read_text(encoding="utf-8")
    else:
        briefing = args.briefing

    if not briefing or not briefing.strip():
        print("Briefing is empty", file=sys.stderr)
        return 3

    result = validate_briefing(args.worker, briefing)

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_human(result))

    if result.error:
        return 3
    if not result.is_tier_2:
        return 2
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Padrão A — Telemetry recorder for polished wrapper runs.

Captures the v1/v2/final scores + metadata from a polished wrapper
execution and appends to quality/polished_production_runs.yaml.

Designed to be invoked by Claude at the end of Step 5 (RE-SCORE + OUTPUT)
inside each polished SKILL.md. Append-only — never modifies or deletes
existing entries.

Usage (called from Bash by the wrapper):
    python -m scripts.record_polished_run \\
        --skill dario-pitch-polished \\
        --v1-score 80 --v2-score 88 \\
        --final v2 \\
        --client "cuidai" \\
        --briefing-summary "Cuidaí seed pitch — caregiver SaaS BR" \\
        --gate-decision revised \\
        --status-mix "7/4/5"

Optional:
    --briefing-summary defaults to "[no summary]"
    --gate-decision: one of {revised, ship_v1, aborted}
    --status-mix: "verified/assumed/projection" counts, e.g. "7/4/5"
    --notes: free-form notes

Output: prints the appended entry as JSON to stdout (for audit trail).

Exit codes:
    0 — entry appended successfully
    1 — validation error (bad inputs)
    2 — IO error (cannot write yaml)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
RUNS_FILE = ORCH_DIR / "quality" / "polished_production_runs.yaml"


VALID_GATE_DECISIONS = {"revised", "ship_v1", "aborted"}


def _ensure_runs_file() -> dict:
    """Load existing runs or initialize a new file with header."""
    if RUNS_FILE.exists():
        with open(RUNS_FILE, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}

    data.setdefault("schema_version", 1)
    data.setdefault("description", (
        "Padrão A production runs log — append-only. "
        "Each entry: one invocation of a polished wrapper. "
        "Aggregated by scripts/aggregate_polished_metrics.py."
    ))
    data.setdefault("runs", [])
    return data


def append_run(
    skill: str,
    v1_score: int,
    v2_score: int | None,
    final: str,
    client: str,
    briefing_summary: str = "[no summary]",
    gate_decision: str = "revised",
    status_mix: str | None = None,
    notes: str | None = None,
    model_used: str = "",
) -> dict:
    """Validate + append a new run entry. Dual-write: SQLite primary + YAML mirror.

    SQLite (db.py polished_runs table, v3 schema) is the source of truth for
    queries. YAML is kept as a backward-compat mirror so legacy aggregators
    still work during the migration period. New code should use db.get_polished_runs()
    directly.
    """
    if gate_decision not in VALID_GATE_DECISIONS:
        raise ValueError(
            f"gate_decision must be one of {VALID_GATE_DECISIONS}, "
            f"got {gate_decision!r}"
        )
    if not 0 <= v1_score <= 100:
        raise ValueError(f"v1_score must be 0-100, got {v1_score}")
    if v2_score is not None and not 0 <= v2_score <= 100:
        raise ValueError(f"v2_score must be 0-100, got {v2_score}")
    if final not in {"v1", "v2", "aborted"}:
        raise ValueError(f"final must be v1/v2/aborted, got {final!r}")
    if gate_decision == "aborted" and final != "aborted":
        raise ValueError("If gate_decision=aborted, final must also be aborted")
    if gate_decision == "ship_v1" and v2_score is not None:
        raise ValueError("If gate_decision=ship_v1, v2_score must be None")

    ts = datetime.now(UTC).isoformat(timespec="seconds")
    entry = {
        "ts": ts,
        "skill": skill,
        "client": client,
        "briefing_summary": briefing_summary,
        "gate_decision": gate_decision,
        "v1_score": v1_score,
        "v2_score": v2_score,
        "final": final,
        "lift_pts": (v2_score - v1_score) if v2_score is not None else 0,
    }
    if status_mix:
        entry["status_mix"] = status_mix
    if notes:
        entry["notes"] = notes
    if model_used:
        entry["model_used"] = model_used

    # Primary write: SQLite (concurrent-safe via WAL + busy_timeout)
    try:
        from core.db import DB
        DB().record_polished_run(
            skill=skill, client=client,
            v1_score=v1_score, v2_score=v2_score,
            final=final, gate_decision=gate_decision,
            briefing_summary=briefing_summary,
            status_mix=status_mix or "",
            notes=notes or "",
            ts=ts,
            model_used=model_used,
        )
    except Exception as e:
        # Don't lose the entry if SQLite is unavailable — YAML still captures it
        print(f"[record_polished_run] SQLite write failed (non-fatal): {e}",
              file=sys.stderr)

    # Secondary write: YAML mirror for backward compat with legacy aggregators
    # TODO: deprecate once aggregate_polished_metrics reads from DB only
    data = _ensure_runs_file()
    data["runs"].append(entry)
    RUNS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RUNS_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

    return entry


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True,
                    help="Polished wrapper name (e.g. dario-pitch-polished)")
    ap.add_argument("--v1-score", type=int, required=True, help="v1 critique score 0-100")
    ap.add_argument("--v2-score", type=int, default=None,
                    help="v2 critique score 0-100 (omit if gate_decision=ship_v1 or aborted)")
    ap.add_argument("--final", required=True, choices=["v1", "v2", "aborted"],
                    help="Which version was actually delivered")
    ap.add_argument("--client", required=True, help="Client identifier (e.g. cuidai, arrecada)")
    ap.add_argument("--briefing-summary", default="[no summary]",
                    help="One-line briefing description for traceability")
    ap.add_argument("--gate-decision", default="revised",
                    choices=sorted(VALID_GATE_DECISIONS),
                    help="What the polish gate decided")
    ap.add_argument("--status-mix", default=None,
                    help="Gate 7 verified/assumed/projection counts (e.g. '7/4/5')")
    ap.add_argument("--notes", default=None, help="Free-form notes")
    ap.add_argument("--model-used", default="",
                    help="LLM model identifier (e.g. claude-opus-4-7) for drift detection")
    args = ap.parse_args()

    try:
        entry = append_run(
            skill=args.skill,
            v1_score=args.v1_score,
            v2_score=args.v2_score,
            final=args.final,
            client=args.client,
            briefing_summary=args.briefing_summary,
            gate_decision=args.gate_decision,
            status_mix=args.status_mix,
            notes=args.notes,
            model_used=args.model_used,
        )
    except ValueError as e:
        print(f"[record_polished_run] VALIDATION ERROR: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"[record_polished_run] IO ERROR: {e}", file=sys.stderr)
        return 2

    print(json.dumps(entry, ensure_ascii=False, indent=2))
    print(f"[record_polished_run] OK — appended to {RUNS_FILE}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

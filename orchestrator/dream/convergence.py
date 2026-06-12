"""Convergence detection — promote recurring skill sequences to procedural workflows.

A workflow is promoted when the same skill sequence has been observed in
>= MIN_SESSIONS distinct sessions with avg_score >= MIN_SCORE.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from memory import procedural
from memory.config import get as _cfg
from memory.schemas import ProceduralWorkflow

# Calibrated to real volume via config/memory_dream.yaml — the old hardcoded
# 3 sessions / score 70 never fired (DD finding A13, 2026-06-12).
MIN_SESSIONS = int(_cfg("convergence_min_sessions"))
MIN_SCORE = float(_cfg("convergence_min_score"))


def promote_convergent(episodes: list[Any], candidates: list[dict], dry_run: bool = False) -> list[str]:
    """For each detected convergent sequence, check quality and create/update procedural workflow."""
    by_session: dict[str, list[Any]] = defaultdict(list)
    for ep in sorted(episodes, key=lambda e: e.timestamp):
        day = ep.timestamp[:10]
        session_key = f"{ep.project or 'global'}::{day}"
        by_session[session_key].append(ep)

    promoted: list[str] = []
    existing = {wf.workflow_id for wf in procedural.list_workflows()}

    for cand in candidates:
        seq = cand["sequence"]
        sessions_used = []
        scores = []
        durations = []
        projects = set()
        for sk, eps in by_session.items():
            sk_skills = [e.skill for e in eps]
            for i in range(len(sk_skills) - len(seq) + 1):
                if sk_skills[i : i + len(seq)] == seq:
                    sessions_used.append(sk)
                    window = eps[i : i + len(seq)]
                    scores.extend([e.score for e in window if e.score is not None])
                    durations.extend([e.duration_seconds for e in window if e.duration_seconds])
                    projects.add(eps[0].project or "global")
                    break

        if len(sessions_used) < MIN_SESSIONS:
            continue
        avg_score = mean(scores) if scores else 0.0
        if avg_score < MIN_SCORE:
            continue

        wf_id = "PROC-conv_" + "_".join(s.replace("dario-", "").replace("diva-", "")[:10] for s in seq)
        if wf_id in existing:
            wf = procedural.read_workflow(wf_id)
            if wf:
                wf.sessions_observed = max(wf.sessions_observed, len(sessions_used))
                wf.avg_score = avg_score
                if not dry_run:
                    procedural.write_workflow(wf)
            continue

        wf = ProceduralWorkflow(
            workflow_id=wf_id,
            name=f"Workflow: {' → '.join(seq)}",
            discovered_from="convergence",
            sessions_observed=len(sessions_used),
            skills_sequence=seq,
            avg_score=round(avg_score, 1),
            avg_duration_seconds=round(mean(durations), 1) if durations else 0.0,
            applicable_when=f"Observed across {', '.join(sorted(projects))}",
            project_hints=list(projects),
        )
        if not dry_run:
            procedural.write_workflow(wf)
        promoted.append(wf_id)

    return promoted

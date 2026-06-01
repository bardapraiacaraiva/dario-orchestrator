"""Procedural memory — learned workflows.

Workflows are sequences of skills that produced good outcomes consistently.
They can be hand-authored (legacy skill_chains.yaml) OR discovered automatically
through convergence detection (the Dream engine).
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from .schemas import ProceduralWorkflow, utcnow

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
PROCEDURAL_DIR = ORCH_DIR / "memory" / "procedural"
PROCEDURAL_DIR.mkdir(parents=True, exist_ok=True)

LEGACY_CHAINS = ORCH_DIR / "skill_chains.yaml"


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return s[:50] or "workflow"


def write_workflow(wf: ProceduralWorkflow) -> Path:
    if not wf.workflow_id:
        wf.workflow_id = f"PROC-{_slug(wf.name)}"
    path = PROCEDURAL_DIR / f"{wf.workflow_id}.yaml"
    data = wf.model_dump(mode="json", exclude_none=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    return path


def read_workflow(workflow_id: str) -> ProceduralWorkflow | None:
    path = PROCEDURAL_DIR / f"{workflow_id}.yaml"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        loaded: ProceduralWorkflow = ProceduralWorkflow.model_validate(yaml.safe_load(f))
        return loaded


def list_workflows() -> list[ProceduralWorkflow]:
    out = []
    for path in sorted(PROCEDURAL_DIR.glob("PROC-*.yaml")):
        try:
            with open(path, encoding="utf-8") as f:
                out.append(ProceduralWorkflow.model_validate(yaml.safe_load(f)))
        except Exception:
            continue
    return out


def find_applicable(
    project: str = "",
    skill_context: list[str] | None = None,
) -> list[ProceduralWorkflow]:
    """Find workflows whose hints match the current project or initial skills."""
    skill_context = skill_context or []
    matches = []
    for wf in list_workflows():
        score = 0
        if project and any(project.lower() in h.lower() for h in wf.project_hints):
            score += 2
        if skill_context and wf.skills_sequence:
            first_skill = wf.skills_sequence[0]
            if first_skill in skill_context:
                score += 3
        if score > 0:
            matches.append((score, wf))
    matches.sort(key=lambda x: -x[0])
    return [wf for _, wf in matches]


MIN_WORKFLOW_LEN_FOR_USAGE = 2


def detect_completed(recent_skills: list[str], project: str = "") -> list[ProceduralWorkflow]:
    """Find workflows whose full skills_sequence matches the trailing portion of
    recent_skills. Used to detect "a workflow just completed" after the latest task.

    A workflow matches when its sequence equals the last len(seq) skills, and
    sequence length >= MIN_WORKFLOW_LEN_FOR_USAGE.
    """
    if not recent_skills:
        return []
    matches = []
    for wf in list_workflows():
        seq = wf.skills_sequence
        if len(seq) < MIN_WORKFLOW_LEN_FOR_USAGE or len(seq) > len(recent_skills):
            continue
        if recent_skills[-len(seq):] != seq:
            continue
        # Optional project-hint filter: if hints exist, project must match one
        if project and wf.project_hints and not any(project.lower() in h.lower() for h in wf.project_hints):
            continue
        matches.append(wf)
    return matches


def record_usage(workflow_id: str, success: bool, score: int | None = None) -> None:
    wf = read_workflow(workflow_id)
    if not wf:
        return
    wf.use_count += 1
    wf.last_used = utcnow()
    if score is not None:
        wf.avg_score = (wf.avg_score * (wf.use_count - 1) + score) / wf.use_count
    successes = int(round(wf.success_rate * (wf.use_count - 1))) + (1 if success else 0)
    wf.success_rate = successes / wf.use_count
    write_workflow(wf)


def import_legacy_chains() -> int:
    """One-time migration: turn skill_chains.yaml into procedural workflows."""
    if not LEGACY_CHAINS.exists():
        return 0
    with open(LEGACY_CHAINS, encoding="utf-8") as f:
        chains = yaml.safe_load(f) or {}
    imported = 0
    for name, spec in (chains.get("chains") or {}).items():
        steps = spec.get("steps") or []
        skills = [s.get("skill") for s in steps if isinstance(s, dict) and s.get("skill")]
        if not skills:
            continue
        wf_id = f"PROC-legacy_{_slug(name)}"
        if (PROCEDURAL_DIR / f"{wf_id}.yaml").exists():
            continue
        wf = ProceduralWorkflow(
            workflow_id=wf_id,
            name=f"Legacy chain: {name}",
            discovered_from="legacy_chains",
            sessions_observed=0,
            skills_sequence=skills,
            applicable_when=spec.get("description", ""),
            project_hints=spec.get("triggers", []) if isinstance(spec.get("triggers"), list) else [],
        )
        write_workflow(wf)
        imported += 1
    return imported


def stats() -> dict:
    items = list_workflows()
    discovered = sum(1 for w in items if w.discovered_from == "convergence")
    legacy = sum(1 for w in items if w.discovered_from == "legacy_chains")
    return {
        "total": len(items),
        "discovered_from_convergence": discovered,
        "imported_from_legacy": legacy,
        "avg_use_count": round(sum(w.use_count for w in items) / max(len(items), 1), 1),
    }


if __name__ == "__main__":
    import json
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        n = import_legacy_chains()
        print(f"Imported {n} legacy chains as procedural workflows.")
    else:
        print(json.dumps(stats(), indent=2))

#!/usr/bin/env python3
"""Dashboard data collectors — extracted from generate_dashboard.py (Onda 4).

Pure data layer: every function reads orchestrator state (DB-first, YAML
fallback) and returns plain dicts/lists. No HTML here — the renderer lives in
generate_dashboard.py. Extracted so collectors are importable/testable without
rendering 1300 lines of template.
"""

import sys
from datetime import datetime
from pathlib import Path

import yaml

HOME = Path.home()
ORCH = HOME / ".claude" / "orchestrator"
SKILLS = HOME / ".claude" / "skills"
DASHBOARD = ORCH / "dashboard.html"

# Single source of truth for the dashboard version label. Mirrors the
# orchestrator's v12.x major (license_manager.py + runtime.py reference
# v12.1 as the current line; installer is v12.3.0).
DARIO_VERSION = "v12.1"


def git_head_short() -> str:
    """Return the orchestrator repo's short commit hash, or empty if unavailable."""
    try:
        import subprocess
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=2, cwd=str(HOME / ".claude"),
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""

def load_yaml_safe(path):
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except:
        return {}

def _status_to_subdir(status):
    """Map a task status to the legacy subdir bucket the dashboard groups by."""
    if status == "done":
        return "done"
    if status == "blocked":
        return "backlog_blocked"
    return "active"  # todo, in_progress, in_review


def _iso_to_ts(value):
    """Best-effort ISO-8601 -> epoch seconds for sort; 0 if unparseable."""
    if not value:
        return 0
    try:
        from datetime import datetime as _dt
        return _dt.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0


def get_tasks():
    # DB-FIRST (2026-06-01): CONVENTIONS.md declares SQLite the source of truth.
    # The dashboard previously globbed tasks/*.yaml only, so it reported 0 tasks
    # while the engine/runtime acted on the DB (divergence fix). YAML stays as
    # fallback for environments without the DB.
    tasks = []
    try:
        if str(ORCH) not in sys.path:
            sys.path.insert(0, str(ORCH))
        from core.task_store import TaskStore
        for t in TaskStore().get_all():
            if not isinstance(t, dict):
                continue
            t.setdefault("_source_dir", _status_to_subdir(t.get("status")))
            t.setdefault("_mtime", _iso_to_ts(t.get("updated_at") or t.get("created")))
            tasks.append(t)
    except Exception:
        tasks = []

    if not tasks:
        # YAML fallback (DB unavailable or empty)
        for subdir in ("active", "backlog_blocked", "done"):
            d = ORCH / "tasks" / subdir
            if not d.exists():
                continue
            for f in d.glob("*.yaml"):
                t = load_yaml_safe(f)
                if not t or not isinstance(t, dict):
                    continue
                t.setdefault("_source_dir", subdir)
                t.setdefault("_mtime", f.stat().st_mtime)
                tasks.append(t)

    status_rank = {"in_progress": 0, "in_review": 1, "todo": 2, "blocked": 3, "done": 4}
    prio_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}

    def sort_key(t):
        s = status_rank.get(t.get("status"), 9)
        p = prio_rank.get(t.get("priority", "low"), 9)
        # Newer first within same status
        return (s, p, -t.get("_mtime", 0))

    return sorted(tasks, key=sort_key)

def get_budget():
    month = datetime.now().strftime("%Y-%m")
    path = ORCH / "budgets" / f"{month}.yaml"
    if path.exists():
        return load_yaml_safe(path)
    return {"total_tokens_used": 0, "limit": 50000000, "percentage": 0, "by_project": {}, "by_skill": {}, "by_model": {"opus": 0, "sonnet": 0, "haiku": 0}}

def get_quality():
    path = ORCH / "quality" / "skill-metrics.yaml"
    if path.exists():
        return load_yaml_safe(path)
    return {"global_avg_quality": 0, "skills": {}}

def get_pulse():
    path = ORCH / "last_pulse.yaml"
    if path.exists():
        return load_yaml_safe(path)
    return {}


def get_padrao_a_metrics():
    """Aggregate polished_production_runs.yaml on-the-fly.

    Returns dict {last_30_days: agg, all_time: agg} where each agg has
    overall + per_skill stats. Returns None if no runs file or no entries.
    """
    runs_path = ORCH / "quality" / "polished_production_runs.yaml"
    if not runs_path.exists():
        return None
    try:
        sys.path.insert(0, str(ORCH))
        from scripts.aggregate_polished_metrics import aggregate, load_runs
    except ImportError:
        return None
    runs = load_runs()
    if not runs:
        return None
    return {
        "last_30_days": aggregate(runs, window_days=30),
        "all_time": aggregate(runs, window_days=None),
        "n_runs_total": len(runs),
    }

def count_skills():
    counts = {"dario": 0, "diva": 0, "lucas": 0, "seo": 0, "a360": 0, "other": 0}
    if SKILLS.exists():
        for d in SKILLS.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists():
                name = d.name
                if name.startswith("dario"): counts["dario"] += 1
                elif name.startswith("diva"): counts["diva"] += 1
                elif name.startswith("lucas"): counts["lucas"] += 1
                elif name.startswith("seo"): counts["seo"] += 1
                elif "a360" in name: counts["a360"] += 1
                else: counts["other"] += 1
    # Count A360 sub-skills
    a360_base = SKILLS / "a360-framework-lite" / ".claude" / "skills"
    if a360_base.exists():
        for d in a360_base.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists():
                counts["a360"] += 1
    return counts

def get_company():
    path = ORCH / "company.yaml"
    if path.exists():
        data = load_yaml_safe(path)
        agents = len(data.get("agents", {}))
        workers = len(data.get("workers", {}))
        return {"agents": agents, "workers": workers, "total": agents + workers}
    return {"agents": 0, "workers": 0, "total": 0}

def status_badge(status):
    colors = {
        "todo": ("blue", "#448aff"),
        "backlog": ("dim", "#8896b3"),
        "in_progress": ("amber", "#ffab00"),
        "in_review": ("purple", "#b388ff"),
        "done": ("green", "#00e676"),
        "blocked": ("red", "#ff5252"),
    }
    c = colors.get(status, ("dim", "#8896b3"))
    return f'<span style="color:{c[1]};background:rgba({int(c[1][1:3],16)},{int(c[1][3:5],16)},{int(c[1][5:7],16)},.15);padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600;">{status}</span>'

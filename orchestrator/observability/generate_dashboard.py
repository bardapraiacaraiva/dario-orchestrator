#!/usr/bin/env python3
"""
DARIO Dashboard Generator — Reads real YAML data and generates live dashboard.
Run: python3 generate_dashboard.py
Opens: dashboard.html with real data from orchestrator files.
"""

import os
import sys
from datetime import UTC, datetime
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

def generate():
    tasks = get_tasks()
    budget = get_budget()
    quality = get_quality()
    pulse = get_pulse()
    padrao_a = get_padrao_a_metrics()
    skills = count_skills()
    company = get_company()
    total_skills = sum(skills.values())

    # Budget breakdown by project type (dev vs client)
    spend_by_type = None
    try:
        sys.path.insert(0, str(ORCH))
        from scripts.budget_breakdown_by_type import (
            aggregate_month, load_budget_file, load_types_config,
        )
        _cfg = load_types_config()
        _bm = datetime.now().strftime("%Y-%m")
        _bf = ORCH / "budgets" / f"{_bm}.yaml"
        if _bf.exists():
            spend_by_type = aggregate_month(load_budget_file(_bf), _cfg)
    except Exception:
        spend_by_type = None

    # Subagent token capture (Faixa 3 #1 — SubagentStop hook → subagent_runs/)
    subagent_capture = None
    try:
        import json as _json
        runs_dir = ORCH / "subagent_runs"
        if runs_dir.exists():
            now_month = datetime.now().strftime("%Y-%m")
            agg = {
                "all_time": {"runs": 0, "msgs": 0, "tokens": 0, "cost_usd": 0.0,
                             "attributed_runs": 0, "by_task": {}, "by_model": {}},
                "this_month": {"runs": 0, "msgs": 0, "tokens": 0, "cost_usd": 0.0},
                "last_run_ts": None,
            }
            for f in runs_dir.rglob("*.json"):
                try:
                    rec = _json.loads(f.read_text(encoding="utf-8"))
                except Exception:
                    continue
                t = rec.get("totals", {})
                agg["all_time"]["runs"] += 1
                agg["all_time"]["msgs"] += rec.get("message_count", 0)
                agg["all_time"]["tokens"] += t.get("total_tokens", 0)
                agg["all_time"]["cost_usd"] += t.get("cost_usd", 0)
                if rec.get("task_id"):
                    agg["all_time"]["attributed_runs"] += 1
                    by_t = agg["all_time"]["by_task"]
                    by_t[rec["task_id"]] = by_t.get(rec["task_id"], 0) + t.get("cost_usd", 0)
                for model, mt in t.get("by_model", {}).items():
                    by_m = agg["all_time"]["by_model"]
                    by_m[model] = by_m.get(model, 0) + mt.get("cost_usd", 0)
                if f.parent.name == now_month:
                    agg["this_month"]["runs"] += 1
                    agg["this_month"]["msgs"] += rec.get("message_count", 0)
                    agg["this_month"]["tokens"] += t.get("total_tokens", 0)
                    agg["this_month"]["cost_usd"] += t.get("cost_usd", 0)
                ts = rec.get("captured_at")
                if ts and (agg["last_run_ts"] is None or ts > agg["last_run_ts"]):
                    agg["last_run_ts"] = ts
            if agg["all_time"]["runs"] > 0:
                subagent_capture = agg
    except Exception:
        subagent_capture = None

    # Direct-script API spend (anthropic SDK calls via TrackedAnthropic wrapper)
    api_spend = None
    try:
        from scripts.aggregate_api_spend import aggregate as api_aggregate
        from scripts.aggregate_api_spend import load_entries as api_load_entries
        _entries = api_load_entries()
        if _entries:
            api_spend = {
                "last_24h": api_aggregate(_entries, window_hours=24),
                "this_month": api_aggregate(_entries, month=datetime.now().strftime("%Y-%m")),
                "all_time": api_aggregate(_entries),
            }
    except Exception:
        api_spend = None

    # Model drift events (v4 schema, Risk #10 stamp+warn)
    drift_events = None
    drift_coverage = None  # (runs_with_model, runs_total)
    try:
        import sqlite3
        from core.db import DB
        _db = DB()
        drift_events = _db.get_drift_events()
        # Coverage: how many polished_runs actually carry model_used? If 0,
        # the widget cannot honestly say "no drift" — it's a telemetry gap.
        try:
            con = sqlite3.connect(_db.db_path)
            cur = con.cursor()
            total = cur.execute("SELECT COUNT(*) FROM polished_runs").fetchone()[0]
            with_model = cur.execute(
                "SELECT COUNT(*) FROM polished_runs WHERE model_used IS NOT NULL AND model_used != ''"
            ).fetchone()[0]
            drift_coverage = (with_model, total)
            con.close()
        except Exception:
            drift_coverage = None
    except Exception:
        drift_events = None

    # Stale tasks (in_progress for >24h — schema v2 SLA breach) + top blockers
    stale_tasks = []
    blocker_tasks = []
    try:
        from datetime import timedelta
        now_utc = datetime.now(UTC)
        stale_threshold = now_utc - timedelta(hours=24)
        for t in tasks:
            status = t.get("status")
            if status == "in_progress":
                co = t.get("checked_out_at") or t.get("updated_at") or t.get("created_at")
                if co:
                    try:
                        co_dt = datetime.fromisoformat(str(co).replace("Z", "+00:00"))
                        if co_dt < stale_threshold:
                            age_h = int((now_utc - co_dt).total_seconds() // 3600)
                            stale_tasks.append({**t, "_age_h": age_h})
                    except Exception:
                        pass
            elif status == "blocked":
                ts = t.get("updated_at") or t.get("created_at")
                if ts:
                    try:
                        ts_dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                        age_h = int((now_utc - ts_dt).total_seconds() // 3600)
                        blocker_tasks.append({**t, "_age_h": age_h})
                    except Exception:
                        blocker_tasks.append({**t, "_age_h": None})
                else:
                    blocker_tasks.append({**t, "_age_h": None})
        stale_tasks.sort(key=lambda x: -x["_age_h"])
        blocker_tasks.sort(key=lambda x: -(x.get("_age_h") or 0))
    except Exception:
        stale_tasks = []
        blocker_tasks = []

    # Burn rate forecast — extrapolate current spend to end of month
    burn_forecast = None
    try:
        import calendar
        today = datetime.now()
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        day_of_month = today.day
        used = budget.get("total_tokens_used", 0)
        limit = budget.get("limit", 50000000)
        if day_of_month > 0 and limit > 0:
            daily_avg = used / day_of_month
            projected_eom = daily_avg * days_in_month
            projected_pct = (projected_eom / limit) * 100
            current_pct_local = (used / limit) * 100
            burn_forecast = {
                "daily_avg": daily_avg,
                "projected_eom_tokens": projected_eom,
                "projected_eom_pct": projected_pct,
                "current_pct": current_pct_local,
                "days_left": days_in_month - day_of_month,
                "alert": projected_pct >= 95,
                "warn": projected_pct >= 80,
            }
    except Exception:
        burn_forecast = None

    # Quality 30d sparkline data (from quality_daily.yaml, populated by cron)
    sparkline_points = []
    try:
        snap_file = ORCH / "quality" / "quality_daily.yaml"
        if snap_file.exists():
            with open(snap_file, encoding="utf-8") as f:
                snap_data = yaml.safe_load(f) or {}
            entries = snap_data.get("entries", [])
            from datetime import timedelta as _td
            cutoff = (datetime.now(UTC) - _td(days=30)).date().isoformat()
            sparkline_points = [
                {"date": e["date"], "avg": float(e.get("global_avg", 0))}
                for e in entries
                if isinstance(e, dict) and e.get("date", "") >= cutoff
                and isinstance(e.get("global_avg"), (int, float))
            ]
    except Exception:
        sparkline_points = []

    # Per-skill regression alerts — compare current avg vs baseline (>=15pt drop = alert)
    regression_alerts = []
    try:
        skills_data = (quality or {}).get("skills", {})
        if isinstance(skills_data, dict):
            for skill_name, s in skills_data.items():
                if not isinstance(s, dict):
                    continue
                cur_avg = s.get("avg") or s.get("score") or s.get("current_avg")
                baseline = s.get("baseline") or s.get("baseline_avg")
                if cur_avg is None or baseline is None:
                    continue
                try:
                    delta = float(cur_avg) - float(baseline)
                except (TypeError, ValueError):
                    continue
                if delta <= -15:
                    regression_alerts.append({
                        "skill": skill_name,
                        "current": float(cur_avg),
                        "baseline": float(baseline),
                        "delta": delta,
                    })
        regression_alerts.sort(key=lambda x: x["delta"])  # most negative first
    except Exception:
        regression_alerts = []

    # Enforcement layer state (Risk #1 thin layer)
    enforcement_state = None
    try:
        from enforcement.parallelism_guard import active_slots, _get_max_parallel
        from enforcement.budget_gate import is_budget_safe, DEFAULT_HARDSTOP_PCT
        slots = active_slots()
        enforcement_state = {
            "active_slots": len(slots),
            "max_parallel": _get_max_parallel(),
            "slot_callers": [s.get("caller", "?") for s in slots[:5]],
            "budget_safe": is_budget_safe(),
            "budget_hardstop": DEFAULT_HARDSTOP_PCT,
        }
    except Exception:
        enforcement_state = None

    pct = budget.get("percentage", 0)
    if isinstance(pct, str): pct = float(pct)
    budget_color = "green" if pct < 80 else "amber" if pct < 95 else "red"

    avg_quality = quality.get("global_avg_quality", 0) or 0

    # Delivery-ready rate — new first-class metric (Caminho B, 2026-05-23)
    # Reports % of REAL outputs the LLM judge marked "deliverable=yes"
    # (no senior review needed). Honest production-quality signal.
    delivery_yes = 0
    delivery_total = 0
    production_validated_count = 0
    for skill_name, sm in (quality.get("skills") or {}).items():
        if not isinstance(sm, dict):
            continue
        yes = sm.get("deliverable_yes_count", 0)
        n = sm.get("production_n_real_outputs", 0)
        if n:
            delivery_yes += int(yes or 0)
            delivery_total += int(n)
            production_validated_count += 1
    delivery_rate_pct = (100.0 * delivery_yes / delivery_total) if delivery_total else 0.0

    # Human review queue stats (added 2026-05-23)
    queue_pending = 0
    queue_resolved = 0
    queue_avg_ttr_min = 0
    queue_dir = ORCH / "human_review_queue"
    if queue_dir.exists():
        ttrs = []
        for meta_file in queue_dir.glob("*.meta.yaml"):
            try:
                m = load_yaml_safe(meta_file)
                state = m.get("state", "pending")
                if state == "pending":
                    queue_pending += 1
                elif state == "resolved":
                    queue_resolved += 1
                    if m.get("time_to_resolution_minutes"):
                        ttrs.append(float(m["time_to_resolution_minutes"]))
            except Exception:
                continue
        if ttrs:
            queue_avg_ttr_min = sum(ttrs) / len(ttrs)

    # Per-client stats (FASE 3, 2026-05-23)
    client_stats_path = ORCH / "quality" / "client-stats.yaml"
    top_clients = []
    if client_stats_path.exists():
        try:
            cs = load_yaml_safe(client_stats_path)
            clients = cs.get("clients", {})
            # Top by total_outputs_obsidian, excluding internal/archived
            ranked = [
                (cid, c) for cid, c in clients.items()
                if c.get("status") not in ("internal", "archived", "unknown", None)
                and c.get("total_outputs_obsidian", 0) > 0
            ]
            ranked.sort(key=lambda x: -(x[1].get("total_outputs_obsidian") or 0))
            top_clients = ranked[:6]
        except Exception:
            top_clients = []

    # Build per-client rows (structured card, like Budget Por Projecto)
    def _money_html(c):
        v = c.get("monthly_value")
        cur = c.get("currency") or ""
        if not v:
            return '<span style="color:var(--dim);font-size:11px;">—</span>'
        sym = {"EUR": "€", "BRL": "R$", "USD": "$"}.get(cur, cur)
        return f'<span style="color:var(--green);font-size:11px;font-weight:600;">{sym}{v:,}/mo</span>'

    def _status_dot(c):
        s = (c.get("status") or "").lower()
        if "blocked" in s or "pending" in s: return "dot-amber"
        return "dot-green"

    # MRR aggregates (sum monthly_value per currency, active billing only)
    mrr_by_currency: dict[str, int] = {}
    active_paying = 0
    if client_stats_path.exists():
        try:
            cs2 = load_yaml_safe(client_stats_path)
            for cid, c in (cs2.get("clients") or {}).items():
                bs = (c.get("billing_status") or "").lower()
                mv = c.get("monthly_value") or 0
                cur = (c.get("currency") or "EUR").upper()
                if bs == "active" and mv > 0:
                    mrr_by_currency[cur] = mrr_by_currency.get(cur, 0) + mv
                    active_paying += 1
        except Exception:
            pass
    mrr_pieces = []
    sym = {"EUR": "€", "BRL": "R$", "USD": "$"}
    for cur, val in sorted(mrr_by_currency.items()):
        mrr_pieces.append(f"{sym.get(cur, cur)}{val:,}")
    mrr_header = " · ".join(mrr_pieces) if mrr_pieces else "—"

    clients_html = ""
    for cid, c in top_clients[:6]:
        name = (c.get("name") or cid)[:28]
        outputs = c.get("total_outputs_obsidian", 0)
        status = (c.get("status") or "?")[:16]
        dr = c.get("delivery_ready_rate_pct")
        dr_html = f'<span style="color:var(--dim);font-size:10px;margin-left:6px;">{dr}% yes</span>' if dr is not None else ""
        clients_html += (
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid var(--border);">'
            f'<div style="flex:1;min-width:0;">'
            f'<div style="font-size:12px;font-weight:600;color:var(--text);">'
            f'<span class="dot {_status_dot(c)}" style="display:inline-block;margin-right:6px;"></span>{name}{dr_html}</div>'
            f'<div style="font-size:10px;color:var(--dim);margin-top:2px;">{status}</div>'
            f'</div>'
            f'<div style="text-align:right;margin-left:12px;">'
            f'<div style="font-size:14px;font-weight:700;color:#43a0ff;">{outputs}</div>'
            f'<div style="font-size:9px;color:var(--dim);text-transform:uppercase;">outputs</div>'
            f'</div>'
            f'<div style="text-align:right;margin-left:12px;min-width:75px;">{_money_html(c)}</div>'
            f'</div>'
        )

    # Task rows — prioritise active/blocked, fill with recent done
    task_rows = ""
    for t in tasks[:10]:
        # Age: completed_at for done, created_at otherwise, mtime as fallback
        ref_ts = t.get("completed_at") if t.get("status") == "done" else t.get("created_at")
        age = ""
        if ref_ts:
            try:
                ts = datetime.fromisoformat(str(ref_ts).replace("Z", "+00:00"))
                delta = datetime.now(UTC) - ts
                age = f"{delta.days}d" if delta.days > 0 else f"{delta.seconds//3600}h"
            except:
                age = "?"
        if not age and t.get("_mtime"):
            try:
                delta = datetime.now(UTC) - datetime.fromtimestamp(t["_mtime"], UTC)
                age = f"{delta.days}d" if delta.days > 0 else f"{delta.seconds//3600}h"
            except:
                age = "?"
        task_rows += f"""<tr>
<td style="font-weight:600;color:var(--cyan);">{t.get('id','?')}</td>
<td>{t.get('title','?')[:40]}</td>
<td>{status_badge(t.get('status','?'))}</td>
<td style="color:var(--dim);">{t.get('assignee','—') or '—'}</td>
<td>{t.get('priority','—')}</td>
<td style="color:var(--dim);">{age}</td>
</tr>"""

    if not task_rows:
        task_rows = '<tr><td colspan="6" style="text-align:center;color:var(--dim);padding:20px;">Sem tasks no taskboard</td></tr>'

    # Budget by project (top 3)
    by_proj = budget.get("by_project", {})
    proj_items = sorted(by_proj.items(), key=lambda x: -x[1])[:3]
    proj_html = "".join(f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;"><span style="color:var(--dim);font-size:12px;">{k}</span><span style="font-size:12px;">{v:,}</span></div>' for k, v in proj_items)

    # Budget by model
    by_model = budget.get("by_model", {})
    model_html = ""
    model_total = sum(by_model.values()) or 1
    for m, v in by_model.items():
        pct_m = (v / model_total) * 100
        color = {"opus": "var(--cyan)", "sonnet": "var(--purple)", "haiku": "var(--green)"}.get(m, "var(--dim)")
        model_html += f'<div style="margin-bottom:6px;"><div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px;"><span>{m}</span><span>{v:,}</span></div><div style="height:4px;background:var(--border);border-radius:2px;"><div style="height:100%;width:{pct_m:.0f}%;background:{color};border-radius:2px;"></div></div></div>'

    # Quality skills
    q_skills = quality.get("skills", {})
    q_items = sorted(q_skills.items(), key=lambda x: (x[1].get("avg_quality_score") or 0) if isinstance(x[1], dict) else 0, reverse=True)[:6]
    q_html = ""
    for name, data in q_items:
        if not isinstance(data, dict): continue
        score = data.get("avg_quality_score", 0) or 0
        tier = data.get("tier", "?")
        color = "var(--green)" if score >= 85 else "var(--amber)" if score >= 70 else "var(--red)"
        q_html += f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;"><span style="flex:1;font-size:12px;color:var(--dim);">{name}</span><div style="width:120px;height:6px;background:var(--border);border-radius:3px;"><div style="height:100%;width:{score}%;background:{color};border-radius:3px;"></div></div><span style="font-size:12px;font-weight:600;width:35px;text-align:right;">{score:.0f}</span></div>'

    tier_a = sum(1 for _, d in q_skills.items() if isinstance(d, dict) and (d.get("avg_quality_score", 0) or 0) >= 85)
    tier_b = sum(1 for _, d in q_skills.items() if isinstance(d, dict) and 70 <= (d.get("avg_quality_score", 0) or 0) < 85)
    unscored = sum(1 for _, d in q_skills.items() if isinstance(d, dict) and not d.get("avg_quality_score"))

    # Padrão A — polished wrapper telemetry widget
    if padrao_a is None:
        padrao_a_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:16px;">'
            'Sem runs registados ainda<br>'
            '<span style="font-size:10px;">Cada invocação de /dario-X-polished'
            ' adiciona uma entrada</span></div>'
        )
        padrao_a_summary = "n=0"
    else:
        agg_30 = padrao_a["last_30_days"]["overall"]
        agg_all = padrao_a["all_time"]["overall"]
        per_skill_30 = padrao_a["last_30_days"]["per_skill"]
        n_30 = agg_30["n_runs"]
        n_all = padrao_a["n_runs_total"]
        pass_30 = (agg_30["gate_pass_rate"] or 0) * 100
        lift_30 = agg_30.get("mean_lift_pts")
        lift_color = "var(--green)" if lift_30 and lift_30 >= 4 else "var(--amber)" if lift_30 and lift_30 > 0 else "var(--dim)"
        padrao_a_summary = f"n={n_all} all-time / n={n_30} last-30d"

        # Top per-skill rows
        sorted_skills = sorted(
            per_skill_30.items(),
            key=lambda kv: (kv[1].get("mean_lift_pts") or 0),
            reverse=True,
        )
        rows_html = ""
        for skill, m in sorted_skills[:6]:
            lift = m.get("mean_lift_pts")
            lift_str = f"+{lift}" if lift is not None else "—"
            pass_pct = (m.get("gate_pass_rate") or 0) * 100
            sk_color = "var(--green)" if lift is not None and lift >= 4 else "var(--amber)" if lift is not None and lift > 0 else "var(--red)"
            short_name = skill.replace("dario-", "").replace("-polished", "")
            rows_html += (
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:12px;">'
                f'<span style="flex:1;color:var(--dim);">{short_name}</span>'
                f'<span style="width:50px;text-align:right;color:var(--dim);font-size:11px;">{m["n_runs"]}r</span>'
                f'<span style="width:50px;text-align:right;color:var(--dim);font-size:11px;">{pass_pct:.0f}%</span>'
                f'<span style="width:40px;text-align:right;font-weight:600;color:{sk_color};">{lift_str}</span>'
                f'</div>'
            )

        if not rows_html:
            rows_html = '<div style="color:var(--dim);font-size:11px;text-align:center;padding:8px;">Sem runs no último 30d</div>'

        lift_display = f"+{lift_30}" if lift_30 is not None else "—"
        padrao_a_html = (
            f'<div style="display:flex;gap:20px;justify-content:center;margin-bottom:14px;">'
            f'<div style="text-align:center;">'
            f'<div class="big-num" style="color:{lift_color};font-size:1.8rem;">{lift_display}</div>'
            f'<div style="font-size:10px;color:var(--dim);">Mean lift 30d</div>'
            f'</div>'
            f'<div style="text-align:center;border-left:1px solid var(--border);padding-left:20px;">'
            f'<div class="big-num" style="font-size:1.8rem;color:var(--cyan);">{pass_30:.0f}%</div>'
            f'<div style="font-size:10px;color:var(--dim);">Gate pass 30d</div>'
            f'</div>'
            f'<div style="text-align:center;border-left:1px solid var(--border);padding-left:20px;">'
            f'<div class="big-num" style="font-size:1.8rem;">{n_30}</div>'
            f'<div style="font-size:10px;color:var(--dim);">Runs 30d</div>'
            f'</div>'
            f'</div>'
            f'<div style="font-size:10px;color:var(--dim);margin-bottom:8px;text-transform:uppercase;letter-spacing:.06em;">'
            f'Per-skill (last 30d) — runs · pass% · lift</div>'
            f'{rows_html}'
            f'<div style="font-size:10px;color:var(--dim);margin-top:10px;border-top:1px solid var(--border);padding-top:8px;">'
            f'All-time: {n_all} runs · target lift &ge; +4pts'
            f'</div>'
        )

    # Spend-by-type widget (gap #4: dev vs client visibility)
    if spend_by_type is None or spend_by_type.get("total_tokens", 0) == 0:
        spend_type_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:16px;">'
            'Sem spend tracked este mês</div>'
        )
        spend_type_summary = "n/a"
    else:
        total = spend_by_type["total_tokens"]
        by_type = spend_by_type["by_type"]
        pcts = spend_by_type["percentages_by_type"]
        client_t = by_type.get("client", 0)
        dev_t = by_type.get("dev", 0)
        unknown_t = by_type.get("unknown", 0)
        client_pct = pcts.get("client", 0)
        dev_pct = pcts.get("dev", 0)
        unknown_pct = pcts.get("unknown", 0)

        unknown_warning = ""
        if unknown_t > 0:
            unknown_warning = (
                f'<div style="font-size:11px;color:var(--amber);margin-top:8px;">'
                f'⚠ {unknown_t:,} tokens ({unknown_pct:.1f}%) sem classificação — '
                f'adicionar projeto a config/project_types.yaml'
                f'</div>'
            )

        spend_type_html = (
            f'<div style="display:flex;gap:16px;justify-content:center;margin-bottom:14px;">'
            f'<div style="text-align:center;">'
            f'<div class="big-num" style="font-size:1.8rem;color:var(--green);">{client_pct:.0f}%</div>'
            f'<div style="font-size:10px;color:var(--dim);">Client</div>'
            f'<div style="font-size:9px;color:var(--dim);">{client_t:,} tokens</div>'
            f'</div>'
            f'<div style="text-align:center;border-left:1px solid var(--border);padding-left:16px;">'
            f'<div class="big-num" style="font-size:1.8rem;color:var(--cyan);">{dev_pct:.0f}%</div>'
            f'<div style="font-size:10px;color:var(--dim);">Dev (DARIO)</div>'
            f'<div style="font-size:9px;color:var(--dim);">{dev_t:,} tokens</div>'
            f'</div>'
            f'</div>'
            f'<div style="font-size:10px;color:var(--dim);margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em;">Top 5 projetos</div>'
        )
        for row in spend_by_type["breakdown"][:5]:
            slug = (row["project"] or "<blank>")[:20]
            pct_row = row["tokens"] / total * 100 if total else 0
            type_color = {
                "client": "var(--green)",
                "dev": "var(--cyan)",
                "unknown": "var(--amber)",
            }.get(row["type"], "var(--dim)")
            spend_type_html += (
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;font-size:11px;">'
                f'<span style="flex:1;color:var(--dim);">{slug}</span>'
                f'<span style="color:{type_color};font-size:10px;width:50px;text-align:right;">{row["type"]}</span>'
                f'<span style="color:var(--dim);width:50px;text-align:right;">{pct_row:.1f}%</span>'
                f'</div>'
            )
        spend_type_html += unknown_warning
        spend_type_summary = f"client {client_pct:.0f}% · dev {dev_pct:.0f}%"

    # Direct-script API spend widget (gap #6 — visibility for scripts that
    # bypass the orchestrator's subscription path and hit the API directly)
    if api_spend is None:
        api_spend_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:16px;">'
            'Sem direct API calls registadas<br>'
            '<span style="font-size:10px;">Scripts devem usar '
            '<code>TrackedAnthropic</code> em vez de <code>Anthropic</code> '
            'para serem visíveis aqui</span></div>'
        )
        api_spend_summary = "n=0"
    else:
        s24 = api_spend["last_24h"]
        smonth = api_spend["this_month"]
        sall = api_spend["all_time"]
        usd_24h = s24["total_usd"]
        usd_month = smonth["total_usd"]
        calls_24h = s24["n_calls"]

        # Color based on 24h spend severity (informational thresholds)
        usd_color = "var(--green)" if usd_24h < 1 else \
                    "var(--amber)" if usd_24h < 10 else "var(--red)"

        api_spend_summary = f"${usd_24h:.2f} 24h · ${usd_month:.2f} mês"

        # Top callers (by month)
        callers = sorted(smonth["by_caller"].items(),
                         key=lambda kv: kv[1]["cost_usd"], reverse=True)[:5]
        callers_html = ""
        for caller, m in callers:
            caller_short = caller[:30]
            callers_html += (
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;font-size:11px;">'
                f'<span style="flex:1;color:var(--dim);">{caller_short}</span>'
                f'<span style="color:var(--dim);font-size:10px;width:40px;text-align:right;">{m["calls"]}c</span>'
                f'<span style="color:var(--text);font-weight:600;width:60px;text-align:right;">${m["cost_usd"]:.4f}</span>'
                f'</div>'
            )
        if not callers_html:
            callers_html = '<div style="color:var(--dim);font-size:11px;text-align:center;padding:8px;">Sem chamadas este mês</div>'

        api_spend_html = (
            f'<div style="display:flex;gap:16px;justify-content:center;margin-bottom:14px;">'
            f'<div style="text-align:center;">'
            f'<div class="big-num" style="font-size:1.6rem;color:{usd_color};">${usd_24h:.2f}</div>'
            f'<div style="font-size:10px;color:var(--dim);">24h spend</div>'
            f'<div style="font-size:9px;color:var(--dim);">{calls_24h} calls</div>'
            f'</div>'
            f'<div style="text-align:center;border-left:1px solid var(--border);padding-left:16px;">'
            f'<div class="big-num" style="font-size:1.6rem;color:var(--cyan);">${usd_month:.2f}</div>'
            f'<div style="font-size:10px;color:var(--dim);">Mês {datetime.now().strftime("%Y-%m")}</div>'
            f'<div style="font-size:9px;color:var(--dim);">{smonth["n_calls"]} calls</div>'
            f'</div>'
            f'<div style="text-align:center;border-left:1px solid var(--border);padding-left:16px;">'
            f'<div class="big-num" style="font-size:1.6rem;">${sall["total_usd"]:.2f}</div>'
            f'<div style="font-size:10px;color:var(--dim);">All-time</div>'
            f'<div style="font-size:9px;color:var(--dim);">{sall["n_calls"]} calls</div>'
            f'</div>'
            f'</div>'
            f'<div style="font-size:10px;color:var(--dim);margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em;">Top callers (this month) · calls · cost</div>'
            f'{callers_html}'
        )

    # Subagent token capture widget (Faixa 3 #1)
    if subagent_capture is None:
        subagent_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:16px;">'
            'Sem subagent runs capturadas<br>'
            '<span style="font-size:10px;">Hook <code>SubagentStop</code> dispara em '
            '<code>enforcement/token_capture.py</code> e escreve em '
            '<code>subagent_runs/YYYY-MM/</code></span></div>'
        )
        subagent_summary = "n=0"
    else:
        sm = subagent_capture["this_month"]
        sa = subagent_capture["all_time"]
        attribution_pct = (sa["attributed_runs"] / sa["runs"] * 100) if sa["runs"] else 0
        att_color = "var(--green)" if attribution_pct >= 70 else \
                    "var(--amber)" if attribution_pct >= 40 else "var(--red)"
        subagent_summary = f"{sa['runs']} runs · ${sa['cost_usd']:.2f}"

        top_tasks = sorted(sa["by_task"].items(), key=lambda kv: kv[1], reverse=True)[:5]
        tasks_html = ""
        for tid, cost in top_tasks:
            tasks_html += (
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;font-size:11px;">'
                f'<span style="flex:1;color:var(--cyan);font-weight:600;">{tid}</span>'
                f'<span style="color:var(--text);font-weight:600;width:70px;text-align:right;">${cost:.2f}</span>'
                f'</div>'
            )
        if not tasks_html:
            tasks_html = '<div style="color:var(--dim);font-size:11px;text-align:center;padding:8px;">Sem task IDs detectados</div>'

        models_html = ""
        for model, cost in sorted(sa["by_model"].items(), key=lambda kv: kv[1], reverse=True):
            models_html += (
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;font-size:11px;">'
                f'<span style="flex:1;color:var(--dim);">{model}</span>'
                f'<span style="color:var(--text);font-weight:600;width:70px;text-align:right;">${cost:.2f}</span>'
                f'</div>'
            )

        last_capture = subagent_capture.get("last_run_ts") or "—"
        if last_capture != "—" and len(last_capture) >= 16:
            last_capture = last_capture[:16].replace("T", " ")

        subagent_html = (
            f'<div style="display:flex;gap:16px;justify-content:center;margin-bottom:14px;">'
            f'<div style="text-align:center;">'
            f'<div class="big-num" style="font-size:1.6rem;color:var(--cyan);">${sm["cost_usd"]:.2f}</div>'
            f'<div style="font-size:10px;color:var(--dim);">Mês {datetime.now().strftime("%Y-%m")}</div>'
            f'<div style="font-size:9px;color:var(--dim);">{sm["runs"]} runs · {sm["tokens"]/1_000_000:.1f}M tok</div>'
            f'</div>'
            f'<div style="text-align:center;border-left:1px solid var(--border);padding-left:16px;">'
            f'<div class="big-num" style="font-size:1.6rem;">${sa["cost_usd"]:.2f}</div>'
            f'<div style="font-size:10px;color:var(--dim);">All-time</div>'
            f'<div style="font-size:9px;color:var(--dim);">{sa["runs"]} runs · {sa["tokens"]/1_000_000:.1f}M tok</div>'
            f'</div>'
            f'<div style="text-align:center;border-left:1px solid var(--border);padding-left:16px;">'
            f'<div class="big-num" style="font-size:1.6rem;color:{att_color};">{attribution_pct:.0f}%</div>'
            f'<div style="font-size:10px;color:var(--dim);">Attribution</div>'
            f'<div style="font-size:9px;color:var(--dim);">{sa["attributed_runs"]}/{sa["runs"]} with task_id</div>'
            f'</div>'
            f'</div>'
            f'<div style="font-size:10px;color:var(--dim);margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em;">Top tasks (all-time) · cost USD</div>'
            f'{tasks_html}'
            f'<div style="font-size:10px;color:var(--dim);margin:10px 0 6px;text-transform:uppercase;letter-spacing:.06em;">By model · cost USD</div>'
            f'{models_html}'
            f'<div style="font-size:10px;color:var(--dim);margin-top:10px;text-align:right;">Last capture: {last_capture}</div>'
        )

    # Model drift widget (Risk #10)
    n_events = 0 if drift_events is None else len(drift_events)
    with_model, total_runs = (drift_coverage or (0, 0))
    coverage_pct = (with_model / total_runs * 100) if total_runs else 0

    if n_events == 0 and total_runs > 0 and with_model == 0:
        # Telemetry gap: runs exist but none capture model_used
        drift_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:14px;">'
            '<span style="color:var(--amber);">●</span> Telemetry gap — model_used not captured<br>'
            f'<span style="font-size:10px;">0/{total_runs} polished runs carry model identifier · '
            'wrappers need to pass <code>--model-used</code> to <code>record_polished_run</code></span>'
            '</div>'
        )
        drift_summary = f"0/{total_runs} runs stamped"
    elif n_events == 0 and total_runs == 0:
        # No telemetry at all
        drift_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:14px;">'
            '<span style="color:var(--dim);">●</span> No polished runs recorded yet<br>'
            '<span style="font-size:10px;">Awaiting first <code>record_polished_run</code> call</span></div>'
        )
        drift_summary = "no data"
    elif n_events == 0:
        # Real "no drift" — coverage exists and all match
        drift_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:14px;">'
            '<span style="color:var(--green);">●</span> No drift detected<br>'
            f'<span style="font-size:10px;">{with_model}/{total_runs} runs stamped · all match declared model</span></div>'
        )
        drift_summary = f"0 events · {coverage_pct:.0f}% coverage"
    else:
        # Group by skill
        from collections import Counter as _Counter
        by_skill = _Counter(e.get("skill", "?") for e in drift_events)
        latest = drift_events[0] if drift_events else None
        rows_html = ""
        for skill, count in sorted(by_skill.items(), key=lambda x: x[1], reverse=True)[:5]:
            short = skill.replace("dario-", "").replace("-polished", "")
            rows_html += (
                f'<div style="display:flex;justify-content:space-between;'
                f'margin-bottom:4px;font-size:11px;">'
                f'<span style="color:var(--dim);">{short}</span>'
                f'<span style="color:var(--amber);font-weight:600;">{count} events</span>'
                f'</div>'
            )
        latest_html = ""
        if latest:
            latest_html = (
                f'<div style="margin-top:10px;padding-top:8px;border-top:1px solid var(--border);'
                f'font-size:10px;color:var(--dim);">'
                f'Latest: <b>{latest.get("skill","?")}</b> — '
                f'{latest.get("declared_model","?")} → {latest.get("actual_model","?")}'
                f'<br>{latest.get("ts","?")}</div>'
            )
        drift_html = (
            f'<div style="text-align:center;margin-bottom:12px;">'
            f'<div class="big-num" style="font-size:1.8rem;color:var(--amber);">{len(drift_events)}</div>'
            f'<div style="font-size:10px;color:var(--dim);">Total drift events</div>'
            f'</div>'
            f'<div style="font-size:10px;color:var(--dim);margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em;">By skill (top 5)</div>'
            f'{rows_html}'
            f'{latest_html}'
        )
        drift_summary = f"{len(drift_events)} events"

    # Enforcement layer widget (Risk #1)
    if enforcement_state is None:
        enforcement_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:14px;">'
            'Enforcement layer not available</div>'
        )
        enforcement_summary = "unavailable"
    else:
        slots_used = enforcement_state["active_slots"]
        slots_max = enforcement_state["max_parallel"]
        budget_safe = enforcement_state["budget_safe"]
        slots_color = ("var(--green)" if slots_used < slots_max
                       else "var(--red)")
        budget_color = "var(--green)" if budget_safe else "var(--red)"
        budget_label = "SAFE" if budget_safe else "BLOCKED"
        callers_html = ""
        if enforcement_state["slot_callers"]:
            callers_html = (
                '<div style="font-size:10px;color:var(--dim);margin-top:6px;">'
                'Active: ' + ", ".join(enforcement_state["slot_callers"]) +
                '</div>'
            )
        enforcement_html = (
            f'<div style="display:flex;gap:16px;justify-content:center;margin-bottom:10px;">'
            f'<div style="text-align:center;">'
            f'<div class="big-num" style="font-size:1.6rem;color:{slots_color};">'
            f'{slots_used}/{slots_max}</div>'
            f'<div style="font-size:10px;color:var(--dim);">Parallel slots</div>'
            f'</div>'
            f'<div style="text-align:center;border-left:1px solid var(--border);padding-left:16px;">'
            f'<div class="big-num" style="font-size:1.6rem;color:{budget_color};">{budget_label}</div>'
            f'<div style="font-size:10px;color:var(--dim);">Budget gate (≥{enforcement_state["budget_hardstop"]:.0f}%)</div>'
            f'</div>'
            f'</div>'
            f'{callers_html}'
        )
        enforcement_summary = f"{slots_used}/{slots_max} slots, budget {budget_label}"

    # --- Stale tasks widget ---
    if not stale_tasks:
        stale_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:14px;">'
            '<span style="color:var(--green);">●</span> No stale tasks<br>'
            '<span style="font-size:10px;">No in_progress task has been checked out >24h</span>'
            '</div>'
        )
        stale_summary = "0"
    else:
        rows_html = ""
        for t in stale_tasks[:5]:
            tid = t.get("id", "?")
            title = (t.get("title", "?") or "")[:40]
            ass = t.get("assignee", "—") or "—"
            age_h = t.get("_age_h", 0)
            rows_html += (
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:11px;">'
                f'<span style="flex:1;min-width:0;">'
                f'<span style="color:var(--cyan);font-weight:600;">{tid}</span> '
                f'<span style="color:var(--dim);">{title}</span><br>'
                f'<span style="font-size:10px;color:var(--dim);">{ass}</span></span>'
                f'<span style="color:var(--red);font-weight:600;margin-left:8px;">{age_h}h</span>'
                f'</div>'
            )
        stale_html = (
            f'<div style="text-align:center;margin-bottom:10px;">'
            f'<div class="big-num" style="font-size:1.6rem;color:var(--red);">{len(stale_tasks)}</div>'
            f'<div style="font-size:10px;color:var(--dim);">stale (>24h in_progress)</div>'
            f'</div>{rows_html}'
        )
        stale_summary = str(len(stale_tasks))

    # --- Top blockers widget ---
    if not blocker_tasks:
        blockers_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:14px;">'
            '<span style="color:var(--green);">●</span> No blocked tasks'
            '</div>'
        )
        blockers_summary = "0"
    else:
        rows_html = ""
        for t in blocker_tasks[:5]:
            tid = t.get("id", "?")
            title = (t.get("title", "?") or "")[:40]
            reason = (t.get("blocked_reason") or "—")[:50]
            age_h = t.get("_age_h")
            age_lbl = f"{age_h}h" if age_h is not None else "?"
            rows_html += (
                f'<div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:11px;">'
                f'<div style="display:flex;justify-content:space-between;">'
                f'<span><span style="color:var(--cyan);font-weight:600;">{tid}</span> '
                f'<span style="color:var(--dim);">{title}</span></span>'
                f'<span style="color:var(--amber);font-weight:600;">{age_lbl}</span></div>'
                f'<div style="font-size:10px;color:var(--dim);margin-top:2px;">↳ {reason}</div>'
                f'</div>'
            )
        blockers_html = (
            f'<div style="text-align:center;margin-bottom:10px;">'
            f'<div class="big-num" style="font-size:1.6rem;color:var(--amber);">{len(blocker_tasks)}</div>'
            f'<div style="font-size:10px;color:var(--dim);">blocked tasks</div>'
            f'</div>{rows_html}'
        )
        blockers_summary = str(len(blocker_tasks))

    # --- Burn rate forecast widget ---
    if burn_forecast is None:
        burn_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:14px;">'
            'No burn data available'
            '</div>'
        )
        burn_summary = "n/a"
    else:
        bf = burn_forecast
        proj_color = 'var(--red)' if bf['alert'] else 'var(--amber)' if bf['warn'] else 'var(--green)'
        proj_status = '⚠ WILL BREACH 95%' if bf['alert'] else '⚠ trending hot' if bf['warn'] else '● on track'
        burn_html = (
            f'<div style="display:flex;gap:16px;justify-content:center;margin-bottom:10px;">'
            f'<div style="text-align:center;">'
            f'<div class="big-num" style="font-size:1.6rem;">{bf["current_pct"]:.1f}%</div>'
            f'<div style="font-size:10px;color:var(--dim);">Used today</div>'
            f'</div>'
            f'<div style="text-align:center;border-left:1px solid var(--border);padding-left:16px;">'
            f'<div class="big-num" style="font-size:1.6rem;color:{proj_color};">{bf["projected_eom_pct"]:.1f}%</div>'
            f'<div style="font-size:10px;color:var(--dim);">Forecast EOM</div>'
            f'</div>'
            f'</div>'
            f'<div style="font-size:11px;color:var(--dim);text-align:center;margin-bottom:6px;">'
            f'{bf["daily_avg"]:,.0f} tokens/day · {bf["days_left"]} days remaining'
            f'</div>'
            f'<div style="text-align:center;font-size:11px;color:{proj_color};font-weight:600;">{proj_status}</div>'
        )
        burn_summary = f"{bf['projected_eom_pct']:.1f}% forecast"

    # --- Quality 30d sparkline widget ---
    if not sparkline_points:
        sparkline_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:14px;">'
            '<span style="color:var(--dim);">●</span> No history yet<br>'
            '<span style="font-size:10px;">Daily snapshot runs at 03:00 BRT cron · populates over 30 days</span>'
            '</div>'
        )
        sparkline_summary = "no data"
    elif len(sparkline_points) < 2:
        p = sparkline_points[0]
        sparkline_html = (
            f'<div style="text-align:center;padding:14px;">'
            f'<div class="big-num" style="font-size:1.8rem;">{p["avg"]:.1f}</div>'
            f'<div style="font-size:11px;color:var(--dim);">Single data point · {p["date"]}</div>'
            f'<div style="font-size:10px;color:var(--dim);margin-top:6px;">Need ≥2 days for trend</div>'
            f'</div>'
        )
        sparkline_summary = f"1 day · avg {p['avg']:.1f}"
    else:
        # Build inline SVG sparkline
        vals = [p["avg"] for p in sparkline_points]
        v_min = min(vals)
        v_max = max(vals)
        v_span = max(v_max - v_min, 1)  # avoid /0 on flat line
        w, h = 280, 60
        pad = 4
        n = len(sparkline_points)
        coords = []
        for i, p in enumerate(sparkline_points):
            x = pad + (i / max(n - 1, 1)) * (w - 2 * pad)
            y = h - pad - ((p["avg"] - v_min) / v_span) * (h - 2 * pad)
            coords.append(f"{x:.1f},{y:.1f}")
        polyline = " ".join(coords)
        first = sparkline_points[0]["avg"]
        last = sparkline_points[-1]["avg"]
        delta = last - first
        delta_color = 'var(--green)' if delta >= 0 else 'var(--red)'
        sparkline_html = (
            f'<div style="text-align:center;margin-bottom:8px;">'
            f'<div style="display:inline-flex;gap:14px;align-items:baseline;">'
            f'<div><span class="big-num" style="font-size:1.6rem;">{last:.1f}</span>'
            f'<span style="color:var(--dim);font-size:11px;margin-left:4px;">today</span></div>'
            f'<div style="color:{delta_color};font-weight:600;">{delta:+.1f}</div>'
            f'<div style="color:var(--dim);font-size:11px;">vs {sparkline_points[0]["date"][5:]}</div>'
            f'</div></div>'
            f'<svg width="100%" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="none" style="display:block;">'
            f'<polyline points="{polyline}" fill="none" stroke="var(--cyan)" stroke-width="2"/>'
            f'</svg>'
            f'<div style="display:flex;justify-content:space-between;font-size:10px;color:var(--dim);margin-top:4px;">'
            f'<span>{sparkline_points[0]["date"]}</span>'
            f'<span>min {v_min:.0f} · max {v_max:.0f}</span>'
            f'<span>{sparkline_points[-1]["date"]}</span>'
            f'</div>'
        )
        sparkline_summary = f"{n} days · {delta:+.1f}"

    # --- Regression alerts widget ---
    if not regression_alerts:
        regression_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:14px;">'
            '<span style="color:var(--green);">●</span> No regressions detected<br>'
            '<span style="font-size:10px;">All skills within 15pts of baseline</span>'
            '</div>'
        )
        regression_summary = "0"
    else:
        rows_html = ""
        for r in regression_alerts[:5]:
            rows_html += (
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:11px;">'
                f'<span style="color:var(--text);">{r["skill"]}</span>'
                f'<span><span style="color:var(--dim);">{r["baseline"]:.0f}→{r["current"]:.0f}</span> '
                f'<span style="color:var(--red);font-weight:600;margin-left:6px;">{r["delta"]:+.0f}</span></span>'
                f'</div>'
            )
        regression_html = (
            f'<div style="text-align:center;margin-bottom:10px;">'
            f'<div class="big-num" style="font-size:1.6rem;color:var(--red);">{len(regression_alerts)}</div>'
            f'<div style="font-size:10px;color:var(--dim);">skills regressed >15pts</div>'
            f'</div>{rows_html}'
        )
        regression_summary = str(len(regression_alerts))

    # Pulse time
    pulse_time = pulse.get("pulse_time", "nunca")
    if isinstance(pulse_time, str) and "T" in pulse_time:
        pulse_time = pulse_time[:16].replace("T", " ")

    # Active/blocked counts
    active_count = sum(1 for t in tasks if t.get("status") in ("todo", "in_progress", "in_review"))
    blocked_count = sum(1 for t in tasks if t.get("status") == "blocked")
    done_count = sum(1 for t in tasks if t.get("status") == "done")

    # Shared nav fragment (same nav as other dashboards — keeps page in sync
    # whenever _nav_fragment.html is updated). Substituted via {nav_html}
    # placeholder, so its braces are inserted literally without f-string
    # re-interpretation (no double-escaping needed).
    nav_path = ORCH / "_nav_fragment.html"
    nav_html = nav_path.read_text(encoding="utf-8") if nav_path.exists() else ""

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    head_short = git_head_short() or "no-git"

    html = f"""<!DOCTYPE html>
<html lang="pt"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>DARIO Orchestrator — Dashboard Live</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#0a0e1a;--surface:#111827;--card:#1a2235;--border:#2a3a5a;--text:#f0f4ff;--dim:#8896b3;--cyan:#00e5ff;--green:#00e676;--amber:#ffab00;--red:#ff5252;--purple:#b388ff}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);padding:20px;min-height:100vh}}
.header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid var(--border)}}
.logo{{font-size:20px;font-weight:800;text-shadow:0 0 20px rgba(0,229,255,.4)}}
.logo span{{color:var(--cyan)}}
.meta{{display:flex;gap:16px;font-size:12px;color:var(--dim);align-items:center}}
.badge{{padding:3px 10px;border-radius:10px;font-weight:600;font-size:11px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:24px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px}}
.card h3{{font-size:14px;color:var(--dim);margin-bottom:16px;text-transform:uppercase;letter-spacing:.08em}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;color:var(--dim);font-size:11px;text-transform:uppercase;padding:8px 6px;border-bottom:1px solid var(--border)}}
td{{padding:8px 6px;border-bottom:1px solid rgba(255,255,255,.03)}}
.big-num{{font-size:2.2rem;font-weight:800;color:var(--cyan)}}
.ring{{width:100px;height:100px;border-radius:50%;border:6px solid var(--border);border-top-color:var(--{budget_color});display:flex;align-items:center;justify-content:center;margin:0 auto 12px;font-size:1.1rem;font-weight:700}}
.health-row{{display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:13px}}
.dot{{width:8px;height:8px;border-radius:50%;flex-shrink:0}}
.dot-green{{background:var(--green);box-shadow:0 0 6px var(--green)}}
.dot-red{{background:var(--red);box-shadow:0 0 6px var(--red)}}
.footer{{text-align:center;color:var(--dim);font-size:11px;padding-top:16px;border-top:1px solid var(--border)}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body>
{nav_html}
<div class="header">
  <div class="logo">DARIO <span>Orchestrator</span> — Dashboard Live</div>
  <div class="meta">
    <span>Gerado: {now}</span>
    <span class="badge" style="background:rgba({'0,230,118' if pct<80 else '255,171,0' if pct<95 else '255,82,82'},.15);color:var(--{budget_color});border:1px solid rgba({'0,230,118' if pct<80 else '255,171,0' if pct<95 else '255,82,82'},.3);">Budget: {pct:.1f}%</span>
    <span class="badge" style="background:rgba(0,230,118,.15);color:var(--green);border:1px solid rgba(0,230,118,.3);" title="Soma monthly_value de clientes com billing_status=active. {active_paying} clientes pagantes.">MRR: {mrr_header}</span>
    <span>Pulse: {pulse_time}</span>
    <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 6px var(--green);"></span>
  </div>
</div>

<div class="grid">
  <!-- TASKS -->
  <div class="card">
    <h3>Taskboard ({len(tasks)} total | {active_count} activas | {blocked_count} bloqueadas | {done_count} done)</h3>
    <table>
      <thead><tr><th>ID</th><th>Tarefa</th><th>Status</th><th>Assignee</th><th>Prioridade</th><th>Idade</th></tr></thead>
      <tbody>{task_rows}</tbody>
    </table>
  </div>

  <!-- BUDGET -->
  <div class="card">
    <h3>Budget — {budget.get('month', datetime.now().strftime('%Y-%m'))}</h3>
    <div style="text-align:center;">
      <div class="ring">{pct:.1f}%</div>
      <div style="font-size:13px;color:var(--dim);">{budget.get('total_tokens_used',0):,} / {budget.get('limit',50000000):,} tokens</div>
    </div>
    <div style="margin-top:16px;">
      <div style="font-size:11px;color:var(--dim);margin-bottom:8px;text-transform:uppercase;">Por Projecto (top 3)</div>
      {proj_html or '<div style="color:var(--dim);font-size:12px;">Sem dados</div>'}
    </div>
    <div style="margin-top:12px;">
      <div style="font-size:11px;color:var(--dim);margin-bottom:8px;text-transform:uppercase;">Por Modelo</div>
      {model_html or '<div style="color:var(--dim);font-size:12px;">Sem dados</div>'}
    </div>
  </div>

  <!-- QUALITY -->
  <div class="card">
    <h3>Qualidade</h3>
    <div style="display:flex;gap:24px;justify-content:center;margin-bottom:16px;">
      <div style="text-align:center;">
        <div class="big-num">{avg_quality:.1f}</div>
        <div style="font-size:11px;color:var(--dim);">Score medio /100</div>
        <div style="font-size:10px;color:var(--dim);margin-top:2px;">(LLM-judge 5-dim)</div>
      </div>
      <div style="text-align:center;border-left:1px solid var(--border);padding-left:24px;">
        <div class="big-num" style="color:{('var(--green)' if delivery_rate_pct >= 50 else 'var(--amber)' if delivery_rate_pct >= 25 else 'var(--red)')};">{delivery_rate_pct:.0f}%</div>
        <div style="font-size:11px;color:var(--dim);">Delivery-ready</div>
        <div style="font-size:10px;color:var(--dim);margin-top:2px;">({delivery_yes}/{delivery_total} real outputs)</div>
      </div>
    </div>
    <div style="display:flex;gap:12px;justify-content:center;margin-bottom:16px;">
      <span class="badge" style="background:rgba(0,230,118,.15);color:var(--green);border:1px solid rgba(0,230,118,.3);">A: {tier_a}</span>
      <span class="badge" style="background:rgba(255,171,0,.15);color:var(--amber);border:1px solid rgba(255,171,0,.3);">B: {tier_b}</span>
      <span class="badge" style="background:rgba(136,150,179,.15);color:var(--dim);border:1px solid rgba(136,150,179,.3);">?: {unscored}</span>
      <span class="badge" style="background:rgba(67,160,255,.15);color:#43a0ff;border:1px solid rgba(67,160,255,.3);">Prod: {production_validated_count}</span>
    </div>
    {q_html or '<div style="color:var(--dim);font-size:12px;text-align:center;">Sem scores registados</div>'}
  </div>

  <!-- TOP CLIENTS (FASE 3) -->
  <div class="card">
    <h3>Top Clientes — por outputs entregues</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Ranking por nº de deliverables no vault Obsidian · exclui internal/archived
    </div>
    {clients_html or '<div style="color:var(--dim);font-size:12px;text-align:center;padding:20px;">Sem clientes registados<br><span style="font-size:10px;">Correr: python scripts/compute_client_stats.py</span></div>'}
  </div>

  <!-- PADRÃO A — Polished wrapper telemetry -->
  <div class="card">
    <h3>Padrão A — Polished Wrappers ({padrao_a_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Production runs telemetry · self-polishing skill loop · A/B target +4pts mean lift
    </div>
    {padrao_a_html}
  </div>

  <!-- SPEND BY TYPE — dev vs client (gap #4) -->
  <div class="card">
    <h3>Spend by Type ({spend_type_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Token attribution dev (DARIO internal) vs client (paid work) · fonte: config/project_types.yaml
    </div>
    {spend_type_html}
  </div>

  <!-- DIRECT API SPEND — anthropic SDK scripts (gap #6) -->
  <div class="card">
    <h3>API Spend Direct ({api_spend_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Scripts que usam anthropic SDK directo (DSPy, judge, etc.) · NÃO conta subscription work
    </div>
    {api_spend_html}
  </div>

  <!-- SUBAGENT TOKEN CAPTURE — Faixa 3 #1 (SubagentStop hook) -->
  <div class="card">
    <h3>Subagent Token Capture ({subagent_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Tokens consumidos por Agent tool (sidechain) · fonte: <code>subagent_runs/YYYY-MM/*.json</code> · hook: <code>enforcement/token_capture.py</code>
    </div>
    {subagent_html}
  </div>

  <!-- MODEL DRIFT — Risk #10 stamp + warn -->
  <div class="card">
    <h3>Model Drift ({drift_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Polished wrappers running on a model different from their `tested_with_model` declaration
    </div>
    {drift_html}
  </div>

  <!-- ENFORCEMENT LAYER — Risk #1 thin layer (parallelism + budget gate) -->
  <div class="card">
    <h3>Enforcement Layer ({enforcement_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Real Python guards on critical invariants · parallelism + budget hard-stop
    </div>
    {enforcement_html}
  </div>

  <!-- STALE TASKS (Phase 0.5 SLA breach surfacer) -->
  <div class="card">
    <h3>Stale Tasks ({stale_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Tasks stuck in_progress for >24h · checked_out_at vs now · sorted by age desc
    </div>
    {stale_html}
  </div>

  <!-- TOP BLOCKERS -->
  <div class="card">
    <h3>Top Blockers ({blockers_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Tasks with status=blocked · sorted by age desc · shows blocked_reason
    </div>
    {blockers_html}
  </div>

  <!-- BURN RATE FORECAST -->
  <div class="card">
    <h3>Burn Rate Forecast ({burn_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Linear projection of monthly token spend · current pace × days remaining
    </div>
    {burn_html}
  </div>

  <!-- SKILL REGRESSION ALERTS -->
  <div class="card">
    <h3>Skill Regressions ({regression_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Skills whose current avg is ≥15pts below their baseline · per CONVENTIONS Phase 8
    </div>
    {regression_html}
  </div>

  <!-- QUALITY SPARKLINE 30d -->
  <div class="card">
    <h3>Quality Avg — Last 30 days ({sparkline_summary})</h3>
    <div style="font-size:11px;color:var(--dim);margin-bottom:12px;">
      Daily snapshot of global avg quality · populated by cron at 03:00 BRT
    </div>
    {sparkline_html}
  </div>

  <!-- SYSTEM HEALTH -->
  <div class="card">
    <h3>Saude do Sistema</h3>
    <div class="health-row"><span class="dot dot-green"></span> Orchestrator — company.yaml ({company['total']} entidades)</div>
    <div class="health-row"><span class="dot dot-green"></span> Skills — {total_skills} totais (DARIO {skills['dario']}, DIVA {skills['diva']}, LUCAS {skills['lucas']}, SEO {skills['seo']}, A360 {skills['a360']})</div>
    <div class="health-row"><span class="dot dot-green"></span> Budget Tracker — {budget.get('month','?')}, {pct:.1f}% usado</div>
    <div class="health-row"><span class="dot dot-green"></span> Quality — {len(q_skills)} skills scored, avg {avg_quality:.1f}, delivery-ready {delivery_rate_pct:.0f}% ({delivery_yes}/{delivery_total})</div>
    <div class="health-row"><span class="dot {'dot-amber' if queue_pending > 0 else 'dot-green'}"></span> Review Queue — {queue_pending} pending, {queue_resolved} resolved {'(avg TTR ' + f'{queue_avg_ttr_min:.0f}min)' if queue_resolved else ''}</div>
    <div class="health-row"><span class="dot {'dot-green' if padrao_a else 'dot-amber'}"></span> Padrão A — {padrao_a_summary}{', last-30d lift +' + str(padrao_a['last_30_days']['overall'].get('mean_lift_pts', '?')) + 'pts' if padrao_a and padrao_a['last_30_days']['overall'].get('mean_lift_pts') is not None else ''}</div>
    <div class="health-row"><span class="dot dot-green"></span> Top clients — {len(top_clients)} ativos (ver card dedicado)</div>
    <div class="health-row"><span class="dot dot-green"></span> Tasks — {len(tasks)} activas, {done_count} done</div>
    <div class="health-row"><span class="dot {'dot-green' if pulse_time != 'nunca' else 'dot-red'}"></span> Last Pulse — {pulse_time}</div>
  </div>
</div>

<div class="footer">
  DARIO Orchestrator {DARIO_VERSION} ({head_short}) — Dashboard gerado automaticamente a partir dos ficheiros YAML reais<br>
  Regenerar: <code>python3 ~/.claude/orchestrator/generate_dashboard.py</code>
</div>

<!-- LIVE OVERLAYS — fetch from runtime API on :8422 every 10s -->
<div id="dario-live-now" style="position:fixed;top:60px;right:12px;display:none;
  background:rgba(10,14,26,.92);border:1px solid #2a3a5a;border-radius:10px;padding:10px 14px;
  backdrop-filter:blur(8px);font-size:11px;color:#f0f4ff;z-index:9998;max-width:260px;">
  <div style="color:#8896b3;font-size:9px;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px;">Now Running</div>
  <div id="dario-live-now-list"></div>
</div>

<div id="dario-live-ticker" style="position:fixed;bottom:0;left:0;right:0;
  background:rgba(10,14,26,.88);border-top:1px solid #2a3a5a;padding:6px 12px;
  font-size:11px;color:#8896b3;display:none;z-index:9997;font-family:monospace;
  white-space:nowrap;overflow:hidden;">
  <span id="dario-live-ticker-text">Awaiting events…</span>
</div>

<script>
(function() {{
  const API = 'http://localhost:8422';
  const nowBox = document.getElementById('dario-live-now');
  const nowList = document.getElementById('dario-live-now-list');
  const ticker = document.getElementById('dario-live-ticker');
  const tickerText = document.getElementById('dario-live-ticker-text');

  async function refreshNowRunning() {{
    try {{
      const r = await fetch(API + '/tasks');
      if (!r.ok) return;
      const data = await r.json();
      const live = (data.tasks || []).filter(t =>
        t.status === 'in_progress' || t.status === 'in_review'
      );
      if (!live.length) {{
        nowBox.style.display = 'none';
        return;
      }}
      nowBox.style.display = 'block';
      nowList.innerHTML = live.slice(0, 4).map(t => {{
        const tid = (t.id || '').slice(0, 10);
        const title = (t.title || '').slice(0, 30);
        const dot = t.status === 'in_progress' ? '#00e5ff' : '#ffab00';
        return `<div style="padding:3px 0;">
          <span style="color:${{dot}};">●</span>
          <span style="color:#00e5ff;font-weight:600;">${{tid}}</span>
          <span style="color:#8896b3;">${{title}}</span>
        </div>`;
      }}).join('');
    }} catch (e) {{}}
  }}

  let lastAuditId = 0;
  async function refreshTicker() {{
    try {{
      const r = await fetch(API + '/audit?limit=10');
      if (!r.ok) return;
      const data = await r.json();
      const entries = data.entries || [];
      if (!entries.length) return;
      const newest = entries[0];
      if ((newest.id || 0) <= lastAuditId) return;
      lastAuditId = newest.id || 0;
      const time = new Date(newest.timestamp).toLocaleTimeString('pt-PT', {{ hour12: false }});
      const action = (newest.action || 'event').replace(/_/g, ' ');
      const tid = newest.task_id || '';
      const details = (newest.details || '').slice(0, 80);
      tickerText.innerHTML = `<span style="color:#00e5ff;">${{time}}</span> · ${{action}} ${{tid}} · <span style="color:#f0f4ff;">${{details}}</span>`;
      ticker.style.display = 'block';
    }} catch (e) {{}}
  }}

  refreshNowRunning();
  refreshTicker();
  setInterval(refreshNowRunning, 10000);
  setInterval(refreshTicker, 5000);
}})();
</script>
</body></html>"""

    # --- Live JSON feed (2026-06-01): widgets auto-refresh from dashboard-data.json ---
    # The generator bakes a snapshot into HTML; this small JSON lets the open page
    # poll for fresh budget/tasks/quality every 20s without a regen/reload. Served
    # same-origin by the http.server (port 8766). Requires http:// (file:// blocks fetch).
    import json as _json_feed
    from datetime import datetime as _dt_feed
    _active = sum(1 for _t in tasks if str(_t.get("status", "")).lower()
                  not in ("done", "cancelled", "archived"))
    _feed = {
        "generated_at": _dt_feed.now().astimezone().isoformat(timespec="seconds"),
        "budget_pct": round(pct, 2),
        "active_tasks": _active,
        "total_tasks": len(tasks),
        "quality_avg": round(avg_quality, 1),
        "skills": total_skills,
    }
    try:
        (ORCH / "dashboard-data.json").write_text(
            _json_feed.dumps(_feed, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

    _live_strip = (
        '<div id="live-strip" style="display:flex;gap:18px;align-items:center;flex-wrap:wrap;'
        'padding:8px 18px;margin:0;background:#0d1320;border-bottom:1px solid #1c2740;'
        'font-size:12px;color:#8896b3;">'
        '<span style="color:#00e676;font-weight:700;">● LIVE</span>'
        '<span>Budget <b id="live-budget" style="color:#f0f4ff;">—</b></span>'
        '<span>Active tasks <b id="live-tasks" style="color:#f0f4ff;">—</b></span>'
        '<span>Quality <b id="live-quality" style="color:#f0f4ff;">—</b></span>'
        '<span>Skills <b id="live-skills" style="color:#f0f4ff;">—</b></span>'
        '<span id="live-updated" style="margin-left:auto;">updated —</span>'
        '</div>'
    )
    _live_script = (
        "<script>(function(){"
        "var $=function(i){return document.getElementById(i);};"
        "function r(){fetch('./dashboard-data.json?t='+Date.now())"
        ".then(function(x){return x.ok?x.json():null;})"
        ".then(function(d){if(!d)return;"
        "if($('live-budget'))$('live-budget').textContent=d.budget_pct+'%';"
        "if($('live-tasks'))$('live-tasks').textContent=d.active_tasks+'/'+d.total_tasks;"
        "if($('live-quality'))$('live-quality').textContent=d.quality_avg;"
        "if($('live-skills'))$('live-skills').textContent=d.skills;"
        "var u=$('live-updated');if(u&&d.generated_at){"
        "var age=(Date.now()-new Date(d.generated_at).getTime())/60000;"
        "u.textContent='updated '+new Date(d.generated_at).toLocaleTimeString('pt-PT',{hour12:false})+(age>30?' (stale)':'');"
        "u.style.color=age>30?'#ff5252':(age>10?'#ffab00':'#00e676');}"
        "}).catch(function(){});}"
        "r();setInterval(r,20000);})();</script>"
    )
    html = html.replace('<div class="header">', _live_strip + '<div class="header">', 1)
    html = html.replace('</body></html>', _live_script + '</body></html>', 1)

    with open(DASHBOARD, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard gerado: {DASHBOARD}")
    print(f"Tasks: {len(tasks)} | Budget: {pct:.1f}% | Quality: {avg_quality:.1f} | Skills: {total_skills}")

    # Auto-open
    if sys.platform == "win32":
        os.system(f'start "" "{DASHBOARD}"')
    elif sys.platform == "darwin":
        os.system(f'open "{DASHBOARD}"')
    else:
        os.system(f'xdg-open "{DASHBOARD}"')

if __name__ == "__main__":
    generate()

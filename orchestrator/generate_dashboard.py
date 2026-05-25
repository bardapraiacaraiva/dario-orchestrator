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

def get_tasks():
    tasks = []
    active = ORCH / "tasks" / "active"
    if active.exists():
        for f in active.glob("*.yaml"):
            t = load_yaml_safe(f)
            if t and isinstance(t, dict):
                tasks.append(t)
    return sorted(tasks, key=lambda x: x.get("priority", "low") == "critical", reverse=True)

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
    try:
        from db import DB
        drift_events = DB().get_drift_events()
    except Exception:
        drift_events = None

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

    # Task rows
    task_rows = ""
    for t in tasks[:10]:
        age = ""
        if t.get("created_at"):
            try:
                created = datetime.fromisoformat(t["created_at"].replace("Z", "+00:00"))
                delta = datetime.now(UTC) - created
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
        task_rows = '<tr><td colspan="6" style="text-align:center;color:var(--dim);padding:20px;">Nenhuma tarefa activa</td></tr>'

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

    # Model drift widget (Risk #10)
    if drift_events is None or len(drift_events) == 0:
        drift_html = (
            '<div style="color:var(--dim);font-size:12px;text-align:center;padding:14px;">'
            '<span style="color:var(--green);">●</span> No drift detected<br>'
            '<span style="font-size:10px;">All polished runs match declared model</span></div>'
        )
        drift_summary = "0 events"
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

    # Pulse time
    pulse_time = pulse.get("pulse_time", "nunca")
    if isinstance(pulse_time, str) and "T" in pulse_time:
        pulse_time = pulse_time[:16].replace("T", " ")

    # Active/blocked counts
    active_count = sum(1 for t in tasks if t.get("status") in ("todo", "in_progress", "in_review"))
    blocked_count = sum(1 for t in tasks if t.get("status") == "blocked")
    done_count = sum(1 for t in tasks if t.get("status") == "done")

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
    <h3>Tarefas Activas ({len(tasks)} total | {active_count} activas | {blocked_count} bloqueadas | {done_count} done)</h3>
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

</body></html>"""

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

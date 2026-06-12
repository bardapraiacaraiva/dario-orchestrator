#!/usr/bin/env python3
"""
DARIO CFO — Unified Financial Dashboard Engine
Aggregates all financial data into a single 360° view:
- Token costs & ROI (token_meter + budget_tracker)
- Client revenue & receivables (finance/receivables.yaml)
- Tax calendar (finance/tax_calendar.yaml + tax_calendar.py)
- Quality costs / rework (quality_scorer + DB scores)
- P&L snapshot (per project)
- Security tier compliance

Usage:
    python financial_dashboard.py              # Full dashboard (CLI)
    python financial_dashboard.py --json       # JSON output for API
    python financial_dashboard.py --html       # Generate HTML dashboard
    python financial_dashboard.py --section X  # Only one section
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

ORCH_DIR = Path(os.path.expanduser("~/.claude/orchestrator"))
FINANCE_DIR = ORCH_DIR / "finance"
DB_PATH = ORCH_DIR / "orchestrator.db"

USD_EUR = 0.92  # Default exchange rate


def load_yaml_safe(path):
    """Load YAML file safely, return empty dict if missing."""
    if not Path(path).exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def query_db(sql):
    """Query SQLite database."""
    try:
        import sqlite3
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(sql)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows
    except Exception:
        return []


def get_budget_data():
    """Get current month budget from DB."""
    now = datetime.date.today()
    month_key = now.strftime("%Y-%m")
    rows = query_db(f"SELECT * FROM budget WHERE month='{month_key}'")
    if rows:
        r = rows[0]
        return {
            "month": r.get("month", month_key),
            "tokens_used": r.get("tokens_used", 0),
            "token_limit": r.get("token_limit", 50000000),
            "percentage": round(r.get("tokens_used", 0) / max(r.get("token_limit", 50000000), 1) * 100, 2),
        }
    # Fallback to YAML
    budget_file = ORCH_DIR / "budgets" / f"{month_key.replace('-', '-')}.yaml"
    data = load_yaml_safe(budget_file)
    return {
        "month": month_key,
        "tokens_used": data.get("tokens_used", 0),
        "token_limit": data.get("token_limit", 50000000),
        "percentage": data.get("percentage", 0),
    }


def get_task_stats():
    """Get task statistics from DB."""
    tasks = query_db("SELECT * FROM tasks")
    total = len(tasks)
    done = sum(1 for t in tasks if t.get("status") == "done")
    active = total - done
    projects = set(t.get("project", "unknown") for t in tasks)

    # Token usage by project
    by_project = {}
    for t in tasks:
        proj = t.get("project", "unknown")
        tokens = t.get("actual_tokens") or t.get("estimated_tokens") or 0
        by_project[proj] = by_project.get(proj, 0) + tokens

    return {
        "total": total,
        "done": done,
        "active": active,
        "projects": len(projects),
        "by_project": dict(sorted(by_project.items(), key=lambda x: x[1], reverse=True)[:10]),
    }


def get_quality_stats():
    """Get quality scores from DB."""
    scores = query_db("SELECT skill, score FROM scores ORDER BY id DESC LIMIT 50")
    if not scores:
        return {"avg_score": 0, "total_scored": 0, "by_skill": {}}

    by_skill = {}
    for s in scores:
        skill = s.get("skill", "unknown")
        score = s.get("score", 0)
        if skill not in by_skill:
            by_skill[skill] = {"scores": [], "avg": 0}
        by_skill[skill]["scores"].append(score)

    for skill, data in by_skill.items():
        data["avg"] = round(sum(data["scores"]) / len(data["scores"]), 1)
        data["count"] = len(data["scores"])
        del data["scores"]

    all_scores = [s.get("score", 0) for s in scores]
    return {
        "avg_score": round(sum(all_scores) / len(all_scores), 1) if all_scores else 0,
        "total_scored": len(scores),
        "by_skill": by_skill,
    }


def get_tax_alerts():
    """Get tax calendar alerts via tax_calendar.py."""
    try:
        result = subprocess.run(
            [sys.executable, str(ORCH_DIR / "tax_calendar.py"), "--alerts", "--json"],
            capture_output=True, text=True, timeout=10
        )
        return json.loads(result.stdout) if result.stdout.strip() else {"obligations": []}
    except Exception:
        return {"obligations": []}


def get_receivables():
    """Load receivables data."""
    data = load_yaml_safe(FINANCE_DIR / "receivables.yaml")
    return data.get("summary", {
        "total_pending": 0,
        "total_overdue": 0,
        "total_paid_this_month": 0,
        "avg_collection_days": 0,
    })


def get_freelancers():
    """Load freelancer data."""
    data = load_yaml_safe(FINANCE_DIR / "freelancers.yaml")
    return data.get("summary", {
        "total_gross_ytd": 0,
        "total_irs_retained_ytd": 0,
        "total_net_paid_ytd": 0,
        "freelancers_active": 0,
    })


def get_security_compliance():
    """Check security tier compliance."""
    company = load_yaml_safe(ORCH_DIR / "company.yaml")
    workers = company.get("workers", {})

    tiered = sum(1 for w in workers.values() if w.get("security_tier"))
    with_validator = sum(1 for w in workers.values() if w.get("validator"))
    with_schema = sum(1 for w in workers.values() if w.get("output_schema"))

    finance_workers = [k for k in workers if any(x in k for x in
        ["conta-", "risco-", "cfo-", "financial", "pricing", "saas-metrics", "agency-finance"])]

    return {
        "total_finance_workers": len(finance_workers),
        "tiered": tiered,
        "with_validator": with_validator,
        "with_schema": with_schema,
        "compliance_pct": round(tiered / max(len(finance_workers), 1) * 100),
    }


def estimate_token_cost(tokens_used):
    """Rough EUR estimate from a raw token count (assumes a mixed model blend).

    NOTE: this is a coarse estimate, not the billed cost — it ignores the
    input/output split and cache pricing. The exact per-run cost_usd lives in
    subagent_runs/*.json; prefer summing those when accuracy matters.
    Prices corrected 2026-06-12 (Fase 2) to the canonical model_pricing.yaml:
    Opus $5/$25 (was 15/75), Haiku $1/$5 (was 0.80/4).
    """
    # Weighted blend: 10% Opus, 60% Sonnet, 30% Haiku; (input+output)/2 each.
    cost_per_1m = 0.10 * (5 + 25) / 2 + 0.60 * (3 + 15) / 2 + 0.30 * (1 + 5) / 2
    cost_usd = (tokens_used / 1_000_000) * cost_per_1m
    return round(cost_usd * USD_EUR, 2)


def build_dashboard_data():
    """Build complete dashboard data object."""
    today = datetime.date.today()

    budget = get_budget_data()
    tasks = get_task_stats()
    quality = get_quality_stats()
    tax = get_tax_alerts()
    receivables = get_receivables()
    freelancers = get_freelancers()
    security = get_security_compliance()

    estimated_cost = estimate_token_cost(budget["tokens_used"])

    return {
        "generated_at": datetime.datetime.now().isoformat(),
        "month": today.strftime("%Y-%m"),
        "budget": {
            **budget,
            "estimated_cost_eur": estimated_cost,
            "status": "OK" if budget["percentage"] < 80 else ("WARNING" if budget["percentage"] < 95 else "CRITICAL"),
        },
        "tasks": tasks,
        "quality": quality,
        "tax_alerts": {
            "total": tax.get("total_obligations", 0),
            "overdue": tax.get("overdue", 0),
            "urgent": tax.get("urgent", 0),
            "warnings": tax.get("warnings", 0),
            "obligations": tax.get("obligations", [])[:5],  # Top 5
        },
        "receivables": receivables,
        "freelancers": freelancers,
        "security": security,
    }


def generate_html(data):
    """Generate HTML dashboard."""
    tax_rows = ""
    for obl in data["tax_alerts"].get("obligations", []):
        color = {"OVERDUE": "#ff4444", "URGENT": "#ff8800", "WARNING": "#ffcc00", "OK": "#44cc44", "DONE": "#888"}.get(obl.get("urgency", "OK"), "#888")
        tax_rows += f"""<tr>
            <td>{obl.get('name','')[:45]}</td>
            <td>{obl.get('deadline','')}</td>
            <td>{obl.get('days_until','')}d</td>
            <td><span style="color:{color};font-weight:bold">{obl.get('urgency','')}</span></td>
        </tr>"""

    project_rows = ""
    for proj, tokens in data["tasks"]["by_project"].items():
        cost = estimate_token_cost(tokens)
        project_rows += f"<tr><td>{proj}</td><td>{tokens:,}</td><td>EUR {cost:.2f}</td></tr>"

    quality_rows = ""
    for skill, qdata in data["quality"]["by_skill"].items():
        quality_rows += f"<tr><td>{skill}</td><td>{qdata['avg']}</td><td>{qdata['count']}</td></tr>"

    budget = data["budget"]
    budget_color = "#44cc44" if budget["percentage"] < 80 else ("#ff8800" if budget["percentage"] < 95 else "#ff4444")

    sec = data["security"]

    html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DARIO CFO Dashboard</title>
<style>
:root {{ --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9; --accent: #58a6ff; --green: #3fb950; --yellow: #d29922; --red: #f85149; --orange: #d18616; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace; padding: 20px; }}
h1 {{ color: var(--accent); font-size: 1.4em; margin-bottom: 4px; }}
h2 {{ color: var(--accent); font-size: 1.1em; margin-bottom: 12px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }}
.subtitle {{ color: #8b949e; font-size: 0.85em; margin-bottom: 20px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 16px; margin-bottom: 16px; }}
.card {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }}
.metric {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid var(--border); font-size: 0.9em; }}
.metric:last-child {{ border: none; }}
.metric .label {{ color: #8b949e; }}
.metric .value {{ font-weight: 600; }}
.metric .value.green {{ color: var(--green); }}
.metric .value.yellow {{ color: var(--yellow); }}
.metric .value.red {{ color: var(--red); }}
.metric .value.orange {{ color: var(--orange); }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.85em; }}
th {{ text-align: left; color: #8b949e; border-bottom: 1px solid var(--border); padding: 6px 4px; font-weight: 500; }}
td {{ padding: 5px 4px; border-bottom: 1px solid #21262d; }}
.bar {{ height: 8px; background: #21262d; border-radius: 4px; overflow: hidden; margin-top: 8px; }}
.bar-fill {{ height: 100%; border-radius: 4px; transition: width 0.3s; }}
.header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
.badge {{ background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 4px 12px; font-size: 0.8em; }}
.alert-banner {{ background: #1c0f0f; border: 1px solid var(--red); border-radius: 8px; padding: 12px; margin-bottom: 16px; }}
.alert-banner.warning {{ background: #1c1a0f; border-color: var(--orange); }}
</style>
</head>
<body>
<div class="header">
    <div>
        <h1>DARIO CFO Dashboard</h1>
        <div class="subtitle">Financial Command Center — {data['month']} — Generated {data['generated_at'][:19]}</div>
    </div>
    <div>
        <span class="badge">Budget: <span style="color:{budget_color}">{budget['percentage']:.1f}%</span></span>
        <span class="badge">Tasks: {data['tasks']['done']}/{data['tasks']['total']}</span>
        <span class="badge">Quality: {data['quality']['avg_score']}</span>
    </div>
</div>

{"<div class='alert-banner'><strong>TAX ALERT:</strong> " + str(data['tax_alerts']['overdue']) + " obrigacao(oes) em ATRASO + " + str(data['tax_alerts']['urgent']) + " URGENTE(S)</div>" if data['tax_alerts']['overdue'] > 0 or data['tax_alerts']['urgent'] > 0 else ""}

<div class="grid">
    <div class="card">
        <h2>Token Budget</h2>
        <div class="metric"><span class="label">Tokens usados</span><span class="value">{budget['tokens_used']:,}</span></div>
        <div class="metric"><span class="label">Limite mensal</span><span class="value">{budget['token_limit']:,}</span></div>
        <div class="metric"><span class="label">Uso</span><span class="value" style="color:{budget_color}">{budget['percentage']:.2f}%</span></div>
        <div class="metric"><span class="label">Custo estimado</span><span class="value">EUR {budget['estimated_cost_eur']:.2f}</span></div>
        <div class="bar"><div class="bar-fill" style="width:{min(budget['percentage'],100):.1f}%;background:{budget_color}"></div></div>
    </div>

    <div class="card">
        <h2>Tasks</h2>
        <div class="metric"><span class="label">Total</span><span class="value">{data['tasks']['total']}</span></div>
        <div class="metric"><span class="label">Concluidas</span><span class="value green">{data['tasks']['done']}</span></div>
        <div class="metric"><span class="label">Activas</span><span class="value yellow">{data['tasks']['active']}</span></div>
        <div class="metric"><span class="label">Projectos</span><span class="value">{data['tasks']['projects']}</span></div>
        <div class="metric"><span class="label">Quality avg</span><span class="value">{data['quality']['avg_score']}</span></div>
    </div>

    <div class="card">
        <h2>Receivables</h2>
        <div class="metric"><span class="label">Pendente</span><span class="value">EUR {data['receivables'].get('total_pending', 0):,.2f}</span></div>
        <div class="metric"><span class="label">Overdue</span><span class="value red">EUR {data['receivables'].get('total_overdue', 0):,.2f}</span></div>
        <div class="metric"><span class="label">Pago este mes</span><span class="value green">EUR {data['receivables'].get('total_paid_this_month', 0):,.2f}</span></div>
        <div class="metric"><span class="label">Dias med. cobranca</span><span class="value">{data['receivables'].get('avg_collection_days', 0)}</span></div>
    </div>

    <div class="card">
        <h2>Freelancers YTD</h2>
        <div class="metric"><span class="label">Bruto total</span><span class="value">EUR {data['freelancers'].get('total_gross_ytd', 0):,.2f}</span></div>
        <div class="metric"><span class="label">IRS retido</span><span class="value">EUR {data['freelancers'].get('total_irs_retained_ytd', 0):,.2f}</span></div>
        <div class="metric"><span class="label">Liquido pago</span><span class="value">EUR {data['freelancers'].get('total_net_paid_ytd', 0):,.2f}</span></div>
        <div class="metric"><span class="label">Activos</span><span class="value">{data['freelancers'].get('freelancers_active', 0)}</span></div>
    </div>
</div>

<div class="grid">
    <div class="card">
        <h2>Calendario Fiscal</h2>
        <table>
            <tr><th>Obrigacao</th><th>Deadline</th><th>Dias</th><th>Status</th></tr>
            {tax_rows if tax_rows else "<tr><td colspan='4' style='color:#8b949e'>Sem alertas</td></tr>"}
        </table>
    </div>

    <div class="card">
        <h2>Custo por Projecto</h2>
        <table>
            <tr><th>Projecto</th><th>Tokens</th><th>Custo Est.</th></tr>
            {project_rows if project_rows else "<tr><td colspan='3' style='color:#8b949e'>Sem dados</td></tr>"}
        </table>
    </div>
</div>

<div class="grid">
    <div class="card">
        <h2>Quality por Skill</h2>
        <table>
            <tr><th>Skill</th><th>Avg Score</th><th>Execucoes</th></tr>
            {quality_rows if quality_rows else "<tr><td colspan='3' style='color:#8b949e'>Sem scores</td></tr>"}
        </table>
    </div>

    <div class="card">
        <h2>Security Compliance</h2>
        <div class="metric"><span class="label">Workers financeiros</span><span class="value">{sec['total_finance_workers']}</span></div>
        <div class="metric"><span class="label">Com security tier</span><span class="value">{sec['tiered']}</span></div>
        <div class="metric"><span class="label">Com validator</span><span class="value">{sec['with_validator']}</span></div>
        <div class="metric"><span class="label">Com output schema</span><span class="value">{sec['with_schema']}</span></div>
        <div class="metric"><span class="label">Compliance</span><span class="value {'green' if sec['compliance_pct']>=80 else 'yellow'}">{sec['compliance_pct']}%</span></div>
        <div class="bar"><div class="bar-fill" style="width:{sec['compliance_pct']}%;background:var(--green)"></div></div>
    </div>
</div>

<div style="text-align:center;color:#8b949e;margin-top:20px;font-size:0.8em">
    DARIO CFO v1.0 — Wave 5 Dashboard — Auto-refresh: <a href="/cfo" style="color:var(--accent)">reload</a> |
    <a href="/cfo/data" style="color:var(--accent)">JSON API</a> |
    <a href="/dashboard" style="color:var(--accent)">Orchestrator Dashboard</a>
</div>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="DARIO CFO Financial Dashboard")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--html", action="store_true", help="Generate HTML to stdout")
    parser.add_argument("--save-html", action="store_true", help="Save HTML to cfo_dashboard.html")
    parser.add_argument("--section", type=str, help="Only one section: budget|tasks|quality|tax|receivables|freelancers|security")
    args = parser.parse_args()

    data = build_dashboard_data()

    if args.section:
        section = data.get(args.section) or data.get(f"{args.section}_alerts")
        if section:
            print(json.dumps(section, indent=2, ensure_ascii=False, default=str))
        else:
            print(f"Section '{args.section}' not found. Available: budget, tasks, quality, tax_alerts, receivables, freelancers, security")
        return

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
        return

    if args.html or args.save_html:
        html = generate_html(data)
        if args.save_html:
            out_path = ORCH_DIR / "cfo_dashboard.html"
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Dashboard saved to {out_path}")
        else:
            print(html)
        return

    # CLI output
    b = data["budget"]
    t = data["tasks"]
    q = data["quality"]
    tx = data["tax_alerts"]
    s = data["security"]

    print(f"\n{'='*60}")
    print(f"  DARIO CFO DASHBOARD — {data['month']}")
    print(f"{'='*60}")
    print(f"\n  BUDGET        {b['tokens_used']:>12,} / {b['token_limit']:,} ({b['percentage']:.2f}%) — EUR {b['estimated_cost_eur']:.2f}")
    print(f"  TASKS         {t['done']:>4} done / {t['total']} total — {t['projects']} projects")
    print(f"  QUALITY       {q['avg_score']:>5.1f} avg — {q['total_scored']} scored")
    print(f"  TAX ALERTS    {tx['overdue']} overdue | {tx['urgent']} urgent | {tx['warnings']} warning")
    print(f"  SECURITY      {s['tiered']} tiered / {s['total_finance_workers']} finance workers ({s['compliance_pct']}%)")
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()

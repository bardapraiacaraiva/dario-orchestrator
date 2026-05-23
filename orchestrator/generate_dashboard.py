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
    skills = count_skills()
    company = get_company()
    total_skills = sum(skills.values())

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
                if c.get("status") not in ("internal", "archived")
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

  <!-- SYSTEM HEALTH -->
  <div class="card">
    <h3>Saude do Sistema</h3>
    <div class="health-row"><span class="dot dot-green"></span> Orchestrator — company.yaml ({company['total']} entidades)</div>
    <div class="health-row"><span class="dot dot-green"></span> Skills — {total_skills} totais (DARIO {skills['dario']}, DIVA {skills['diva']}, LUCAS {skills['lucas']}, SEO {skills['seo']}, A360 {skills['a360']})</div>
    <div class="health-row"><span class="dot dot-green"></span> Budget Tracker — {budget.get('month','?')}, {pct:.1f}% usado</div>
    <div class="health-row"><span class="dot dot-green"></span> Quality — {len(q_skills)} skills scored, avg {avg_quality:.1f}, delivery-ready {delivery_rate_pct:.0f}% ({delivery_yes}/{delivery_total})</div>
    <div class="health-row"><span class="dot {'dot-amber' if queue_pending > 0 else 'dot-green'}"></span> Review Queue — {queue_pending} pending, {queue_resolved} resolved {'(avg TTR ' + f'{queue_avg_ttr_min:.0f}min)' if queue_resolved else ''}</div>
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

#!/usr/bin/env python3
"""
DARIO Cognitive Dashboard Generator
====================================
Upgrade 13 (operational complement to Sprints 1-4 + U11+U12+U14).

Generates a static HTML dashboard (cognitive_dashboard.html) that visualises
the state of every cognitive subsystem in one page:

  - Drift status per eval (golden comparison)
  - CoT overconfidence rate + verdict breakdown
  - Semantic memory growth (excellence vs patterns)
  - Integrity gate status (7 checks)
  - Cron history (last 7 days)
  - Q-value top skills
  - Synaptic graph health
  - Embeddings cache freshness

All data is read live from YAML/SQLite on each generation. No server,
no JS — pure server-rendered HTML, openable in any browser.

CLI:
    python cognitive_dashboard.py            Generate dashboard
    python cognitive_dashboard.py --open     Generate + open in browser
    python cognitive_dashboard.py --json     Emit dataset only (debug)
"""

import argparse
import json
import sys
import webbrowser
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
DASHBOARD_FILE = ORCH_DIR / "cognitive_dashboard.html"

sys.path.insert(0, str(ORCH_DIR))

try:
    from ruamel.yaml import YAML
    _yaml = YAML()

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _yaml.load(f)
except ImportError:
    import yaml as _pyaml

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _pyaml.safe_load(f)


# =============================================================================
# DATA COLLECTORS — each returns a dict ready for rendering
# =============================================================================

def collect_drift_status() -> dict:
    """Per-eval golden status — last known comparison result for each."""
    from golden_eval import GOLDEN_DIR, compare_against_golden, list_goldens
    goldens = list_goldens()
    rows = []
    for g in goldens:
        text_file = GOLDEN_DIR / f"{g['eval_id']}.golden.txt"
        if not text_file.exists():
            continue
        text = text_file.read_text(encoding="utf-8")
        r = compare_against_golden(g["eval_id"], text, candidate_score=g["human_score"])
        rows.append({
            "eval_id": g["eval_id"],
            "human_score": g["human_score"],
            "verdict": r.get("verdict", "?"),
            "lexical": r.get("lexical_jaccard"),
            "semantic": r.get("semantic_cosine"),
            "length_ratio": r.get("length_ratio"),
            "drift_severity": r.get("drift_severity"),
            "version": g["version"],
        })
    return {
        "total": len(rows),
        "rows": rows,
        "match_count": sum(1 for r in rows if r["verdict"] == "MATCH"),
        "drift_count": sum(1 for r in rows if r["verdict"] == "DRIFT"),
        "degraded_count": sum(1 for r in rows if r["verdict"] == "DEGRADED"),
    }


def collect_cot_health() -> dict:
    from dispatch.dispatch_cot import stats
    s = stats()
    return {
        "total_traces": s["total_traces"],
        "by_level": s["by_confidence_level"],
        "by_signal": s["by_winning_signal"],
        "postmortems": s["postmortems"],
        "overconfidence_rate": s["overconfidence_rate"],
    }


def collect_semantic_memory() -> dict:
    from cognitive.episode_promoter import stats as ep_stats
    s = ep_stats()
    # Read recent patterns from disk
    sem_dir = ORCH_DIR / "memory" / "semantic"
    recent_patterns = []
    if sem_dir.exists():
        for f in sorted(sem_dir.glob("SEM-*pattern*.yaml"))[:5]:
            try:
                data = _load_yaml(str(f))
                if isinstance(data, dict):
                    recent_patterns.append({
                        "name": data.get("name", f.stem),
                        "type": data.get("type", "pattern"),
                        "confidence": data.get("confidence"),
                        "episodes": len(data.get("promoted_from_episodes") or []),
                    })
            except Exception:
                continue
    return {
        "total": s["semantic_memories"],
        "by_type": s["by_type"],
        "auto_rules": s["auto_rules"],
        "recent_patterns": recent_patterns,
    }


def collect_integrity_status() -> dict:
    sys.path.insert(0, str(ORCH_DIR / "tools"))
    from integrity_gate import run_all
    report = run_all()
    checks = []
    for c in report["checks"]:
        checks.append({
            "name": c["name"],
            "status": c["status"],
            "summary": c.get("summary", ""),
        })
    return {
        "verdict": report["verdict"],
        "exit_code": report["exit_code"],
        "checks": checks,
    }


def collect_cron_history() -> dict:
    cron_dir = ORCH_DIR / "cron"
    last_run_file = cron_dir / "last_run.yaml"
    last_run = {}
    if last_run_file.exists():
        try:
            last_run = _load_yaml(str(last_run_file)) or {}
        except Exception:
            pass
    history = []
    if cron_dir.exists():
        for f in sorted(cron_dir.glob("daily-*.yaml"), reverse=True)[:7]:
            try:
                data = _load_yaml(str(f))
                if isinstance(data, dict):
                    history.append({
                        "date": f.stem.replace("daily-", ""),
                        "status": data.get("status", "ok"),
                        "alerts": len(data.get("alerts", [])),
                        "warnings": len(data.get("warnings", [])),
                        "duration": data.get("duration_seconds"),
                    })
            except Exception:
                continue
    return {"last_run": last_run, "history": history}


def collect_qvalue_top() -> dict:
    from qvalue_memory_wire import stats as q_stats
    from qvalue_memory_wire import top_strategies
    s = q_stats()
    top = top_strategies(5)
    return {
        "total_episodes": s.get("total_episodes", 0),
        "distinct_skills": s.get("distinct_skills", 0),
        "avg_q_value": s.get("avg_q_value", 0),
        "top": top,
    }


def collect_synaptic_health() -> dict:
    from synaptic_update import _load_weights, stats
    s = stats()
    weights = _load_weights()
    graph = weights.get("affinity_graph", {})
    # Top 5 strongest pairs
    pairs_sorted = sorted(
        [(k, v) for k, v in graph.items() if isinstance(v, dict)],
        key=lambda x: -float(x[1].get("weight", 0.5))
    )[:5]
    top_pairs = [
        {"pair": k, "weight": v.get("weight", 0.5),
         "co_activations": v.get("co_activations", 0),
         "avg_score": v.get("avg_combined_score", 0)}
        for k, v in pairs_sorted
    ]
    return {**s, "top_pairs": top_pairs}


def collect_embeddings_status() -> dict:
    from dispatch.semantic_dispatch import cache_stats, extract_skill_corpus
    s = cache_stats()
    corpus = extract_skill_corpus()
    return {
        "total_cached": s["total"],
        "corpus_size": len(corpus),
        "coverage_pct": round(s["total"] / max(len(corpus), 1) * 100, 1),
        "newest": s.get("newest"),
        "oldest": s.get("oldest"),
    }


def collect_all() -> dict:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "drift": collect_drift_status(),
        "cot": collect_cot_health(),
        "semantic": collect_semantic_memory(),
        "integrity": collect_integrity_status(),
        "cron": collect_cron_history(),
        "qvalue": collect_qvalue_top(),
        "synaptic": collect_synaptic_health(),
        "embeddings": collect_embeddings_status(),
    }


# =============================================================================
# RENDERERS — produce HTML fragments
# =============================================================================

def _badge(text: str, kind: str = "ok") -> str:
    palette = {
        "ok": ("rgba(0,230,118,.15)", "var(--green)", "rgba(0,230,118,.3)"),
        "warn": ("rgba(255,171,0,.15)", "var(--amber)", "rgba(255,171,0,.3)"),
        "alert": ("rgba(255,82,82,.15)", "var(--red)", "rgba(255,82,82,.3)"),
        "info": ("rgba(0,229,255,.15)", "var(--cyan)", "rgba(0,229,255,.3)"),
        "muted": ("rgba(136,150,179,.15)", "var(--dim)", "rgba(136,150,179,.3)"),
    }
    bg, color, border = palette.get(kind, palette["info"])
    return (
        f'<span class="badge" style="background:{bg};color:{color};border:1px solid {border};">'
        f'{text}</span>'
    )


def _verdict_kind(verdict: str) -> str:
    return {
        "PASS": "ok", "MATCH": "ok",
        "WARN": "warn", "DEGRADED": "warn",
        "FAIL": "alert", "DRIFT": "alert", "ERROR": "alert",
    }.get(verdict, "muted")


def render_drift_card(data: dict) -> str:
    rows_html = []
    for r in data["rows"]:
        verdict_badge = _badge(r["verdict"], _verdict_kind(r["verdict"]))
        rows_html.append(
            f"<tr>"
            f"<td style='font-weight:600;color:var(--cyan);'>{r['eval_id']}</td>"
            f"<td>{verdict_badge}</td>"
            f"<td>{r.get('human_score', '?')}</td>"
            f"<td>{r.get('lexical', '-')}</td>"
            f"<td>{r.get('semantic', '-')}</td>"
            f"<td>v{r.get('version', 1)}</td>"
            f"</tr>"
        )
    rows = "\n".join(rows_html) or "<tr><td colspan='6' style='color:var(--dim);'>No goldens captured</td></tr>"
    summary_badge = _badge(
        f"{data['match_count']} MATCH · {data['degraded_count']} DEGRADED · {data['drift_count']} DRIFT",
        "alert" if data["drift_count"] > 0 else ("warn" if data["degraded_count"] > 0 else "ok"),
    )
    return f"""
<div class="card">
  <h3>Golden Eval Drift Status {summary_badge}</h3>
  <table>
    <thead><tr><th>Eval</th><th>Verdict</th><th>Human</th><th>Lexical</th><th>Semantic</th><th>v</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>"""


def render_cot_card(data: dict) -> str:
    rate = data["overconfidence_rate"]
    rate_kind = "alert" if rate >= 0.20 else ("warn" if rate >= 0.10 else "ok")
    pm = data["postmortems"]
    return f"""
<div class="card">
  <h3>Dispatch Chain-of-Thought {_badge(f"OC rate {rate:.0%}", rate_kind)}</h3>
  <div style="display:flex;gap:20px;flex-wrap:wrap;">
    <div><div class="big-num">{data['total_traces']}</div>
         <div style="color:var(--dim);font-size:11px;">TOTAL TRACES</div></div>
    <div><div class="big-num" style="color:var(--green);">{pm.get('VINDICATED',0)}</div>
         <div style="color:var(--dim);font-size:11px;">VINDICATED</div></div>
    <div><div class="big-num" style="color:var(--red);">{pm.get('OVERCONFIDENT',0)}</div>
         <div style="color:var(--dim);font-size:11px;">OVERCONFIDENT</div></div>
    <div><div class="big-num" style="color:var(--amber);">{pm.get('CONFIRMED_DOUBT',0)}</div>
         <div style="color:var(--dim);font-size:11px;">CONFIRMED DOUBT</div></div>
  </div>
  <div style="margin-top:16px;font-size:12px;color:var(--dim);">
    By signal: explicit={data['by_signal'].get('explicit',0)} ·
    semantic={data['by_signal'].get('semantic',0)} ·
    qvalue={data['by_signal'].get('qvalue',0)} ·
    keyword={data['by_signal'].get('keyword',0)}
  </div>
</div>"""


def render_semantic_card(data: dict) -> str:
    patterns_html = []
    for p in data["recent_patterns"]:
        patterns_html.append(
            f"<div class='health-row'><span class='dot dot-green'></span>"
            f"<span style='font-weight:600;'>{p['name']}</span>"
            f"<span style='color:var(--dim);font-size:11px;margin-left:auto;'>"
            f"{p['episodes']} episodes · conf {p.get('confidence', '?')}</span></div>"
        )
    patterns = "\n".join(patterns_html) or "<div style='color:var(--dim);'>No patterns yet</div>"
    return f"""
<div class="card">
  <h3>Semantic Memory & Auto-Rules</h3>
  <div style="display:flex;gap:20px;margin-bottom:16px;">
    <div><div class="big-num">{data['total']}</div>
         <div style="color:var(--dim);font-size:11px;">MEMORIES</div></div>
    <div><div class="big-num" style="color:var(--green);">{data['by_type'].get('excellence',0)}</div>
         <div style="color:var(--dim);font-size:11px;">EXCELLENCE</div></div>
    <div><div class="big-num" style="color:var(--purple);">{data['by_type'].get('pattern',0)}</div>
         <div style="color:var(--dim);font-size:11px;">PATTERNS</div></div>
    <div><div class="big-num" style="color:var(--cyan);">{data['auto_rules']}</div>
         <div style="color:var(--dim);font-size:11px;">AUTO-RULES</div></div>
  </div>
  <div>{patterns}</div>
</div>"""


def render_integrity_card(data: dict) -> str:
    rows_html = []
    for c in data["checks"]:
        status_badge = _badge(c["status"], _verdict_kind(c["status"]))
        rows_html.append(
            f"<div class='health-row'>"
            f"<span style='flex:1;font-weight:500;'>{c['name']}</span>"
            f"{status_badge}"
            f"</div>"
            f"<div style='font-size:11px;color:var(--dim);margin:2px 0 8px 0;padding-left:2px;'>{c.get('summary','')}</div>"
        )
    verdict_badge = _badge(data["verdict"], _verdict_kind(data["verdict"]))
    return f"""
<div class="card">
  <h3>Integrity Gate {verdict_badge}</h3>
  {''.join(rows_html)}
</div>"""


def render_cron_card(data: dict) -> str:
    rows_html = []
    for r in data["history"]:
        kind = _verdict_kind({"ok": "PASS", "warn": "WARN", "alert": "FAIL"}.get(r["status"], "MUTED"))
        rows_html.append(
            f"<tr>"
            f"<td>{r['date']}</td>"
            f"<td>{_badge(r['status'].upper(), kind)}</td>"
            f"<td>{r['alerts']}</td>"
            f"<td>{r['warnings']}</td>"
            f"<td>{r.get('duration', '-'):.1f}s</td>"
            f"</tr>"
        )
    rows = "\n".join(rows_html) or "<tr><td colspan='5' style='color:var(--dim);'>No cron history yet</td></tr>"
    last = data["last_run"]
    last_summary = (f"Last ran {last.get('ran_at', '?')[:19]}" if last else "Never run")
    return f"""
<div class="card">
  <h3>Cron Daily History — {last_summary}</h3>
  <table>
    <thead><tr><th>Date</th><th>Status</th><th>Alerts</th><th>Warnings</th><th>Duration</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>"""


def render_qvalue_card(data: dict) -> str:
    rows_html = []
    for s in data["top"]:
        rows_html.append(
            f"<tr>"
            f"<td style='font-weight:600;color:var(--cyan);'>{s['skill']}</td>"
            f"<td>{s['q_value']:.3f}</td>"
            f"<td>{s['avg_score']:.1f}</td>"
            f"<td>{s['visits']}</td>"
            f"</tr>"
        )
    rows = "\n".join(rows_html) or "<tr><td colspan='4' style='color:var(--dim);'>No episodes yet</td></tr>"
    return f"""
<div class="card">
  <h3>Q-Value Memory — Top Strategies</h3>
  <div style="display:flex;gap:20px;margin-bottom:14px;">
    <div><div class="big-num">{data['total_episodes']}</div>
         <div style="color:var(--dim);font-size:11px;">EPISODES</div></div>
    <div><div class="big-num">{data['distinct_skills']}</div>
         <div style="color:var(--dim);font-size:11px;">DISTINCT SKILLS</div></div>
    <div><div class="big-num" style="color:var(--cyan);">{data['avg_q_value']}</div>
         <div style="color:var(--dim);font-size:11px;">AVG Q-VALUE</div></div>
  </div>
  <table>
    <thead><tr><th>Skill</th><th>Q-Value</th><th>Avg Score</th><th>Visits</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>"""


def render_synaptic_card(data: dict) -> str:
    rows_html = []
    for p in data["top_pairs"]:
        rows_html.append(
            f"<tr>"
            f"<td style='font-weight:500;'>{p['pair']}</td>"
            f"<td>{p['weight']}</td>"
            f"<td>{p['co_activations']}</td>"
            f"<td>{p['avg_score']}</td>"
            f"</tr>"
        )
    rows = "\n".join(rows_html) or "<tr><td colspan='4' style='color:var(--dim);'>No pairs</td></tr>"
    return f"""
<div class="card">
  <h3>Synaptic Affinity Graph</h3>
  <div style="display:flex;gap:20px;margin-bottom:14px;">
    <div><div class="big-num">{data['total_pairs']}</div>
         <div style="color:var(--dim);font-size:11px;">TOTAL PAIRS</div></div>
    <div><div class="big-num" style="color:var(--green);">{data['active_pairs']}</div>
         <div style="color:var(--dim);font-size:11px;">ACTIVE</div></div>
    <div><div class="big-num">{data['avg_weight']}</div>
         <div style="color:var(--dim);font-size:11px;">AVG WEIGHT</div></div>
    <div><div class="big-num" style="color:var(--cyan);">{data['total_co_activations']}</div>
         <div style="color:var(--dim);font-size:11px;">CO-ACT TOTAL</div></div>
  </div>
  <table>
    <thead><tr><th>Pair</th><th>Weight</th><th>Co-Act</th><th>Avg</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>"""


def render_embeddings_card(data: dict) -> str:
    coverage = data["coverage_pct"]
    kind = "ok" if coverage >= 99 else ("warn" if coverage >= 95 else "alert")
    newest = data.get("newest") or ("?", "?")
    return f"""
<div class="card">
  <h3>Semantic Embeddings Cache {_badge(f"coverage {coverage}%", kind)}</h3>
  <div style="display:flex;gap:20px;">
    <div><div class="big-num">{data['total_cached']}</div>
         <div style="color:var(--dim);font-size:11px;">CACHED</div></div>
    <div><div class="big-num">{data['corpus_size']}</div>
         <div style="color:var(--dim);font-size:11px;">CORPUS</div></div>
  </div>
  <div style="margin-top:14px;font-size:12px;color:var(--dim);">
    Newest: {newest[0] if isinstance(newest, (tuple,list)) else newest} @ {newest[1] if isinstance(newest, (tuple,list)) and len(newest)>1 else "?"}
  </div>
</div>"""


# =============================================================================
# FULL HTML ASSEMBLY
# =============================================================================

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0e1a;--surface:#111827;--card:#1a2235;--border:#2a3a5a;
--text:#f0f4ff;--dim:#8896b3;--cyan:#00e5ff;--green:#00e676;
--amber:#ffab00;--red:#ff5252;--purple:#b388ff}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
background:var(--bg);color:var(--text);padding:20px;min-height:100vh}
.header{display:flex;align-items:center;justify-content:space-between;
margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid var(--border)}
.logo{font-size:20px;font-weight:800;text-shadow:0 0 20px rgba(0,229,255,.4)}
.logo span{color:var(--cyan)}
.meta{display:flex;gap:16px;font-size:12px;color:var(--dim);align-items:center}
.badge{padding:3px 10px;border-radius:10px;font-weight:600;font-size:11px;
display:inline-block;}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:24px}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;margin-bottom:24px}
.card{background:var(--card);border:1px solid var(--border);
border-radius:14px;padding:20px}
.card h3{font-size:14px;color:var(--dim);margin-bottom:16px;
text-transform:uppercase;letter-spacing:.08em;display:flex;
align-items:center;justify-content:space-between;}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;color:var(--dim);font-size:11px;
text-transform:uppercase;padding:8px 6px;border-bottom:1px solid var(--border)}
td{padding:8px 6px;border-bottom:1px solid rgba(255,255,255,.03)}
.big-num{font-size:2rem;font-weight:800;color:var(--cyan)}
.health-row{display:flex;align-items:center;gap:8px;margin-bottom:4px;font-size:13px}
.dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.dot-green{background:var(--green);box-shadow:0 0 6px var(--green)}
.dot-red{background:var(--red);box-shadow:0 0 6px var(--red)}
.footer{text-align:center;color:var(--dim);font-size:11px;padding-top:16px;
border-top:1px solid var(--border);margin-top:20px}
@media(max-width:1000px){.grid,.grid-3{grid-template-columns:1fr}}
"""


def render_html(data: dict) -> str:
    integ = data["integrity"]
    overall_kind = _verdict_kind(integ["verdict"])
    overall_badge = _badge(f"System: {integ['verdict']}", overall_kind)
    timestamp_human = data["generated_at"][:19].replace("T", " ")

    body = f"""
<div class="header">
  <div class="logo">DARIO <span>Cognitive Health</span> Dashboard</div>
  <div class="meta">
    <span>Generated: {timestamp_human} UTC</span>
    {overall_badge}
  </div>
</div>

<div class="grid">
  {render_drift_card(data["drift"])}
  {render_integrity_card(data["integrity"])}
</div>

<div class="grid">
  {render_cot_card(data["cot"])}
  {render_semantic_card(data["semantic"])}
</div>

<div class="grid">
  {render_qvalue_card(data["qvalue"])}
  {render_synaptic_card(data["synaptic"])}
</div>

<div class="grid">
  {render_cron_card(data["cron"])}
  {render_embeddings_card(data["embeddings"])}
</div>

<div class="footer">
  DARIO Orchestrator — Cognitive subsystems audit · Sprints 1-4 + U11/U12/U14 wiring
</div>
"""

    return f"""<!DOCTYPE html>
<html lang="pt"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>DARIO Cognitive Dashboard</title>
<style>{CSS}</style></head><body>{body}</body></html>"""


def generate(output_path: Path = None, open_browser: bool = False) -> Path:
    out = output_path or DASHBOARD_FILE
    data = collect_all()
    html = render_html(data)
    out.write_text(html, encoding="utf-8")
    if open_browser:
        try:
            webbrowser.open(out.resolve().as_uri())
        except Exception:
            pass
    return out


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from licensing.license_guard import enforce_or_exit
        enforce_or_exit("cognitive_dashboard")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    p = argparse.ArgumentParser(description="DARIO Cognitive Dashboard")
    p.add_argument("--open", action="store_true", help="Open in browser after generating")
    p.add_argument("--json", "-j", action="store_true", help="Emit dataset only (debug)")
    p.add_argument("--output", help="Custom output path")
    args = p.parse_args()

    if args.json:
        data = collect_all()
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
        return 0

    output_path = Path(args.output) if args.output else None
    out = generate(output_path=output_path, open_browser=args.open)
    print(f"Generated: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

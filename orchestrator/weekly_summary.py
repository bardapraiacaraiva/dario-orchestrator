#!/usr/bin/env python3
"""
DARIO Weekly Cognitive Learning Summary
=========================================
Upgrade 18 (operational consolidation report).

Each day cron_daily produces a daily report (cron/daily-YYYY-MM-DD.yaml)
with jobs + alerts + warnings. Each session_boot promotes new patterns,
detects drift, captures dispatches. But nobody steps back to ask: "what
did the system actually LEARN this week?"

This module aggregates the last 7 days into a structured weekly summary:

  - Patterns crystallized (new SEM-*.yaml entries)
  - Auto-rules generated (new evolution/rules/*.yaml)
  - Drift detected / fixed / lingering
  - CoT overconfidence rate trend (week-over-week)
  - Synaptic weight deltas (top movers)
  - Q-value top movers
  - Integrity gate verdicts (any FAIL events)
  - Cron health (% of days OK)

Output is a markdown report saved to the Obsidian vault for permanent
visibility — `05 - Claude - IA/Outputs/YYYY-WW - Cognitive Weekly.md`.
Also serializable as JSON for programmatic consumption.

CLI:
    python weekly_summary.py                Generate this week's report
    python weekly_summary.py --week 2026-W20   Specific ISO week
    python weekly_summary.py --json
    python weekly_summary.py --no-save        Don't write to Obsidian
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
CRON_DIR = ORCH_DIR / "cron"
SEMANTIC_DIR = ORCH_DIR / "memory" / "semantic"
RULES_DIR = ORCH_DIR / "evolution" / "rules"
HINTS_DIR = ORCH_DIR / "prompt_hints"

OBSIDIAN_OUTPUTS = (Path.home() / "OneDrive" / "Documents" / "D.A.R.I.O" /
                    "05 - Claude - IA" / "Outputs")

sys.path.insert(0, str(ORCH_DIR))

try:
    from ruamel.yaml import YAML
    _yaml = YAML()

    def _load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return _yaml.load(f)
except ImportError:
    import yaml as _pyaml

    def _load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return _pyaml.safe_load(f)


# =============================================================================
# DATA COLLECTION
# =============================================================================

def _week_bounds(week_iso: str = None) -> tuple:
    """Returns (start_datetime, end_datetime, iso_label) UTC for the week.
    Default: current week."""
    if week_iso:
        # Parse YYYY-Www
        year, w = week_iso.split("-W")
        start = datetime.fromisocalendar(int(year), int(w), 1).replace(tzinfo=timezone.utc)
    else:
        now = datetime.now(timezone.utc)
        # Monday of current week
        start = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    end = start + timedelta(days=7)
    iso_year, iso_week, _ = start.isocalendar()
    label = f"{iso_year}-W{iso_week:02d}"
    return start, end, label


def collect_cron_days(start: datetime, end: datetime) -> list:
    if not CRON_DIR.exists():
        return []
    out = []
    for f in sorted(CRON_DIR.glob("daily-*.yaml")):
        try:
            date_str = f.stem.replace("daily-", "")
            d = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
            if d < start or d >= end:
                continue
            data = _load_yaml(str(f))
            if isinstance(data, dict):
                out.append({"date": date_str, **data})
        except Exception:
            continue
    return out


def collect_new_memories(start: datetime, end: datetime) -> list:
    """Semantic memories created within the week window."""
    out = []
    if not SEMANTIC_DIR.exists():
        return out
    for f in SEMANTIC_DIR.glob("SEM-*.yaml"):
        try:
            data = _load_yaml(str(f))
            if not isinstance(data, dict):
                continue
            created = data.get("created_at")
            if not created:
                continue
            try:
                ts = datetime.fromisoformat(created.replace("Z", "+00:00"))
            except Exception:
                continue
            if start <= ts < end:
                out.append({
                    "memory_id": data.get("memory_id"),
                    "name": data.get("name"),
                    "type": data.get("type", "unknown"),
                    "confidence": data.get("confidence"),
                    "episodes": len(data.get("promoted_from_episodes") or []),
                    "created_at": created,
                })
        except Exception:
            continue
    return sorted(out, key=lambda x: x["created_at"])


def collect_new_rules(start: datetime, end: datetime) -> list:
    """Auto-rules generated within the week."""
    out = []
    if not RULES_DIR.exists():
        return out
    for f in RULES_DIR.glob("auto-rule-*.yaml"):
        try:
            data = _load_yaml(str(f))
            if not isinstance(data, dict):
                continue
            gen = data.get("generated_at")
            if not gen:
                continue
            try:
                ts = datetime.fromisoformat(gen.replace("Z", "+00:00"))
            except Exception:
                continue
            if start <= ts < end:
                out.append({
                    "rule_id": data.get("rule_id"),
                    "skill": data.get("skill"),
                    "project": data.get("project"),
                    "boost": data.get("boost"),
                    "rationale": data.get("rationale", "")[:120],
                })
        except Exception:
            continue
    return out


def collect_new_hints(start: datetime, end: datetime) -> list:
    """Prompt hints created/updated within the week."""
    out = []
    if not HINTS_DIR.exists():
        return out
    for f in HINTS_DIR.glob("*.yaml"):
        try:
            data = _load_yaml(str(f))
            if not isinstance(data, dict):
                continue
            updated = data.get("updated_at")
            if not updated:
                continue
            try:
                ts = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            except Exception:
                continue
            if start <= ts < end:
                out.append({
                    "skill": data.get("skill"),
                    "hint_count": len(data.get("hints", [])),
                    "updated_at": updated,
                })
        except Exception:
            continue
    return out


def collect_drift_events(cron_days: list) -> dict:
    """Aggregate drift alerts/warnings from week's cron runs."""
    alert_evals = []
    drift_evals = []
    for day in cron_days:
        for job in day.get("jobs", []):
            if job.get("name") != "regression_check" or job.get("status") != "ok":
                continue
            o = job.get("output", {})
            for eid in (o.get("alerts") or []):
                alert_evals.append({"date": day["date"], "eval": eid})
            for eid in (o.get("drifting") or []):
                if eid not in (o.get("alerts") or []):
                    drift_evals.append({"date": day["date"], "eval": eid})
    return {"alerts": alert_evals, "drift_only": drift_evals}


def collect_cot_trend(cron_days: list) -> dict:
    """Overconfidence rate across the week's daily snapshots."""
    rates = []
    total_traces = 0
    for day in cron_days:
        for job in day.get("jobs", []):
            if job.get("name") != "dispatch_cot_stats" or job.get("status") != "ok":
                continue
            o = job.get("output", {})
            r = o.get("overconfidence_rate")
            if isinstance(r, (int, float)):
                rates.append({"date": day["date"], "rate": r})
            t = o.get("total_traces") or 0
            total_traces = max(total_traces, int(t))
    avg = round(sum(r["rate"] for r in rates) / len(rates), 3) if rates else 0
    return {
        "daily_rates": rates,
        "avg_rate": avg,
        "total_traces_end_of_week": total_traces,
    }


def collect_integrity_events(cron_days: list) -> list:
    """Days where integrity gate produced FAIL or WARN."""
    out = []
    for day in cron_days:
        for job in day.get("jobs", []):
            if job.get("name") != "integrity_gate" or job.get("status") != "ok":
                continue
            o = job.get("output", {})
            verdict = o.get("verdict")
            if verdict in ("FAIL", "WARN"):
                out.append({
                    "date": day["date"],
                    "verdict": verdict,
                    "failed_checks": o.get("failed_checks") or [],
                    "warned_checks": o.get("warned_checks") or [],
                })
    return out


def collect_qvalue_snapshot() -> dict:
    """End-of-week Q-value state."""
    try:
        from qvalue_memory_wire import stats, top_strategies
        s = stats()
        return {**s, "top_5": top_strategies(5)}
    except Exception as e:
        return {"error": str(e)[:100]}


def collect_synaptic_snapshot() -> dict:
    """End-of-week synaptic graph."""
    try:
        from synaptic_update import stats
        return stats()
    except Exception as e:
        return {"error": str(e)[:100]}


def collect_all(week_iso: str = None) -> dict:
    start, end, label = _week_bounds(week_iso)
    cron_days = collect_cron_days(start, end)
    return {
        "iso_week": label,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cron": {
            "days_run": len(cron_days),
            "days_ok": sum(1 for d in cron_days if d.get("status") == "ok"),
            "days_warn": sum(1 for d in cron_days if d.get("status") == "warn"),
            "days_alert": sum(1 for d in cron_days if d.get("status") == "alert"),
        },
        "new_memories": collect_new_memories(start, end),
        "new_rules": collect_new_rules(start, end),
        "new_hints": collect_new_hints(start, end),
        "drift": collect_drift_events(cron_days),
        "cot": collect_cot_trend(cron_days),
        "integrity": collect_integrity_events(cron_days),
        "qvalue_end_of_week": collect_qvalue_snapshot(),
        "synaptic_end_of_week": collect_synaptic_snapshot(),
    }


# =============================================================================
# RENDER
# =============================================================================

def render_markdown(data: dict) -> str:
    label = data["iso_week"]
    parts = [
        f"# Cognitive Weekly Summary — {label}",
        "",
        f"**Week:** {data['start'][:10]} → {data['end'][:10]}",
        f"**Generated:** {data['generated_at'][:19]} UTC",
        "",
        "## Cron Daily Health",
        "",
        f"- Days with cron run: **{data['cron']['days_run']} / 7**",
        f"- OK days: {data['cron']['days_ok']}",
        f"- WARN days: {data['cron']['days_warn']}",
        f"- ALERT days: {data['cron']['days_alert']}",
        "",
    ]

    # Learning section
    parts += ["## What the System Learned", ""]
    mem = data["new_memories"]
    if mem:
        parts.append(f"### New semantic memories ({len(mem)})")
        by_type = Counter(m.get("type", "unknown") for m in mem)
        for t, c in by_type.items():
            parts.append(f"- {t}: **{c}**")
        parts.append("")
        for m in mem[:8]:
            conf = m.get("confidence")
            conf_str = f" · conf {conf:.2f}" if isinstance(conf, (int, float)) else ""
            parts.append(f"  - `{m.get('name')}` ({m.get('episodes', 0)} eps{conf_str})")
        parts.append("")
    else:
        parts += ["### No new semantic memories this week", ""]

    rules = data["new_rules"]
    if rules:
        parts.append(f"### New auto-rules ({len(rules)})")
        for r in rules:
            parts.append(
                f"- **{r.get('skill')}** @ {r.get('project') or '*'}  "
                f"boost={r.get('boost')} — {r.get('rationale', '')}"
            )
        parts.append("")

    hints = data["new_hints"]
    if hints:
        parts.append(f"### New/updated prompt hints ({len(hints)})")
        for h in hints:
            parts.append(f"- **{h.get('skill')}** — {h.get('hint_count')} hint(s)")
        parts.append("")

    # Drift section
    drift = data["drift"]
    parts += ["## Quality Drift Events", ""]
    if drift["alerts"]:
        parts.append(f"### Alerts ({len(drift['alerts'])})")
        for a in drift["alerts"]:
            parts.append(f"- {a['date']} · `{a['eval']}` — drift alert")
        parts.append("")
    if drift["drift_only"]:
        parts.append(f"### Drift (sub-alert) ({len(drift['drift_only'])})")
        for d in drift["drift_only"][:10]:
            parts.append(f"- {d['date']} · `{d['eval']}`")
        parts.append("")
    if not drift["alerts"] and not drift["drift_only"]:
        parts += ["No drift events this week.", ""]

    # CoT trend
    cot = data["cot"]
    parts += [
        "## Dispatch Reasoning",
        "",
        f"- Total CoT traces (end of week): **{cot.get('total_traces_end_of_week', 0)}**",
        f"- Average overconfidence rate: **{cot.get('avg_rate', 0)}**",
    ]
    if cot.get("daily_rates"):
        for r in cot["daily_rates"]:
            parts.append(f"  - {r['date']}: {r['rate']}")
    parts.append("")

    # Integrity
    integ = data["integrity"]
    parts += ["## Integrity Gate Events", ""]
    if integ:
        for e in integ:
            parts.append(
                f"- {e['date']} · **{e['verdict']}**  "
                f"failed={e.get('failed_checks') or '—'}  "
                f"warned={e.get('warned_checks') or '—'}"
            )
    else:
        parts.append("No integrity issues this week — all PASS.")
    parts.append("")

    # End-of-week snapshots
    qv = data["qvalue_end_of_week"]
    sn = data["synaptic_end_of_week"]
    parts += ["## State Snapshot (end of week)", ""]
    if isinstance(qv, dict) and "total_episodes" in qv:
        parts.append(
            f"- **Q-value memory:** {qv['total_episodes']} episodes · "
            f"{qv.get('distinct_skills', 0)} distinct skills · "
            f"avg Q={qv.get('avg_q_value', 0)}"
        )
        if qv.get("top_5"):
            parts.append("  Top strategies:")
            for s in qv["top_5"][:5]:
                parts.append(
                    f"  - `{s.get('skill')}` Q={s.get('q_value')} "
                    f"avg={s.get('avg_score')} visits={s.get('visits')}"
                )
    if isinstance(sn, dict) and "total_pairs" in sn:
        parts.append(
            f"- **Synaptic graph:** {sn['total_pairs']} pairs · "
            f"{sn.get('active_pairs', 0)} active · "
            f"avg weight {sn.get('avg_weight', 0)} · "
            f"co-acts {sn.get('total_co_activations', 0)}"
        )
    parts.append("")

    parts += [
        "---",
        "*Generated by DARIO weekly_summary (Upgrade 18). Source: "
        "cron/daily-*.yaml + memory/semantic/SEM-*.yaml + evolution/rules/ "
        "+ prompt_hints/. Verbatim aggregation — no interpretive analysis.*",
    ]

    return "\n".join(parts)


def _clean_obsidian_shadows(filename: str) -> int:
    """The Obsidian vault has `newFileLocation: folder` + `newFileFolderPath:
    00 - Inbox` configured. When we write externally to a destination folder,
    Obsidian creates empty shadow copies under `00 - Inbox/` mirroring the
    target path. These shadows have size 0 and pollute the vault.

    This helper removes any 0-byte file in the Inbox that matches the basename
    of our just-written file. Returns the count removed.
    """
    vault_root = OBSIDIAN_OUTPUTS.parent.parent  # vault root (D.A.R.I.O/)
    inbox = vault_root / "00 - Inbox"
    if not inbox.exists():
        return 0
    removed = 0
    base = Path(filename).stem  # strip .md
    # Search recursively for shadows: exact name or `<name> N.md` (auto-rename)
    for shadow in inbox.rglob("*.md"):
        try:
            stem = shadow.stem
            if stem == base or stem.startswith(base + " ") and stem[len(base) + 1:].strip().isdigit():
                if shadow.stat().st_size == 0:
                    shadow.unlink()
                    removed += 1
        except Exception:
            continue
    return removed


def save_to_obsidian(label: str, content: str) -> Path:
    OBSIDIAN_OUTPUTS.mkdir(parents=True, exist_ok=True)
    filename = f"{label} - Cognitive Weekly.md"
    path = OBSIDIAN_OUTPUTS / filename
    path.write_text(content, encoding="utf-8")
    # Clean shadows created by Obsidian's "newFileLocation: folder" behaviour
    try:
        _clean_obsidian_shadows(filename)
    except Exception:
        pass
    return path


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from license_guard import enforce_or_exit
        enforce_or_exit("weekly_summary")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    p = argparse.ArgumentParser(description="DARIO Weekly Cognitive Summary")
    p.add_argument("--week", help="ISO week (e.g. 2026-W20). Default: current.")
    p.add_argument("--no-save", action="store_true",
                   help="Don't write to Obsidian")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    data = collect_all(week_iso=args.week)

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
        return 0

    md = render_markdown(data)
    print(md)
    if not args.no_save:
        path = save_to_obsidian(data["iso_week"], md)
        print(f"\n[saved] {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

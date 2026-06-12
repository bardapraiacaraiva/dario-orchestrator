#!/usr/bin/env python3
"""DARIO compute_client_stats — Aggregator per cliente.

Parses .captured_outputs.yaml + scans OBS_OUTPUTS/ folder, agrupa por
cliente identificado via filename pattern.

Usage:
    python scripts/compute_client_stats.py            # update + print
    python scripts/compute_client_stats.py --check    # print only
    python scripts/compute_client_stats.py --json     # JSON output
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

ORCH = Path.home() / ".claude" / "orchestrator"
REGISTRY_PATH = ORCH / ".captured_outputs.yaml"
CLIENT_STATS_PATH = ORCH / "quality" / "client-stats.yaml"
CLIENT_REVENUE_PATH = ORCH / "quality" / "client-revenue.yaml"
OBS_OUTPUTS = Path.home() / "OneDrive" / "Documents" / "D.A.R.I.O" / "05 - Claude - IA" / "Outputs"

try:
    from ruamel.yaml import YAML
    _y = YAML(); _y.preserve_quotes = True; _y.width = 200
    def load_y(p):
        with open(p, encoding='utf-8') as f: return _y.load(f) or {}
    def dump_y(d, p):
        with open(p, 'w', encoding='utf-8') as f: _y.dump(d, f)
except ImportError:
    import yaml
    def load_y(p):
        with open(p, encoding='utf-8') as f: return yaml.safe_load(f) or {}
    def dump_y(d, p):
        with open(p, 'w', encoding='utf-8') as f: yaml.safe_dump(d, f, sort_keys=False)


CLIENT_ALIASES = {
    "atrium premium re": "atrium-premium-re",
    "atrium premium": "atrium-premium-re",
    "atrium golden visa": "atrium-golden-visa",
    "atrium golden": "atrium-golden-visa",
    "atrium": "atrium-premium-re",
    "lucas lusoconta": "lucas-lusoconta",
    "lucas + lusaconta": "lucas-lusoconta",
    "lucas + lusoconta": "lucas-lusoconta",
    "lucas v2": "lucas-lusoconta",
    "lucas": "lucas-lusoconta",
    "lusoconta": "lucas-lusoconta",
    "cuidai": "cuidai",
    "saquei": "saquei",
    "credito": "saquei",
    "patudos": "pupli",
    "pupli": "pupli",
    "vivenda creative home": "vivenda",
    "vivenda": "vivenda",
    "lisbon dog care by marcela": "lisbon-dog-care",
    "lisbon dog care": "lisbon-dog-care",
    "atelier ai": "atelier-ai",
    "tributario.ai": "tributario-ai",
    "tributário.ai": "tributario-ai",
    "arrecada.gov": "arrecada-gov",
    "arrecada": "arrecada-gov",
    "clawcode": "clawcode",
    "claw-code": "clawcode",
    "adgeniuspro": "adgeniuspro",
    "dario": "dario-internal",
    "dario v": "dario-internal",
    "memory & dreaming": "dario-internal",
    "instalacao": "dario-internal",
    "automation solution": "automation-solution",
    "xsquads": "dario-internal",
    "auditoria web": "internal-audits",
    "orchestrator": "dario-internal",
    "session final": "dario-internal",
    "quality sprint": "dario-internal",
    "quality tooling": "dario-internal",
    "installer npx": "dario-internal",
    "delivery_ready_rate": "dario-internal",
    "dspy compile": "dario-internal",
    "caminho b": "dario-internal",
    "fix trio": "dario-internal",
}

# Client identity/status metadata. Revenue fields live em quality/client-revenue.yaml (editável).
CLIENT_METADATA = {
    "atrium-premium-re": {"name": "Atrium Premium Real Estate", "status": "active", "engagement_started": "2026-03-13", "note": "blocked by Thiago decisions"},
    "atrium-golden-visa": {"name": "Atrium Golden Visa", "status": "live", "engagement_started": "2026-02-01", "deployment": "herbalifeportugal.com"},
    "lucas-lusoconta": {"name": "LUCAS / LUSOconta", "status": "active", "engagement_started": "2026-01-15", "deployment": "flipperboys.com"},
    "cuidai": {"name": "Cuidaí BR", "status": "wave-0-complete", "engagement_started": "2026-05-01"},
    "saquei": {"name": "SAQUEI BR", "status": "gate-1-complete", "deployment": "saquei.vercel.app"},
    "pupli": {"name": "PUPLI (ex-Patudos)", "status": "live-vps"},
    "vivenda": {"name": "Vivenda Creative Home", "status": "active"},
    "lisbon-dog-care": {"name": "Lisbon Dog Care", "status": "active"},
    "atelier-ai": {"name": "Atelier AI", "status": "mvp-building"},
    "tributario-ai": {"name": "Tributário.AI", "status": "founder-day-0-pending"},
    "arrecada-gov": {"name": "ARRECADA.GOV", "status": "mvp-live", "note": "success-fee 12%"},
    "clawcode": {"name": "Clawcode Agent", "status": "archived"},
    "adgeniuspro": {"name": "adgeniuspro", "status": "advisory"},
    "dario-internal": {"name": "DARIO Internal Work", "status": "internal"},
}


def load_revenue() -> dict:
    """Load user-editable revenue YAML. Returns {} if missing.

    Schema per client: monthly_value, currency, billing_status, billing_model,
    contract_start, contract_end, last_invoice, notes (all optional).
    """
    if not CLIENT_REVENUE_PATH.exists():
        return {}
    data = load_y(CLIENT_REVENUE_PATH)
    return data.get("clients", {}) or {}


def infer_client(filename: str) -> str | None:
    base = Path(filename).stem
    parts = [p.strip() for p in base.split(" - ")]
    if len(parts) < 2:
        return None
    client_raw = (parts[1] if len(parts) >= 3 else parts[0]).lower()
    for alias_key, normalized in CLIENT_ALIASES.items():
        if alias_key in client_raw:
            return normalized
    return None


def compute() -> dict:
    registry = load_y(REGISTRY_PATH)
    captured = registry.get("captured", {})
    revenue = load_revenue()

    by_client = defaultdict(lambda: {
        "deliverables": [], "scores": [],
        "yes_count": 0, "needs_review_count": 0, "no_count": 0,
        "skills_used": defaultdict(int),
    })

    for filename, entry in captured.items():
        client = infer_client(filename)
        if not client:
            continue
        by_client[client]["deliverables"].append(filename)
        score = entry.get("score")
        if isinstance(score, (int, float)):
            by_client[client]["scores"].append(score)
        v = entry.get("verdict")
        if v == "yes": by_client[client]["yes_count"] += 1
        elif v == "needs-review": by_client[client]["needs_review_count"] += 1
        elif v == "no": by_client[client]["no_count"] += 1
        skill = entry.get("skill", "unknown")
        by_client[client]["skills_used"][skill] += 1

    obs_files = list(OBS_OUTPUTS.glob("*.md")) if OBS_OUTPUTS.exists() else []
    obs_per_client = defaultdict(int)
    for f in obs_files:
        c = infer_client(f.name)
        if c: obs_per_client[c] += 1

    result = {}
    all_clients = set(by_client.keys()) | set(obs_per_client.keys()) | set(CLIENT_METADATA.keys())
    for client_id in all_clients:
        data = by_client.get(client_id, {"deliverables": [], "scores": [], "yes_count": 0,
                                          "needs_review_count": 0, "no_count": 0, "skills_used": {}})
        meta = CLIENT_METADATA.get(client_id, {"name": client_id, "status": "unknown"})
        scored = len(data["scores"])
        total_obs = obs_per_client.get(client_id, 0)
        avg = round(sum(data["scores"]) / scored, 1) if scored else None
        decided = data["yes_count"] + data["needs_review_count"] + data["no_count"]
        rate = round(100.0 * data["yes_count"] / decided, 1) if decided else None

        rev = revenue.get(client_id, {}) or {}
        result[client_id] = {
            "name": meta.get("name", client_id),
            "status": meta.get("status"),
            "monthly_value": rev.get("monthly_value"),
            "currency": rev.get("currency"),
            "billing_status": rev.get("billing_status"),
            "billing_model": rev.get("billing_model"),
            "contract_start": rev.get("contract_start"),
            "last_invoice": rev.get("last_invoice"),
            "revenue_notes": rev.get("notes"),
            "engagement_started": meta.get("engagement_started"),
            "deployment": meta.get("deployment"),
            "note": meta.get("note"),
            "total_outputs_obsidian": total_obs,
            "scored_count": scored,
            "avg_score": avg,
            "delivery_ready_rate_pct": rate,
            "yes_count": data["yes_count"],
            "needs_review_count": data["needs_review_count"],
            "no_count": data["no_count"],
            "top_skills": dict(sorted(dict(data["skills_used"]).items(), key=lambda x: -x[1])[:5]),
        }

    return result


def print_summary(stats: dict):
    print("=== Per-Client Stats ===\n")
    sorted_clients = sorted(stats.items(), key=lambda x: -(x[1].get("total_outputs_obsidian") or 0))
    for client_id, s in sorted_clients:
        name = (s["name"] or client_id)[:33]
        scored = s.get("scored_count", 0)
        avg = s.get("avg_score")
        dr = s.get("delivery_ready_rate_pct")
        status = (s.get("status") or "?")[:18]
        value = s.get("monthly_value")
        currency = s.get("currency", "")
        total_obs = s.get("total_outputs_obsidian", 0)

        avg_str = f"avg {avg}" if avg else "no scores"
        dr_str = f"{dr}% yes" if dr is not None else "—"
        value_str = f"{currency}{value}/mo" if value else "—"

        print(f"  {name:33s} | obs {total_obs:3} | scored {scored:2} | {avg_str:>10} | {dr_str:>8} | {status:20s} | {value_str}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    stats = compute()

    if args.json:
        print(json.dumps(stats, indent=2, default=str))
    else:
        print_summary(stats)

    if not args.check:
        CLIENT_STATS_PATH.parent.mkdir(parents=True, exist_ok=True)
        dump_y({
            "computed_at": datetime.now(UTC).isoformat(),
            "total_clients": len(stats),
            "clients": stats,
        }, CLIENT_STATS_PATH)
        print(f"\nSaved: {CLIENT_STATS_PATH}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

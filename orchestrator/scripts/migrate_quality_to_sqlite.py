#!/usr/bin/env python3
"""Migrate existing YAML/JSONL quality logs into SQLite (db.py v3 schema).

One-shot migration after audit finding "YAML as database is fragile":
  - quality/polished_production_runs.yaml → polished_runs table
  - quality/api_spend_log.yaml + .jsonl    → api_spend table

Idempotent: skips rows already present in DB (matches on ts + caller/skill).
Safe to re-run. Logs how many rows imported, skipped, failed.

Usage:
    python -m scripts.migrate_quality_to_sqlite              # dry run
    python -m scripts.migrate_quality_to_sqlite --apply      # actually insert
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

POLISHED_YAML = ORCH_DIR / "quality" / "polished_production_runs.yaml"
SPEND_YAML = ORCH_DIR / "quality" / "api_spend_log.yaml"
SPEND_JSONL = ORCH_DIR / "quality" / "api_spend_log.jsonl"


def _load_polished_yaml() -> list[dict]:
    if not POLISHED_YAML.exists():
        return []
    with open(POLISHED_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("runs") or []


def _load_spend_entries() -> list[dict]:
    entries: list[dict] = []
    if SPEND_JSONL.exists():
        with open(SPEND_JSONL, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    if not entries and SPEND_YAML.exists():
        with open(SPEND_YAML, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        entries = data.get("entries") or []
    return entries


def migrate_polished(db, dry: bool) -> dict:
    entries = _load_polished_yaml()
    if not entries:
        return {"source": "polished_yaml", "found": 0, "inserted": 0, "skipped": 0, "errors": 0}

    # Dedup against DB by ts+skill+client
    existing = {(r["ts"], r["skill"], r["client"]) for r in db.get_polished_runs()}

    inserted = skipped = errors = 0
    for e in entries:
        key = (e.get("ts"), e.get("skill"), e.get("client"))
        if key in existing:
            skipped += 1
            continue
        if dry:
            inserted += 1
            continue
        try:
            db.record_polished_run(
                skill=e["skill"],
                client=e["client"],
                v1_score=int(e["v1_score"]),
                v2_score=int(e["v2_score"]) if e.get("v2_score") is not None else None,
                final=e["final"],
                gate_decision=e["gate_decision"],
                briefing_summary=e.get("briefing_summary", ""),
                status_mix=e.get("status_mix", ""),
                notes=e.get("notes", ""),
                ts=e.get("ts"),
            )
            inserted += 1
        except Exception as ex:
            print(f"  [polished] error on {key}: {ex}", file=sys.stderr)
            errors += 1
    return {"source": "polished_yaml", "found": len(entries),
            "inserted": inserted, "skipped": skipped, "errors": errors}


def migrate_spend(db, dry: bool) -> dict:
    entries = _load_spend_entries()
    if not entries:
        return {"source": "spend_jsonl_or_yaml", "found": 0,
                "inserted": 0, "skipped": 0, "errors": 0}

    existing = {(r["ts"], r["caller"], r["model"], r["total_tokens"])
                for r in db.get_api_spend()}

    inserted = skipped = errors = 0
    for e in entries:
        key = (e.get("ts"), e.get("caller"), e.get("model"), e.get("total_tokens"))
        if key in existing:
            skipped += 1
            continue
        if dry:
            inserted += 1
            continue
        try:
            db.record_api_spend(
                caller=e["caller"],
                model=e["model"],
                input_tokens=int(e["input_tokens"]),
                output_tokens=int(e["output_tokens"]),
                cost_usd=float(e["cost_usd"]),
                ts=e.get("ts"),
            )
            inserted += 1
        except Exception as ex:
            print(f"  [spend] error on {key}: {ex}", file=sys.stderr)
            errors += 1
    return {"source": "spend_jsonl_or_yaml", "found": len(entries),
            "inserted": inserted, "skipped": skipped, "errors": errors}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Actually insert into SQLite (default: dry run)")
    args = ap.parse_args()

    from db import DB
    db = DB()

    label = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== Migration to SQLite v3 ({label}) ===")

    polished_result = migrate_polished(db, dry=not args.apply)
    spend_result = migrate_spend(db, dry=not args.apply)

    for r in (polished_result, spend_result):
        print(f"  {r['source']}: found={r['found']} "
              f"inserted={r['inserted']} skipped={r['skipped']} "
              f"errors={r['errors']}")

    if not args.apply:
        print("\n(dry run — pass --apply to actually insert)")
    else:
        print("\nDone. SQLite is now the source of truth for polished_runs + api_spend.")
        print("YAML/JSONL files retained as backup; can be archived after 30d.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

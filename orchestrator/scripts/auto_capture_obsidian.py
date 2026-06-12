#!/usr/bin/env python3
"""
DARIO auto-capture — Scans Obsidian Outputs/ folder for new client deliverables
and auto-routes them through score_real_output.py.

Eliminates the manual step "remember to score after each delivery".

How it works:
  1. Scan `D.A.R.I.O/05 - Claude - IA/Outputs/` for .md files
  2. Compare against `.captured_outputs.yaml` registry (skip already-seen)
  3. For each new file:
     - Parse skill from filename or frontmatter `type:` field
     - Parse context from filename (client name, project type)
     - Call score_real_output.py (LLM judge mode by default)
  4. Register the file as captured (with score, verdict, timestamp)
  5. If score < 90 and not --human-verdict mode, file is auto-queued
     to human_review_queue (via score_real_output.py integration)

Usage:
    # Capture new outputs (default: LLM judge, ~$0.01 per new file)
    python scripts/auto_capture_obsidian.py

    # Dry-run: see what would capture without API calls
    python scripts/auto_capture_obsidian.py --dry-run

    # Limit to N new files (avoid runaway costs)
    python scripts/auto_capture_obsidian.py --limit 10

    # Force re-capture even if already in registry
    python scripts/auto_capture_obsidian.py --file "specific.md" --force

    # Show capture stats
    python scripts/auto_capture_obsidian.py --stats

Cost estimate: ~$0.01 per new file (Haiku 4.5 judge, ~600 tokens output).
Run via cron daily or every N hours.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH = Path.home() / ".claude" / "orchestrator"
OBS_OUTPUTS = Path.home() / "OneDrive" / "Documents" / "D.A.R.I.O" / "05 - Claude - IA" / "Outputs"
REGISTRY_PATH = ORCH / ".captured_outputs.yaml"
SCORE_SCRIPT = ORCH / "score_real_output.py"

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


# Skill inference patterns (filename hints → skill name)
SKILL_PATTERNS = [
    # Exact match patterns (prefix-of-filename → skill)
    (r"(?i)action.pack|unblock", "dario-proposal"),
    (r"(?i)(financial.model|p&l|cash.flow|forecast)", "dario-financial-model"),
    (r"(?i)(brand.strategy|brand.identity|positioning|brand.workshop)", "dario-brand"),
    (r"(?i)(naming.workshop|brand.naming)", "dario-naming"),
    (r"(?i)(proposal|orcamento|orçamento)", "dario-proposal"),
    (r"(?i)(pitch.deck|investor.pitch|pitch)", "dario-pitch"),
    (r"(?i)(sales.pipeline|pipeline|outbound)", "dario-pipeline"),
    (r"(?i)(diagnose|diagnost|audit.holístic|holistic.audit)", "dario-diagnose"),
    (r"(?i)(content.calendar|editorial.calendar)", "dario-content"),
    (r"(?i)(cwv|core.web.vitals|lighthouse.fix)", "dario-cwv-fix"),
    (r"(?i)(wp.audit|wordpress.audit)", "dario-wp-audit"),
    (r"(?i)(seo.audit)", "seo-audit"),
    (r"(?i)(sitemap)", "seo-sitemap"),
    (r"(?i)(schema)", "seo-schema"),
    (r"(?i)(hreflang|i18n)", "seo-hreflang"),
    (r"(?i)(moodboard|materiais)", "diva-materials"),
    (r"(?i)(client.onboard|onboarding)", "dario-client-onboard"),
    (r"(?i)(validation|mom.test|lean.validation)", "a360-validacao"),
    (r"(?i)(produto|roadmap.q[1-4]|product.roadmap)", "dario-produto"),
    (r"(?i)(offer|grand.slam)", "dario-offer"),
    (r"(?i)(funnel|funil)", "dario-funnel"),
]


def infer_skill_from_filename(filename: str) -> str | None:
    """Try to infer the skill name from a filename."""
    for pattern, skill in SKILL_PATTERNS:
        if re.search(pattern, filename):
            return skill
    return None


def infer_context_from_filename(filename: str) -> str:
    """Extract context (client + project) from filename pattern.

    Pattern expected: YYYY-MM-DD - <Client> - <Title>.md
    """
    base = Path(filename).stem
    parts = [p.strip() for p in base.split(" - ")]
    if len(parts) >= 2:
        # First part is date, second is client (usually)
        client = parts[1] if len(parts) >= 3 else parts[0]
        title = parts[-1] if len(parts) >= 3 else (parts[1] if len(parts) >= 2 else "")
        return f"{client} — {title}"
    return base


def parse_frontmatter_skill(file_path: Path) -> str | None:
    """Try to find skill via YAML frontmatter `type:` field."""
    try:
        text = file_path.read_text(encoding="utf-8")[:1500]
        m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL | re.MULTILINE)
        if not m:
            return None
        fm = m.group(1)
        type_m = re.search(r"^type:\s*([^\n]+)", fm, re.MULTILINE)
        if type_m:
            t = type_m.group(1).strip().lower()
            # Map common type values to skill names
            type_to_skill = {
                "proposal": "dario-proposal",
                "action-proposal": "dario-proposal",
                "financial-model": "dario-financial-model",
                "brand-strategy": "dario-brand",
                "naming-workshop": "dario-naming",
                "diagnostic": "dario-diagnose",
                "cwv-fix-report": "dario-cwv-fix",
                "editorial-calendar": "dario-content",
                "target-account-list": "dario-pipeline",
                "sales-pipeline": "dario-pipeline",
                "pitch-deck": "dario-pitch",
                "moodboard": "diva-materials",
            }
            return type_to_skill.get(t)
    except Exception:
        pass
    return None


def find_skill(file_path: Path) -> str | None:
    """Combined skill inference (frontmatter first, then filename)."""
    skill = parse_frontmatter_skill(file_path)
    if skill:
        return skill
    return infer_skill_from_filename(file_path.name)


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        return load_y(REGISTRY_PATH)
    return {"version": 1, "captured": {}, "last_scan": None}


def save_registry(registry: dict):
    registry["last_scan"] = datetime.now(UTC).isoformat()
    dump_y(registry, REGISTRY_PATH)


def scan_outputs() -> list[Path]:
    """Return all .md files in OBS_OUTPUTS, sorted by mtime descending (newest first)."""
    if not OBS_OUTPUTS.exists():
        return []
    files = list(OBS_OUTPUTS.glob("*.md"))
    files.sort(key=lambda p: -p.stat().st_mtime)
    return files


def score_one(file_path: Path, skill: str, context: str, dry_run: bool = False) -> dict | None:
    """Call score_real_output.py via subprocess. Returns result dict or None."""
    if dry_run:
        return {"dry_run": True, "skill": skill, "context": context[:120]}

    cmd = [
        sys.executable, str(SCORE_SCRIPT),
        "--skill", skill,
        "--output", str(file_path),
        "--context", context[:800],
        "--json",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=str(ORCH))
        m = re.search(r"\{[\s\S]+\}", proc.stdout)
        if m:
            return json.loads(m.group(0))
        return {"error": "no JSON in output", "stderr": proc.stderr[:200]}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)[:200]}


def cmd_backfill(args) -> int:
    """Mark files as already-captured based on skill-metrics.yaml audit trail.

    Reads each skill's production_audit list and marks matching filenames in
    the registry as already-captured (so they're skipped on next live run).
    Use this AFTER scoring files manually to avoid double-capture.
    """
    metrics_path = ORCH / "quality" / "skill-metrics.yaml"
    if not metrics_path.exists():
        print(f"error: {metrics_path} not found")
        return 1

    metrics = load_y(metrics_path)
    skills = metrics.get("skills", {}) or {}
    registry = load_registry()
    captured = registry.get("captured", {})

    backfilled = 0
    for skill_name, skill_data in skills.items():
        if not isinstance(skill_data, dict):
            continue
        audit = skill_data.get("production_audit", []) or []
        for entry in audit:
            preview = entry.get("output_preview", "") or ""
            # Try to match audit entries to actual files via context_preview/output_preview
            # For now use a marker — capture all files that match a skill's domain
            pass

    # Simpler backfill: mark ALL files in OBS_OUTPUTS that match captured patterns
    files = scan_outputs()
    for f in files:
        if f.name in captured:
            continue
        skill = find_skill(f)
        if not skill:
            continue
        # Mark as captured with placeholder data — will be re-scored if --force
        captured[f.name] = {
            "skill": skill,
            "captured_at": datetime.now(UTC).isoformat(),
            "score": None,
            "verdict": "backfilled",
            "queue_id": None,
            "file_mtime": f.stat().st_mtime,
            "backfill": True,
        }
        backfilled += 1
        if args.limit and backfilled >= args.limit:
            break

    registry["captured"] = captured
    save_registry(registry)
    print(f"=== Backfilled {backfilled} files (skip on future captures unless --force) ===")
    return 0


def cmd_capture(args) -> int:
    registry = load_registry()
    captured = registry.get("captured", {})

    files = scan_outputs()
    if not files:
        print("No .md files found in OBS_OUTPUTS")
        return 0

    new_files = []
    for f in files:
        key = f.name
        if not args.force and key in captured:
            continue
        skill = find_skill(f)
        if not skill and not args.force:
            continue  # skip files we can't infer skill for
        new_files.append((f, skill or "unknown"))

    if args.file:
        new_files = [(f, s) for f, s in new_files if f.name == args.file or args.file in f.name]

    if args.limit:
        new_files = new_files[: args.limit]

    if not new_files:
        print(f"No new files to capture (registry has {len(captured)} entries)")
        return 0

    print(f"=== Capturing {len(new_files)} new outputs ===\n")
    success = 0
    skipped = 0

    for i, (f, skill) in enumerate(new_files, 1):
        context = infer_context_from_filename(f.name)
        print(f"[{i}/{len(new_files)}] {skill:25s}  {f.name[:70]}")

        if args.dry_run:
            print(f"             [dry-run] would score with context: {context[:60]}")
            continue

        result = score_one(f, skill, context, dry_run=False)
        if result is None or "error" in result:
            print(f"             ✗ ERROR: {result.get('error', '?') if result else 'no result'}")
            skipped += 1
            continue

        verdict = result.get("verdict") or result.get("deliverable", "?")
        score = result.get("score", "?")
        print(f"             ✓ {score}/100 [{verdict}]  (rate now: {result.get('delivery_ready_rate_pct', '?')}%)")

        # Register
        captured[f.name] = {
            "skill": skill,
            "captured_at": datetime.now(UTC).isoformat(),
            "score": score,
            "verdict": verdict,
            "queue_id": result.get("queue_id"),
            "file_mtime": f.stat().st_mtime,
        }
        success += 1

    if not args.dry_run:
        registry["captured"] = captured
        save_registry(registry)

    print("\n=== Done ===")
    print(f"  Captured: {success}")
    print(f"  Skipped (errors): {skipped}")
    print(f"  Total registry entries: {len(captured)}")
    return 0


def cmd_stats(args) -> int:
    registry = load_registry()
    captured = registry.get("captured", {})

    print("=== Auto-capture Registry Stats ===\n")
    print(f"  Total captured:    {len(captured)}")
    print(f"  Last scan:         {registry.get('last_scan', 'never')}")

    if captured:
        verdicts = {"yes": 0, "needs-review": 0, "no": 0, "?": 0}
        skills = {}
        for entry in captured.values():
            v = entry.get("verdict", "?")
            verdicts[v if v in verdicts else "?"] = verdicts.get(v if v in verdicts else "?", 0) + 1
            s = entry.get("skill", "unknown")
            skills[s] = skills.get(s, 0) + 1

        print("\n  Verdict distribution:")
        for v, n in verdicts.items():
            if n: print(f"    {v:15s} {n}")

        print("\n  Per skill (top 10):")
        for s, n in sorted(skills.items(), key=lambda x: -x[1])[:10]:
            print(f"    {s:25s} {n}")

    # Show files in OBS_OUTPUTS that AREN'T captured (potential queue)
    files = scan_outputs()
    uncaptured = [f.name for f in files if f.name not in captured]
    print(f"\n  Uncaptured files in Outputs/: {len(uncaptured)}")
    if uncaptured[:5]:
        print("  Sample (5 newest):")
        for n in uncaptured[:5]:
            skill = find_skill(OBS_OUTPUTS / n) or "(unknown — skip)"
            print(f"    [{skill:25s}] {n[:70]}")

    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Auto-capture Obsidian outputs through score_real_output.py")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--limit", type=int)
    p.add_argument("--file", help="Process only a specific filename (substring match)")
    p.add_argument("--force", action="store_true", help="Re-capture already-captured files")
    p.add_argument("--stats", action="store_true", help="Show registry stats")
    p.add_argument("--backfill", action="store_true",
                   help="Mark all existing matched files as captured (no API calls). Use ONCE to pre-populate registry, then live captures only process new outputs.")
    args = p.parse_args()

    if args.stats:
        return cmd_stats(args)
    if args.backfill:
        return cmd_backfill(args)

    return cmd_capture(args)


if __name__ == "__main__":
    sys.exit(main())

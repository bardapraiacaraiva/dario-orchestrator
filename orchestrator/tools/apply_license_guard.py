#!/usr/bin/env python3
"""
Apply license_guard.enforce_or_exit() to all CLI main() entry points.
One-shot script that modifies orchestrator scripts to add license enforcement.

Adds at the top of each main():
    from licensing.license_guard import enforce_or_exit
    enforce_or_exit("<component>")

Idempotent: detects if already present and skips.

Run from orchestrator root:
    python tools/apply_license_guard.py --dry-run
    python tools/apply_license_guard.py --apply
"""

import argparse
import re
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"

# Files to harden: each (filename, component_name)
TARGETS = [
    ("executor.py",            "executor"),
    ("dispatch_engine.py",     "dispatch_engine"),
    ("chain_executor.py",      "chain_executor"),
    ("cron_daily.py",          "cron_daily"),
    ("cognitive_dashboard.py", "cognitive_dashboard"),
    ("webhook_dispatcher.py",  "webhook_dispatcher"),
    ("weekly_summary.py",      "weekly_summary"),
    ("eval_drilldown.py",      "eval_drilldown"),
    ("prompt_hints.py",        "prompt_hints"),
    ("episode_promoter.py",    "episode_promoter"),
    ("dispatch_cot.py",        "dispatch_cot"),
    ("dynamic_branch.py",      "dynamic_branch"),
    ("confidence_engine.py",   "confidence_engine"),
    ("ethical_gate.py",        "ethical_gate"),
    ("semantic_dispatch.py",   "semantic_dispatch"),
    ("synaptic_update.py",     "synaptic_update"),
    ("qvalue_memory_wire.py",  "qvalue_memory_wire"),
    ("chain_validator.py",     "chain_validator"),
    ("golden_eval.py",         "golden_eval"),
]

# Files that are EXPLICITLY exempt (never patched)
EXEMPT = {
    "license_manager.py",      # would self-recurse
    "license_guard.py",        # core of enforcement
    "obsidian_safe_write.py",  # utility, no orchestrator coupling
    "tools/integrity_gate.py", # read-only audit
    "tools/seed_goldens.py",   # data prep
    "tools/apply_cuidai_audit.py",
    "tools/apply_license_guard.py",
}

# Marker line that indicates patch already applied
MARKER = "# license_guard wired (v11.1+ hardening)"

PATCH_BLOCK_TEMPLATE = '''    {marker}
    try:
        from licensing.license_guard import enforce_or_exit
        enforce_or_exit("{component}")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

'''


def patch_main(filepath: Path, component: str, dry_run: bool) -> dict:
    """Insert license_guard call at start of main() body."""
    if not filepath.exists():
        return {"file": str(filepath.name), "status": "missing"}

    text = filepath.read_text(encoding="utf-8")

    if MARKER in text:
        return {"file": filepath.name, "status": "already_patched"}

    # Find the def main(): line
    m = re.search(r"^def main\(\):\s*\n", text, flags=re.MULTILINE)
    if not m:
        return {"file": filepath.name, "status": "no_main_function"}

    # Find first non-docstring, non-blank line inside main()
    # Simplified approach: insert right after `def main():` line + any docstring
    insertion_point = m.end()
    rest = text[insertion_point:]

    # Skip optional docstring
    doc_match = re.match(r'\s*("""(?:.|\n)*?""")\s*\n', rest)
    if doc_match:
        insertion_point += doc_match.end()

    patch = PATCH_BLOCK_TEMPLATE.format(marker=MARKER, component=component)
    new_text = text[:insertion_point] + patch + text[insertion_point:]

    if dry_run:
        return {
            "file": filepath.name,
            "status": "would_patch",
            "insertion_at_char": insertion_point,
            "preview": patch.strip()[:120],
        }

    filepath.write_text(new_text, encoding="utf-8")
    return {"file": filepath.name, "status": "patched"}


def main():
    p = argparse.ArgumentParser(description="Apply license guard to CLIs")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    if not (args.dry_run or args.apply):
        p.print_help()
        return 1

    print(f"Mode: {'DRY RUN' if args.dry_run else 'APPLY'}")
    print(f"Targets: {len(TARGETS)}")
    print()

    stats = {"patched": 0, "already_patched": 0, "missing": 0, "no_main_function": 0,
             "would_patch": 0}

    for filename, component in TARGETS:
        if filename in EXEMPT:
            print(f"  [SKIP-EXEMPT] {filename}")
            continue
        filepath = ORCH_DIR / filename
        result = patch_main(filepath, component, dry_run=args.dry_run)
        status = result["status"]
        stats[status] = stats.get(status, 0) + 1
        symbol = {
            "patched": "[+]", "would_patch": "[~]",
            "already_patched": "[=]", "missing": "[!]",
            "no_main_function": "[?]",
        }.get(status, "[ ]")
        print(f"  {symbol} {filename:<28s} {status}")

    print()
    print("Summary:")
    for k, v in stats.items():
        if v:
            print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

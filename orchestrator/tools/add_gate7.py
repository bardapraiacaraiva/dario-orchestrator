#!/usr/bin/env python3
"""Batch-append Gate 7 (Status Checklist per data point) to SKILL.md files.

Pattern proven in FASE 1 (MEMORY.md: fase1_pipeline_validated_2026_05_23.md):
adding explicit 🔵/🟡/🟢 status labels to each data point lifted
delivery_ready_rate from 17.5% to 50% in 1 session.

This tool propagates the same pattern to all SKILL.md files that don't have it.

Usage:
    python -m tools.add_gate7 --dry-run     # show what would change
    python -m tools.add_gate7 --apply       # write changes
    python -m tools.add_gate7 --apply --limit 10  # cap for safety

Idempotent: looks for marker tags before writing.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"

# Markers we look for to detect Gate 7 already present
GATE7_MARKERS = [
    "Status checklist per data point",
    "Gate 7",
    "🔵 verified",
    "🔵 **verified**",
]

# Begin/end markers for our appended block (allows safe re-runs/removal)
APPEND_BEGIN = "<!-- gate7:begin -->"
APPEND_END = "<!-- gate7:end -->"


GATE7_TEMPLATE = """

{begin_marker}
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **{skill_name}** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in {skill_name}:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
{end_marker}
"""


def has_gate7(content: str) -> bool:
    """Return True if any Gate 7 marker is already present."""
    return any(m in content for m in GATE7_MARKERS) or APPEND_BEGIN in content


def get_skill_name(path: Path, content: str) -> str:
    """Extract skill name from frontmatter `name:` field; fall back to dir name."""
    m = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return path.parent.name


def build_block(skill_name: str) -> str:
    return GATE7_TEMPLATE.format(
        skill_name=skill_name,
        begin_marker=APPEND_BEGIN,
        end_marker=APPEND_END,
    )


def collect_targets() -> list[Path]:
    return sorted(SKILLS_DIR.rglob("SKILL.md"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="don't write, just report")
    ap.add_argument("--apply", action="store_true", help="actually write changes")
    ap.add_argument("--limit", type=int, default=0, help="cap number of files modified (0 = no cap)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not args.dry_run and not args.apply:
        print("Specify --dry-run or --apply", file=sys.stderr)
        return 2

    if not SKILLS_DIR.exists():
        print(f"Skills dir not found: {SKILLS_DIR}", file=sys.stderr)
        return 1

    all_files = collect_targets()
    skipped_with_gate7 = 0
    to_modify: list[tuple[Path, str]] = []

    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as e:
            if args.verbose:
                print(f"  [skip read-error] {f}: {e}")
            continue
        if has_gate7(content):
            skipped_with_gate7 += 1
            continue
        skill_name = get_skill_name(f, content)
        block = build_block(skill_name)
        to_modify.append((f, content + block))

    if args.limit and len(to_modify) > args.limit:
        to_modify = to_modify[: args.limit]

    print(f"SKILL.md files scanned: {len(all_files)}")
    print(f"  already had Gate 7: {skipped_with_gate7}")
    print(f"  to modify: {len(to_modify)}")

    if args.dry_run:
        if args.verbose:
            for f, _ in to_modify[:10]:
                print(f"  WOULD MODIFY: {f}")
            if len(to_modify) > 10:
                print(f"  ... and {len(to_modify) - 10} more")
        return 0

    written = 0
    failed: list[tuple[Path, str]] = []
    for f, new_content in to_modify:
        try:
            f.write_text(new_content, encoding="utf-8")
            written += 1
        except Exception as e:
            failed.append((f, str(e)))

    print(f"\nApplied: {written}")
    if failed:
        print(f"Failed: {len(failed)}")
        for f, err in failed[:5]:
            print(f"  ! {f}: {err}")
    return 0 if not failed else 3


if __name__ == "__main__":
    sys.exit(main())

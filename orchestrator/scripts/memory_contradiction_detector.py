#!/usr/bin/env python3
"""Memory drift detector — flag numerical contradictions across memory files.

Closes audit Risk #9 (partial). Full embedding-based memory is a multi-week
refactor (see RFC stub at end of file); this is the cheap first step that
catches the most common drift symptom:

  - "delivery_rate 17.5%" in one file
  - "delivery_rate 50%" in another file
  - "delivery_rate 56%" in a third

Without a detector, these accumulate silently. With one, drift surfaces
as a CI/cron alert.

Approach:
  1. Walk all *.md files in memory dir
  2. Extract patterns: "<label>: <number><unit>" or "<label> = <number><unit>"
  3. Group by normalized label
  4. Flag groups where values diverge >25% OR are categorically different
     (e.g. "score 80" vs "score 87" = OK; "users 5K" vs "users 50K" = drift)
  5. Output JSONL of findings + summary table

Usage:
    python -m scripts.memory_contradiction_detector              # text report
    python -m scripts.memory_contradiction_detector --json       # JSONL
    python -m scripts.memory_contradiction_detector --threshold 0.30  # 30% divergence
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

MEMORY_DIR_CANDIDATES = [
    Path.home() / ".claude" / "projects" / "C--Users-barda" / "memory",
]
# Auto-discover any other ~/.claude/projects/*/memory/
projects_dir = Path.home() / ".claude" / "projects"
if projects_dir.exists():
    for child in projects_dir.iterdir():
        candidate = child / "memory"
        if candidate.is_dir() and candidate not in MEMORY_DIR_CANDIDATES:
            MEMORY_DIR_CANDIDATES.append(candidate)


# Patterns we look for:
#   "label: 80%" or "label: 80/100" or "label = 80%"
#   "X clients" or "X users" or "X tokens"
LABELED_NUMBER_RE = re.compile(
    r"\b"
    r"(?P<label>[A-Za-z][A-Za-z_\-\s]{2,40}?)"   # 3-40 char label
    r"\s*[:=]\s*"                                # colon or equals
    r"(?P<value>[\d.,]+)"                        # numeric value
    r"\s*"
    r"(?P<unit>%|/100|pts|pp|x|×|k|K|M|"        # common units
        r"tokens?|users?|clients?|skills?|tests?|files?|rows?|"
        r"seconds?|s\b|ms\b|min\b|hours?\b|days?\b|weeks?|months?|"
        r"€|EUR|R\$|BRL|USD|\$)?",
    re.IGNORECASE,
)

# Pattern for "X% out of Y" or "X/Y" ratios
RATIO_RE = re.compile(r"\b(\d+)/(\d+)\b")


# Labels we IGNORE (too vague or always context-dependent)
IGNORE_LABELS = {
    "version", "v", "step", "phase", "wave", "fase", "id", "number",
    "n", "n=", "limit", "max", "min", "default", "example", "sample",
    "test", "line", "col", "row", "year", "month", "day", "hour",
    "page", "chapter", "section", "tab", "port", "pid",
    # Generic narrative connectors — appear with random values across files
    "total", "antes", "depois", "before", "after", "old", "new",
    "from", "to", "de", "para", "actual", "atual", "current", "previous",
    "now", "agora", "score", "value", "result", "result", "found",
    # Metadata fields from frontmatter
    "originsessionid", "node_type", "type", "created", "updated", "ts",
    "started", "ended", "completed",
}

# Patterns that indicate a line should be skipped entirely
SKIP_LINE_RE = re.compile(
    r"(?:"
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"  # UUID
    r"|sha-?256|sha-?1|md5"                                            # hash mentions
    r"|^---\s*$"                                                       # frontmatter delim
    r"|originSessionId|HEAD\s+[a-f0-9]{7}"                            # session/commit refs
    r")",
    re.IGNORECASE,
)


def normalize_label(label: str) -> str:
    """Lowercase, strip whitespace, replace internal spaces with underscore."""
    return re.sub(r"\s+", "_", label.strip().lower())


def parse_value(raw: str, unit: str | None) -> float | None:
    """Parse '80%', '1,500', '2K' etc to a float. Returns None if unparseable."""
    s = raw.replace(",", "").strip()
    try:
        v = float(s)
    except ValueError:
        return None
    if unit:
        u = unit.lower()
        if u in ("k",):
            v *= 1_000
        elif u in ("m",):
            v *= 1_000_000
    return v


def scan_file(path: Path) -> list[dict]:
    """Extract labeled numerical claims from a markdown file."""
    findings: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return findings

    in_frontmatter = False
    for line_num, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()

        # Skip frontmatter block (between --- lines at top of file)
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue

        # Skip code blocks (heuristic) + skip lines with UUIDs/hashes/etc
        if stripped.startswith("```") or stripped.startswith("    "):
            continue
        if SKIP_LINE_RE.search(line):
            continue

        for m in LABELED_NUMBER_RE.finditer(line):
            label = normalize_label(m.group("label"))
            if label in IGNORE_LABELS or len(label) < 3:
                continue
            unit = (m.group("unit") or "").strip().lower()
            value = parse_value(m.group("value"), unit)
            if value is None:
                continue
            findings.append({
                "file": str(path.name),
                "line": line_num,
                "label": label,
                "value": value,
                "unit": unit,
                "raw_line": stripped[:120],
            })

    return findings


def detect_contradictions(all_findings: list[dict], threshold: float) -> list[dict]:
    """Group by label, flag groups with high divergence.

    threshold: max acceptable (max - min) / max. Above this = contradiction.
    """
    by_label_unit: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for f in all_findings:
        key = (f["label"], f["unit"])
        by_label_unit[key].append(f)

    contradictions: list[dict] = []
    for (label, unit), group in by_label_unit.items():
        if len(group) < 2:
            continue  # need at least 2 to contradict
        values = [g["value"] for g in group]
        v_min, v_max = min(values), max(values)
        if v_max == 0:
            continue
        divergence = (v_max - v_min) / v_max
        if divergence < threshold:
            continue

        # Also skip groups where values come from same file (likely fine —
        # different points in time within one narrative)
        unique_files = {g["file"] for g in group}
        if len(unique_files) < 2:
            continue

        contradictions.append({
            "label": label,
            "unit": unit,
            "divergence": round(divergence, 3),
            "min_value": v_min,
            "max_value": v_max,
            "occurrences": [
                {"file": g["file"], "line": g["line"], "value": g["value"],
                 "raw": g["raw_line"]}
                for g in sorted(group, key=lambda x: x["value"])
            ],
        })

    return sorted(contradictions, key=lambda c: c["divergence"], reverse=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.25,
                    help="Min divergence to flag (default 0.25 = 25%%)")
    ap.add_argument("--json", action="store_true",
                    help="JSONL output to stdout")
    ap.add_argument("--memory-dir", default=None,
                    help="Override memory dir (default: auto-discover)")
    args = ap.parse_args()

    if args.memory_dir:
        dirs = [Path(args.memory_dir)]
    else:
        dirs = [d for d in MEMORY_DIR_CANDIDATES if d.exists()]

    if not dirs:
        print("No memory dir found", file=sys.stderr)
        return 1

    all_findings: list[dict] = []
    files_scanned = 0
    for d in dirs:
        for f in d.glob("*.md"):
            if f.name == "MEMORY.md":
                continue  # MEMORY is index, skip
            findings = scan_file(f)
            all_findings.extend(findings)
            files_scanned += 1

    contradictions = detect_contradictions(all_findings, args.threshold)

    if args.json:
        for c in contradictions:
            print(json.dumps(c, ensure_ascii=False))
        return 0 if not contradictions else 2

    print(f"=== Memory Contradiction Scan ===")
    print(f"  Memory dirs: {[str(d) for d in dirs]}")
    print(f"  Files scanned: {files_scanned}")
    print(f"  Total labeled numbers: {len(all_findings)}")
    print(f"  Contradictions found (≥{args.threshold*100:.0f}% divergence): {len(contradictions)}")
    print()

    if not contradictions:
        print("  ✓ No drift detected")
        return 0

    for i, c in enumerate(contradictions[:20], 1):
        print(f"  [{i}] {c['label']!r} ({c['unit']!r}) — {c['divergence']*100:.0f}% divergence "
              f"({c['min_value']} ↔ {c['max_value']})")
        for occ in c["occurrences"][:4]:
            print(f"        {occ['file']}:{occ['line']}  value={occ['value']}")
            print(f"        > {occ['raw'][:100]}")
        print()

    if len(contradictions) > 20:
        print(f"  ... and {len(contradictions) - 20} more (use --json for full list)")

    return 2  # non-zero so cron alerts


if __name__ == "__main__":
    sys.exit(main())

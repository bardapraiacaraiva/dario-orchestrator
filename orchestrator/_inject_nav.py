#!/usr/bin/env python
"""Inject DARIO dashboards nav into HTML files."""
import re
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
NAV_FILE = ORCH_DIR / "_nav_fragment.html"

TARGETS = [
    "mission-control.html",
    "agent-visualizer.html",
    "agent_display.html",
    "cognitive_dashboard.html",
    "cfo_dashboard.html",
]


def inject(file_path: Path, nav: str) -> bool:
    """Inject nav after <body> tag. Returns True if modified."""
    content = file_path.read_text(encoding="utf-8")
    if "dario-nav" in content:
        return False  # already integrated
    new = re.sub(
        r"(<body[^>]*>)",
        lambda m: m.group(1) + "\n" + nav,
        content,
        count=1,
        flags=re.IGNORECASE,
    )
    if new == content:
        # No <body>; inject before </head>
        new = re.sub(r"(</head>)", nav + r"\1", content, count=1, flags=re.IGNORECASE)
    if new == content:
        return False  # cannot inject
    file_path.write_text(new, encoding="utf-8")
    return True


def main() -> int:
    if not NAV_FILE.exists():
        print(f"[FAIL] nav fragment not found: {NAV_FILE}")
        return 1
    nav = NAV_FILE.read_text(encoding="utf-8")
    results = []
    for target in TARGETS:
        file_path = ORCH_DIR / target
        if not file_path.exists():
            results.append((target, "MISSING"))
            continue
        try:
            modified = inject(file_path, nav)
            results.append((target, "INJECTED" if modified else "ALREADY_HAS_NAV"))
        except Exception as e:
            results.append((target, f"ERROR: {e}"))
    for name, status in results:
        symbol = {"INJECTED": "[OK]", "ALREADY_HAS_NAV": "[==]", "MISSING": "[??]"}.get(
            status, "[!!]"
        )
        print(f"  {symbol} {name} -> {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

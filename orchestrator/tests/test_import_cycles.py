"""Tripwire: package-level import cycles must not GROW (Onda 4, 2026-06-12).

The audit found 9 bidirectional package pairs (hub core<->execution<->providers)
— tolerated via late imports, but each new cycle makes refactors drag more of
the system along. This freezes the baseline: removing a pair is progress
(update the baseline!), adding one fails the gate with the offending pair named.
"""

import re
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"

# Frozen 2026-06-12 (audit). Shrink freely; grow only with a deliberate
# decision recorded in the commit message.
BASELINE_PAIRS = {
    ("cognitive", "core"),
    ("cognitive", "quality"),
    ("core", "execution"),
    ("core", "licensing"),
    ("core", "observability"),
    ("core", "reliability"),
    ("core", "runners"),
    ("core", "streaming"),
    ("execution", "providers"),
}

_SKIP_DIRS = {".venv", "__pycache__", ".hypothesis", ".mypy_cache", "node_modules", "tests"}
_IMPORT_PAT = re.compile(r"^\s*(?:from|import)\s+([a-z_]+)[.\s]", re.M)


def _bidirectional_pairs() -> set:
    pkgs = {p.name for p in ORCH_DIR.iterdir()
            if p.is_dir() and p.name not in _SKIP_DIRS and any(p.glob("*.py"))}
    imports = {}
    for pkg in pkgs:
        deps = set()
        for f in (ORCH_DIR / pkg).rglob("*.py"):
            if "__pycache__" in str(f):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for m in _IMPORT_PAT.findall(text):
                if m in pkgs and m != pkg:
                    deps.add(m)
        imports[pkg] = deps
    return {tuple(sorted((a, b))) for a in imports for b in imports[a]
            if a in imports.get(b, set())}


def test_no_new_import_cycles():
    current = _bidirectional_pairs()
    new = current - BASELINE_PAIRS
    assert not new, (
        f"NEW bidirectional import pair(s): {sorted(new)} — break the cycle "
        f"(late import or interface module) or record a deliberate baseline "
        f"update in the commit message."
    )


def test_baseline_not_stale():
    """If a pair was eliminated, celebrate by shrinking the baseline."""
    current = _bidirectional_pairs()
    gone = BASELINE_PAIRS - current
    assert not gone, (
        f"Pair(s) no longer cyclic: {sorted(gone)} — remove them from "
        f"BASELINE_PAIRS so the gate keeps teeth."
    )

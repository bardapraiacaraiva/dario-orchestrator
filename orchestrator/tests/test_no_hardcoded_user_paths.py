"""Path discipline test — fails if any production code hardcodes a
user-specific slug (RFC_MULTI_TENANT.md §5 PW-4).

Catches:
  - `C--Users-barda` (Claude Code's per-user project slug)
  - `/Users/barda/` or `C:/Users/barda/` (raw OS paths)
  - `barda/.claude/` (mixed forms)

Skips:
  - Test files (test_*.py) — they may legitimately reference paths for fixtures
  - Documentation (.md) — these can mention paths for examples
  - This test file itself
  - Memory dump scripts that operate ON barda's specific memory

If you have a legit reason to reference a specific user (e.g., one-time
migration script for barda's data only), name the file with `_oneoff` suffix
to skip the check, OR add it explicitly to ALLOWED_EXCEPTIONS below.
"""

from __future__ import annotations

import re
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"

# Patterns that indicate a hardcoded user-specific path
FORBIDDEN_PATTERNS = [
    re.compile(r"C--Users-barda"),
    re.compile(r"/Users/barda/"),
    re.compile(r"C:[/\\]+Users[/\\]+barda[/\\]"),
    re.compile(r"barda[/\\]\.claude"),
]

# Files where the patterns are allowed (legacy compat fallback strings, doc examples)
ALLOWED_EXCEPTIONS = {
    # autodiag.py contains the pattern only inside _resolve_memory_dir() as
    # a documented legacy fallback string — never executed except when no
    # other user dir is found.
    ORCH_DIR / "runners" / "autodiag.py",
    # The RFC document itself REFERENCES these patterns as bad examples.
    ORCH_DIR / "RFC_MULTI_TENANT.md",
    # CONVENTIONS.md shows the patterns as ❌ examples in the path discipline rule.
    ORCH_DIR / "CONVENTIONS.md",
}


def _is_skipped(path: Path) -> bool:
    """Skip tests, dotfiles, virtualenvs, caches, one-off scripts."""
    parts = path.parts
    if any(p.startswith(".") for p in parts):
        return True
    if "tests" in parts:
        return True
    if path.suffix == ".md":
        return True
    if path.stem.endswith("_oneoff"):
        return True
    if path in ALLOWED_EXCEPTIONS:
        return True
    return False


def test_no_hardcoded_user_paths_in_production_code():
    """Scan orchestrator/ Python + YAML for forbidden user-slug patterns."""
    violations: list[tuple[Path, int, str]] = []
    for root, dirs, files in __import__("os").walk(ORCH_DIR):
        # Prune hidden / cache dirs
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        root_path = Path(root)
        for name in files:
            if not (name.endswith(".py") or name.endswith(".yaml") or name.endswith(".yml")):
                continue
            path = root_path / name
            if _is_skipped(path):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for line_num, line in enumerate(text.splitlines(), 1):
                for pat in FORBIDDEN_PATTERNS:
                    if pat.search(line):
                        violations.append((path, line_num, line.strip()[:120]))
                        break

    assert not violations, (
        f"Found {len(violations)} hardcoded user-slug references "
        "(see RFC_MULTI_TENANT.md §5 PW-4 + CONVENTIONS.md Path discipline). "
        "Use Path.home() or env var override. "
        "If intentional, add to ALLOWED_EXCEPTIONS in this test.\n"
        + "\n".join(
            f"  {p.relative_to(ORCH_DIR)}:{ln}: {snippet}"
            for p, ln, snippet in violations[:20]
        )
    )


def test_exception_list_files_actually_exist():
    """Drift guard: if a file in ALLOWED_EXCEPTIONS is renamed/deleted,
    fail loudly so the exception can be cleaned up."""
    missing = [p for p in ALLOWED_EXCEPTIONS if not p.exists()]
    assert not missing, (
        f"Files in ALLOWED_EXCEPTIONS no longer exist (clean them up): "
        f"{[str(p.relative_to(ORCH_DIR)) for p in missing]}"
    )

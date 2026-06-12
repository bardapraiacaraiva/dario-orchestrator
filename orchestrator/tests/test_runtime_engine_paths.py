"""Every script the runtime invokes must exist (DD finding C2, 2026-06-12).

The 2026-05-25 package refactor moved scripts into subpackages but left
core/runtime.py invoking root-level names — _run_engine returned
{"error": "... not found"} wrapped in HTTP 200, so suspend/resume and six
endpoints silently did nothing for 18 days. This test statically extracts
every _run_engine("...") / ORCH_DIR / "...py" literal from runtime.py and
fails if the target file is missing, so a future move breaks loudly.
"""

import re
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

RUNTIME = ORCH_DIR / "core" / "runtime.py"


def _invoked_scripts() -> set[str]:
    text = RUNTIME.read_text(encoding="utf-8")
    scripts = set(re.findall(r'_run_engine\(\s*"([^"]+\.py)"', text))
    # subprocess calls built as ORCH_DIR / "pkg" / "script.py" or ORCH_DIR / "script.py"
    for parts in re.findall(r'ORCH_DIR\s*((?:/\s*"[^"]+"\s*)+)', text):
        segs = re.findall(r'"([^"]+)"', parts)
        if segs and segs[-1].endswith(".py"):
            scripts.add("/".join(segs))
    return scripts


def test_runtime_extracts_a_plausible_script_set():
    scripts = _invoked_scripts()
    # The pulse alone invokes 6+ engines; an empty/small set means the
    # extraction regex rotted, which would make the next test vacuous.
    assert len(scripts) >= 10, f"extraction looks broken: {sorted(scripts)}"


def test_every_runtime_invoked_script_exists():
    missing = sorted(s for s in _invoked_scripts() if not (ORCH_DIR / s).exists())
    assert not missing, (
        f"core/runtime.py invokes scripts that do not exist: {missing} — "
        "fix the path or add the file; _run_engine swallows the error at runtime."
    )


def test_suspend_resume_lives_in_execution():
    """The module serializes EXECUTION state; it was misfiled under finance/
    by the 2026-05-25 refactor, which is how the ghost paths went unnoticed."""
    assert (ORCH_DIR / "execution" / "suspend_resume.py").exists()
    assert not (ORCH_DIR / "finance" / "suspend_resume.py").exists()

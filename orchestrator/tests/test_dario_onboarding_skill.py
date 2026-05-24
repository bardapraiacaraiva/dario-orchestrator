"""Test that /dario-onboarding skill exists with required structure.

Onboarding is the first thing a new user (or future-Claude on a clean
machine) sees. If this skill drifts, the new-user experience breaks.
"""

from __future__ import annotations

from pathlib import Path

import pytest

SKILL_DIR = Path.home() / ".claude" / "skills" / "dario-onboarding"
SKILL_MD = SKILL_DIR / "SKILL.md"


@pytest.fixture(scope="module")
def skill_text() -> str:
    assert SKILL_MD.exists(), f"Onboarding skill missing at {SKILL_MD}"
    return SKILL_MD.read_text(encoding="utf-8")


class TestSkillStructure:

    def test_frontmatter_name_matches(self, skill_text):
        # First non-empty line should be ---, then name: dario-onboarding
        assert skill_text.startswith("---"), "SKILL.md must start with YAML frontmatter"
        # Find name field
        in_fm = False
        for line in skill_text.splitlines():
            if line.strip() == "---":
                if in_fm:
                    break
                in_fm = True
                continue
            if in_fm and line.startswith("name:"):
                value = line.split(":", 1)[1].strip().strip('"').strip("'")
                assert value == "dario-onboarding"
                return
        pytest.fail("No name: field found in frontmatter")

    def test_has_argument_hint(self, skill_text):
        assert "argument-hint:" in skill_text

    def test_declares_required_tools(self, skill_text):
        # Bash + Read at minimum (skill runs diagnostic commands + reads docs)
        assert "allowed-tools:" in skill_text
        # Find the line and check
        for line in skill_text.splitlines():
            if line.startswith("allowed-tools:"):
                assert "Read" in line, "Read tool required for doc inspection"
                assert "Bash" in line, "Bash tool required for diagnostic commands"
                return
        pytest.fail("allowed-tools line not found")


class TestRequiredSections:

    @pytest.mark.parametrize("section", [
        "Step 1 — HEALTH CHECK",
        "Step 2 — MENTAL MODEL",
        "Step 3 — FIRST DISPATCH",
        "Step 4 — WHERE THINGS LIVE",
        "Step 5 — DAILY HEARTBEAT",
        "Step 6 — KEY RESOURCES",
    ])
    def test_section_present(self, skill_text, section):
        assert section in skill_text, f"Missing section: {section}"

    def test_has_argument_mode_table(self, skill_text):
        # User can invoke with short/health/first-task — make sure documented
        for mode in ("short", "health", "first-task"):
            assert mode in skill_text, f"Argument mode '{mode}' not documented"

    def test_has_gate_7_status_checklist(self, skill_text):
        assert "<!-- gate7:begin -->" in skill_text
        assert "<!-- gate7:end -->" in skill_text


class TestExecutableDiagnostics:
    """Step 1 must contain real bash commands the skill executes.

    If these break (e.g., RAG port changed, license path moved), the
    onboarding skill will report stale info to a new user — bad first impression.
    """

    @pytest.mark.parametrize("expected_command_fragment", [
        "localhost:8420/health",                          # RAG check
        "~/.claude/orchestrator/.license",                 # License check
        "ls ~/.claude/skills/ | grep polished",            # Wrappers check
        "~/.claude/orchestrator/budgets/",                 # Budget check
        "~/.claude/orchestrator/scripts/hooks/pre-push",   # Test suite check
    ])
    def test_diagnostic_command_present(self, skill_text, expected_command_fragment):
        assert expected_command_fragment in skill_text, (
            f"Diagnostic command fragment missing: {expected_command_fragment}. "
            "If you intentionally removed it, update this test."
        )


class TestDocReferences:
    """References to canonical docs must point to files that actually exist."""

    @pytest.mark.parametrize("doc_path", [
        "~/.claude/orchestrator/PADRAO_A_AB_TEST_RESULTS.md",
        "~/.claude/orchestrator/MANUAL.md",
        "~/.claude/projects/C--Users-barda/memory/MEMORY.md",
    ])
    def test_doc_referenced_exists(self, skill_text, doc_path):
        # Skill mentions it
        assert doc_path in skill_text, f"Doc reference missing from skill: {doc_path}"
        # And the file actually exists
        actual = Path(doc_path.replace("~", str(Path.home())))
        assert actual.exists(), (
            f"Skill references {doc_path} but file not found at {actual}. "
            "Either restore the doc or update the skill."
        )


class TestSlashCommandsListed:
    """The 'daily heartbeat' table should mention the workhorse commands."""

    @pytest.mark.parametrize("cmd", [
        "/dario-status",
        "/dario-orchestrator",
        "/dario-dashboard",
        "/dream",
    ])
    def test_command_documented(self, skill_text, cmd):
        assert cmd in skill_text, f"Slash command '{cmd}' missing from daily heartbeat"

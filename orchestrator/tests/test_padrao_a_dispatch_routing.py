"""Integration tests for Padrão A dispatch routing.

Verifies that the orchestrator's company.yaml correctly wires up
the 8 tier-A workers to their polished wrapper variants, and that
all referenced wrapper skills physically exist on disk.

These tests guard against:
  - Missing `skill_client_facing` field on tier-A workers
  - Pointing to a wrapper skill that doesn't exist
  - Tier 2 workers (brand, sales-letter) missing the validation flag
  - Drift between SKILL.md docs and company.yaml routing data

Added 2026-05-24 alongside the Padrão A propagation
(orchestrator/PADRAO_A_AB_TEST_RESULTS.md).
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SKILLS_DIR = Path.home() / ".claude" / "skills"
COMPANY_YAML = ORCH_DIR / "company.yaml"


def load() -> dict:
    """Direct yaml.safe_load of company.yaml.

    Bypasses config.company_loader (which transitively imports
    semantic_dispatch — a VIP-only stub that raises on import).
    For this test we only need the static workers dict, so the
    legacy monolith file is sufficient.
    """
    with open(COMPANY_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ─────────────────────────────────────────────────────────────────────
# Expected Padrão A routing (must match company.yaml + SKILL.md)
# ─────────────────────────────────────────────────────────────────────

TIER_1_WORKERS = {
    # worker_id → expected polished skill name
    "worker-pitch":           "dario-pitch-polished",
    "worker-offer":           "dario-offer-polished",
    "worker-funnel":          "dario-funnel-polished",
    "worker-product":         "dario-product-polished",
    "worker-wp-audit":        "dario-wp-audit-polished",
    "worker-financial-model": "dario-financial-model-polished",
}

TIER_2_WORKERS = {
    # Same shape as Tier 1, but ALSO require briefing validation flag
    "worker-brand":         "dario-brand-polished",
    "worker-sales-letter":  "dario-sales-letter-polished",
}

ALL_PADRAO_A_WORKERS = {**TIER_1_WORKERS, **TIER_2_WORKERS}


# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────

def _load_workers() -> dict:
    cfg = load()
    return cfg.get("workers") or {}


def _skill_exists(skill_name: str) -> bool:
    return (SKILLS_DIR / skill_name / "SKILL.md").is_file()


# ─────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────

class TestPadraoARoutingConfig:
    """Validate company.yaml wiring for Padrão A wrappers."""

    def test_all_padrao_a_workers_exist_in_company_yaml(self):
        workers = _load_workers()
        missing = [w for w in ALL_PADRAO_A_WORKERS if w not in workers]
        assert not missing, f"Workers missing from company.yaml: {missing}"

    def test_tier_1_workers_have_skill_client_facing(self):
        workers = _load_workers()
        for worker_id, expected_polished in TIER_1_WORKERS.items():
            w = workers[worker_id]
            actual = w.get("skill_client_facing")
            assert actual == expected_polished, (
                f"{worker_id}: expected skill_client_facing={expected_polished!r}, "
                f"got {actual!r}"
            )

    def test_tier_1_workers_NOT_marked_requires_validation(self):
        """Tier 1 = auto-route, no pre-flight briefing check."""
        workers = _load_workers()
        for worker_id in TIER_1_WORKERS:
            w = workers[worker_id]
            assert not w.get("requires_briefing_validation"), (
                f"{worker_id} should NOT require briefing validation (Tier 1)"
            )

    def test_tier_2_workers_have_skill_client_facing(self):
        workers = _load_workers()
        for worker_id, expected_polished in TIER_2_WORKERS.items():
            w = workers[worker_id]
            actual = w.get("skill_client_facing")
            assert actual == expected_polished, (
                f"{worker_id}: expected skill_client_facing={expected_polished!r}, "
                f"got {actual!r}"
            )

    def test_tier_2_workers_require_briefing_validation(self):
        """Tier 2 = brand + sales-letter — must validate briefing before dispatch."""
        workers = _load_workers()
        for worker_id in TIER_2_WORKERS:
            w = workers[worker_id]
            assert w.get("requires_briefing_validation") is True, (
                f"{worker_id} must have requires_briefing_validation: true (Tier 2)"
            )

    def test_base_skill_preserved_when_polished_added(self):
        """Adding skill_client_facing must NOT remove the base skill field."""
        workers = _load_workers()
        for worker_id in ALL_PADRAO_A_WORKERS:
            w = workers[worker_id]
            base_skill = w.get("skill")
            assert base_skill, (
                f"{worker_id} lost its base `skill` field — backward compat broken"
            )
            # Base skill must NOT be the polished variant — they must be distinct
            assert base_skill != w.get("skill_client_facing"), (
                f"{worker_id}: base skill should differ from polished variant"
            )

    def test_other_workers_unaffected(self):
        """Workers outside Padrão A should not have skill_client_facing."""
        workers = _load_workers()
        affected = {
            w_id: w.get("skill_client_facing")
            for w_id, w in workers.items()
            if w.get("skill_client_facing") and w_id not in ALL_PADRAO_A_WORKERS
        }
        assert not affected, (
            f"Unexpected workers have skill_client_facing set: {affected}. "
            "Either add them to TIER_1_WORKERS/TIER_2_WORKERS in this test, "
            "or remove the field from company.yaml."
        )


class TestPolishedSkillsExist:
    """Every polished skill referenced by routing must exist on disk."""

    def test_all_polished_skills_have_skill_md(self):
        missing = [
            polished
            for polished in ALL_PADRAO_A_WORKERS.values()
            if not _skill_exists(polished)
        ]
        assert not missing, (
            f"Polished skills referenced in company.yaml but no SKILL.md found: "
            f"{missing}. Expected at {SKILLS_DIR}/<skill>/SKILL.md"
        )

    def test_base_skills_still_exist(self):
        """Originals must remain untouched (zero functionality loss principle)."""
        workers = _load_workers()
        missing = []
        for worker_id in ALL_PADRAO_A_WORKERS:
            base = workers[worker_id]["skill"]
            if not _skill_exists(base):
                missing.append(base)
        assert not missing, (
            f"Base skills missing — backward compat broken: {missing}"
        )

    def test_polished_skill_frontmatter_name_matches(self):
        """Polished SKILL.md `name:` field must equal the directory/skill name."""
        mismatches = []
        for polished in ALL_PADRAO_A_WORKERS.values():
            skill_md = SKILLS_DIR / polished / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8")
            # Find frontmatter `name:` line
            in_fm = False
            name_value = None
            for line in text.splitlines():
                if line.strip() == "---":
                    if in_fm:
                        break
                    in_fm = True
                    continue
                if in_fm and line.startswith("name:"):
                    name_value = line.split(":", 1)[1].strip().strip('"').strip("'")
                    break
            if name_value != polished:
                mismatches.append((polished, name_value))
        assert not mismatches, (
            f"Skill name field mismatch (expected, actual): {mismatches}"
        )

    def test_polished_wrappers_load_base_skill(self):
        """Each polished wrapper must instruct Claude to Read the base SKILL.md
        in Step 1. Without this, the wrapper improvises and produces v1 below
        the validated A/B baseline (this was gap #5 in the architecture audit,
        fixed 2026-05-24).
        """
        missing_directive = []
        missing_base_reference = []
        for polished in ALL_PADRAO_A_WORKERS.values():
            base = polished.replace("-polished", "")
            text = (SKILLS_DIR / polished / "SKILL.md").read_text(encoding="utf-8")

            if "MANDATORY first action — load the base skill" not in text:
                missing_directive.append(polished)
                continue

            # The directive must point to the correct base skill path
            expected_ref = f"~/.claude/skills/{base}/SKILL.md"
            if expected_ref not in text:
                missing_base_reference.append((polished, expected_ref))

        assert not missing_directive, (
            f"Polished wrappers missing base-load directive: {missing_directive}. "
            "Each Step 1 must instruct Read of ~/.claude/skills/<base>/SKILL.md."
        )
        assert not missing_base_reference, (
            f"Polished wrappers pointing to wrong base path: {missing_base_reference}"
        )


class TestRoutingLogicEquivalence:
    """Simulate the dispatch routing rule and verify it picks the right skill."""

    def _resolve_dispatch_skill(self, worker: dict, execution_policy: str) -> str:
        """Mirror the routing rule documented in dario-orchestrator SKILL.md."""
        client_facing_policies = {"client_facing", "critical", "financial"}
        if execution_policy in client_facing_policies:
            polished = worker.get("skill_client_facing")
            if polished:
                # NOTE: this test does not exercise the briefing-validation
                # branch — that requires natural-language input from the user.
                return polished
        return worker["skill"]

    def test_client_facing_routes_to_polished_for_tier_1(self):
        workers = _load_workers()
        for worker_id, expected_polished in TIER_1_WORKERS.items():
            w = workers[worker_id]
            actual = self._resolve_dispatch_skill(w, "client_facing")
            assert actual == expected_polished, (
                f"{worker_id} client_facing → {actual!r}, expected {expected_polished!r}"
            )

    def test_default_policy_routes_to_base_skill(self):
        workers = _load_workers()
        for worker_id in ALL_PADRAO_A_WORKERS:
            w = workers[worker_id]
            actual = self._resolve_dispatch_skill(w, "default")
            assert actual == w["skill"], (
                f"{worker_id} default policy must route to base skill {w['skill']!r}, "
                f"got {actual!r}"
            )

    def test_critical_policy_routes_to_polished(self):
        workers = _load_workers()
        for worker_id, expected_polished in TIER_1_WORKERS.items():
            w = workers[worker_id]
            actual = self._resolve_dispatch_skill(w, "critical")
            assert actual == expected_polished, (
                f"{worker_id} critical policy must use polished {expected_polished!r}, "
                f"got {actual!r}"
            )

    def test_financial_policy_routes_to_polished(self):
        workers = _load_workers()
        # Financial-model is the most relevant for this policy
        w = workers["worker-financial-model"]
        actual = self._resolve_dispatch_skill(w, "financial")
        assert actual == "dario-financial-model-polished"

    def test_worker_without_polished_fallback_to_base(self):
        """Workers outside Padrão A must keep using their base skill on client_facing."""
        workers = _load_workers()
        # Pick a non-Padrão-A worker (e.g., worker-ads)
        non_padrao = [
            (w_id, w) for w_id, w in workers.items()
            if w_id not in ALL_PADRAO_A_WORKERS
               and w.get("type") == "worker"
               and w.get("skill")
        ]
        assert non_padrao, "Expected at least one non-Padrão-A worker to test fallback"
        w_id, w = non_padrao[0]
        actual = self._resolve_dispatch_skill(w, "client_facing")
        assert actual == w["skill"], (
            f"Non-Padrão-A worker {w_id} must fall back to base skill {w['skill']!r} "
            f"on client_facing, got {actual!r}"
        )

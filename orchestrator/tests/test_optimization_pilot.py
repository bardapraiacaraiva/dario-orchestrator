"""Tests for Onda 4 #5 — DSPy optimization pilot.

These tests validate the optimization package structure WITHOUT calling an
LM. The actual compile step is skipped because:
    - It costs real tokens (BootstrapFewShot ~ 50+ LM calls).
    - It requires goldens to be present, which the production env may not have.

Compile-time validation is performed via `--dry-run` of the CLI.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


class TestSignatures:
    def test_brand_signature_imports(self):
        from optimization.signatures import BrandPositioning
        # DSPy Signature subclasses expose input/output fields via .model_fields
        fields = BrandPositioning.model_fields
        assert "briefing" in fields
        assert "posicionamento" in fields
        assert "archetype" in fields
        assert "tom_de_voz" in fields
        assert "diferenciadores" in fields


class TestProgram:
    def test_brand_program_constructs(self):
        from optimization.programs import BrandPositioningProgram
        p = BrandPositioningProgram()
        # Has the predict module
        assert hasattr(p, "generate")


class TestEvalsParser:
    def test_parse_brand_output_extracts_fields(self):
        from optimization.evals import _parse_brand_output

        sample = """# Brand Positioning
## Posicionamento
Marca de cuidados premium focada em famílias com filhos pequenos.

archetype: Caregiver
## Tom de voz
Caloroso, claro, próximo

## Diferenciadores
- Atendimento 24/7
- Produtos hipoalergénicos
- Garantia de devolução em 30 dias
"""
        out = _parse_brand_output(sample)
        assert "premium" in out["posicionamento"].lower()
        assert out["archetype"] == "Caregiver"
        assert "caloroso" in out["tom_de_voz"].lower()
        assert len(out["diferenciadores"]) == 3

    def test_parse_handles_missing_sections(self):
        from optimization.evals import _parse_brand_output
        out = _parse_brand_output("Just some plain text with no headers.")
        assert out["posicionamento"] == ""
        assert out["archetype"] == ""
        assert out["diferenciadores"] == []


class TestBrandScore:
    def test_score_perfect_match_high(self):
        import dspy

        from optimization.evals import brand_score

        example = dspy.Example(
            briefing="Premium brand",
            posicionamento="Premium brand for families",
            archetype="Caregiver",
            tom_de_voz="warm",
            diferenciadores=["24/7"],
        ).with_inputs("briefing")

        # Mock prediction object (DSPy Prediction is dict-like via attribute access)
        class Pred:
            posicionamento = "Premium brand for families with kids"
            archetype = "Caregiver"
            tom_de_voz = "warm"
            diferenciadores = ["24/7"]

        score = brand_score(example, Pred())
        assert score >= 0.7, f"expected high score, got {score}"

    def test_score_handles_none_pred(self):
        import dspy

        from optimization.evals import brand_score

        example = dspy.Example(briefing="x", posicionamento="y", archetype="z",
                                tom_de_voz="w", diferenciadores=[]).with_inputs("briefing")
        assert brand_score(example, None) == 0.0


@pytest.mark.slow
class TestCLI:
    def test_dry_run_reports_example_count(self):
        """The --dry-run path should NOT call any LM and just print example stats."""
        r = subprocess.run(
            [sys.executable, "-m", "optimization.optimize_skill", "dario-brand", "--dry-run"],
            capture_output=True, text=True, timeout=30,
            cwd=str(ORCH_DIR),
        )
        assert r.returncode == 0, f"CLI failed: {r.stderr[:500]}"
        data = json.loads(r.stdout.strip())
        assert "examples_found" in data
        assert isinstance(data["examples_found"], int)

    def test_unsupported_skill_rejected(self):
        r = subprocess.run(
            [sys.executable, "-m", "optimization.optimize_skill", "dario-offer", "--dry-run"],
            capture_output=True, text=True, timeout=30,
            cwd=str(ORCH_DIR),
        )
        assert r.returncode != 0, "Should reject non-brand skill in pilot"

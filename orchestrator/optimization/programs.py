"""DSPy Modules wrapping the Signatures (Onda 4 #5 pilot).

A Module composes one or more LM calls implementing a Signature. The
simplest is `Predict(SignatureClass)` which performs a single completion.
More elaborate modules can chain `ChainOfThought`, `ReAct`, etc.
"""

from __future__ import annotations

import dspy

from optimization.signatures import BrandPositioning


class BrandPositioningProgram(dspy.Module):
    """Single-shot brand positioning generator.

    Uses ChainOfThought to make the model expose its reasoning before
    committing to the four output fields. Optimisers can then learn
    which reasoning patterns yield high-scoring outputs.
    """

    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(BrandPositioning)

    def forward(self, briefing: str):
        return self.generate(briefing=briefing)


__all__ = ["BrandPositioningProgram"]

"""DSPy Signatures for DARIO skills (Onda 4 #5 pilot).

A Signature in DSPy is a typed I/O spec — what goes in, what comes out,
and (optionally) instructions describing the transformation. Unlike a
hand-written prompt, the actual phrasing is left for the optimiser to
learn from examples.

This pilot covers a single skill (`dario-brand`) so the methodology can
be evaluated end-to-end before expanding to the other 559.
"""

from __future__ import annotations

import dspy


class BrandPositioning(dspy.Signature):
    """Generate a brand positioning statement plus archetype, tone of voice,
    and 3-5 differentiators for a client described by the input briefing.

    The output MUST follow the Kapferer Identity Prism dimensions where
    relevant (physique, personality, culture, relationship, reflection,
    self-image) and propose a Jungian archetype that anchors the brand."""

    briefing: str = dspy.InputField(
        desc="Free-text brief: company, market, customer, goal, constraints."
    )
    posicionamento: str = dspy.OutputField(
        desc="One-paragraph positioning statement (PT/EN, follow input language)."
    )
    archetype: str = dspy.OutputField(
        desc="Jungian archetype name (one of the 12 standard archetypes)."
    )
    tom_de_voz: str = dspy.OutputField(
        desc="Tone of voice descriptor (2-4 adjectives + 1-line guidance)."
    )
    diferenciadores: list[str] = dspy.OutputField(
        desc="3 to 5 concrete differentiators (each a short phrase)."
    )


__all__ = ["BrandPositioning"]

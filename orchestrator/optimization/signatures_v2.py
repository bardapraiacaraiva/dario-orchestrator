"""DSPy Signatures for sprint 3 compile — offer, funnel, pitch.

Each signature mirrors the BrandPositioning pattern: typed I/O with
docstring instructions. The optimizer will learn phrasing via demos.
"""

from __future__ import annotations

import dspy


class OfferGeneration(dspy.Signature):
    """Generate a Grand Slam Offer (Hormozi value equation) for the
    business described in the briefing.

    The output MUST follow the value equation structure:
      Value = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort & Sacrifice)

    Include risk reversal, bonus stack (3 tangible bonuses with anchor
    values), and genuine urgency (real deadline or scarcity, not fake)."""

    briefing: str = dspy.InputField(
        desc="Free-text brief: business, target customer, pricing, differential."
    )
    core_offer: str = dspy.OutputField(
        desc="One-paragraph offer headline + 3 bullet points of what's included."
    )
    value_equation: str = dspy.OutputField(
        desc="Breakdown of dream_outcome, perceived_likelihood, time, effort."
    )
    risk_reversal: str = dspy.OutputField(
        desc="Specific guarantee or risk-shift mechanism."
    )
    bonuses: list[str] = dspy.OutputField(
        desc="3 tangible bonuses, each with anchor value (e.g. 'X — valor R$ Y')."
    )
    urgency: str = dspy.OutputField(
        desc="Genuine urgency driver (real deadline, capacity limit, etc.)."
    )


class FunnelDesign(dspy.Signature):
    """Design a multi-stage marketing funnel for the business described.

    Must specify the stages (typically 4-6), conversion thresholds, key
    copy hooks, CTAs per stage, and automation triggers."""

    briefing: str = dspy.InputField(
        desc="Business, product, target, pricing, current traffic source."
    )
    stages: list[str] = dspy.OutputField(
        desc="Funnel stages in order, each with name + purpose."
    )
    conversion_thresholds: str = dspy.OutputField(
        desc="Per-stage conversion benchmark (% expected). One per stage."
    )
    copy_hooks: list[str] = dspy.OutputField(
        desc="Headline / hook per stage (3-5 of them)."
    )
    automations: str = dspy.OutputField(
        desc="Triggers + actions (eg 'cart_abandon → 3-email sequence')."
    )


class PitchDeck(dspy.Signature):
    """Generate a 12-slide pitch deck outline for the venture described.

    Must include narrative arc (problem → solution → traction → ask),
    key slides with 1-line summary each, TAM/SAM/SOM with concrete
    numbers, and financial ask with use-of-funds."""

    briefing: str = dspy.InputField(
        desc="Venture, stage, market, traction, founder context."
    )
    narrative_arc: str = dspy.OutputField(
        desc="3-4 sentence story arc tying all slides together."
    )
    key_slides: list[str] = dspy.OutputField(
        desc="12 slides numbered, each 'N. Slide title — 1-line summary'."
    )
    tam_sam_som: str = dspy.OutputField(
        desc="TAM, SAM, SOM with concrete numbers + reasoning."
    )
    financial_ask: str = dspy.OutputField(
        desc="Amount + use-of-funds breakdown + milestones unlocked."
    )


__all__ = ["OfferGeneration", "FunnelDesign", "PitchDeck"]

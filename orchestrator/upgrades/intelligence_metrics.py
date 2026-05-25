"""Metrics Registry (extracted from `upgrades/intelligence.py` — Onda 6 #1).

Maps DARIO's 5-dimension rubric to research-backed deepeval metrics, plus
the garak red-team probe groups. Stateless registry — both attributes are
class-level dicts.

Parent `upgrades/intelligence.py` re-imports for backward-compat.
"""

from __future__ import annotations


class MetricsRegistry:
    """Registry of available evaluation metrics.

    Maps DARIO's 5-dimension rubric to research-backed metrics from deepeval,
    plus the garak red-team probe groups for adversarial testing tiers.
    """

    METRICS: dict[str, dict] = {
        # DARIO dimension → deepeval metric mapping
        "specificity": {
            "deepeval": "GEval(criteria='specificity')",
            "description": "Does output mention specific context, data, names?",
            "threshold": 0.6,
        },
        "actionability": {
            "deepeval": "GEval(criteria='actionability')",
            "description": "Are next steps clear and executable?",
            "threshold": 0.6,
        },
        "completeness": {
            "deepeval": "TaskCompletionMetric()",
            "description": "All requirements from input addressed?",
            "threshold": 0.7,
        },
        "accuracy": {
            "deepeval": "FaithfulnessMetric()",
            "description": "Facts and data correct? Sourced?",
            "threshold": 0.7,
        },
        "tone": {
            "deepeval": "GEval(criteria='tone_appropriateness')",
            "description": "Tone matches deliverable type?",
            "threshold": 0.5,
        },
        # Additional research metrics
        "hallucination": {
            "deepeval": "HallucinationMetric()",
            "description": "Output contains fabricated information?",
            "threshold": 0.8,
        },
        "answer_relevancy": {
            "deepeval": "AnswerRelevancyMetric()",
            "description": "Output is relevant to the input query?",
            "threshold": 0.7,
        },
    }

    RED_TEAM_PROBES: dict[str, list[str]] = {
        "quick": ["promptinject", "knownbadsignatures", "encoding"],
        "full": ["promptinject", "dan", "encoding", "leakedprompt", "xss", "snowball"],
        "financial": ["promptinject", "encoding", "leakedprompt"],
    }


__all__ = ["MetricsRegistry"]

"""The ONE execution pipeline shared by both engines (DD finding A7, 2026-06-12).

executor.py and providers/anthropic.py each declared their own filter list
with hand-copied parameters — equivalent today, but two definitions is how
they drift apart (the C1 quality-gate bug only existed on one of them).
Both engines now build from here; change filter composition in ONE place.

Lives in execution/ (not streaming/) on purpose: this package already imports
dispatch/, reliability/ and streaming/ in one direction, so the factory adds
no new pair to the frozen import-cycle baseline.
"""

from core.artifact_schemas import SchemaValidationFilter
from dispatch.model_router import ModelRouterFilter
from reliability.output_guardrails import OutputGuardrailFilter
from streaming.filter_pipeline import (
    BudgetFilter,
    FilterPipeline,
    LoggingFilter,
    QualityGateFilter,
    TokenBudgetFilter,
)


def build_execution_pipeline() -> FilterPipeline:
    return FilterPipeline([
        LoggingFilter(),                            # 10: log start/end
        ModelRouterFilter(),                        # 15: select optimal model
        BudgetFilter(warn_pct=80, block_pct=95),    # 20: check budget before execution
        SchemaValidationFilter(),                   # 65: validate output structure
        OutputGuardrailFilter(),                    # 70: secrets/PII/injection tripwire
        QualityGateFilter(min_score=60),            # 80: quality threshold gate
        TokenBudgetFilter(),                        # 90: log spend (complete_task is the sole budget writer)
    ])

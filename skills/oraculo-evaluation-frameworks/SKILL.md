---
name: oraculo-evaluation-frameworks
description: Custom eval framework design, LLM-as-judge, statistical rigor. Triggers em "eval framework", "LLM-as-judge", "evaluation methodology", "Eleuther harness", "DeepEval", "Promptfoo".
license: MIT
parent_agent: oraculo-director
compliance: [research_integrity]
---

# ORACULO-EVALUATION-FRAMEWORKS

## Eval taxonomy
- **Reference-based:** compare to gold answer (BLEU, ROUGE, exact match)
- **Reference-free:** judge intrinsic quality (perplexity, fluency)
- **LLM-as-judge:** AI evaluates AI (with bias mitigation)
- **Human eval:** gold standard, $$$, slow
- **Hybrid:** automated screening + human spot-check

## Stack
- **lm-evaluation-harness (EleutherAI):** standard benchmarks
- **DeepEval:** pytest-style
- **Promptfoo:** config-driven A/B
- **OpenAI Evals:** Microsoft framework
- **HELM:** Stanford holistic
- **TruLens:** feedback loops
- **MLflow:** experiment tracking

## LLM-as-judge bias mitigation
- **Position bias:** randomize order
- **Length bias:** normalize for length
- **Self-bias:** don't use same model as judge
- **Style bias:** focus on substance
- **Calibration:** multiple judges + agreement
- **Pairwise > scoring:** judges better at A vs B than 1-5 scoring

## Statistical rigor
- **Confidence intervals:** bootstrap
- **Sample size calculator:** minimum for statistical significance
- **Multiple comparisons:** Bonferroni, FDR
- **Effect size:** Cohen's d
- **Power analysis:** detect minimum effect

## Templates
1. Custom eval design (taxonomy)
2. LLM-as-judge prompt engineering
3. Human eval protocol
4. CI/CD eval integration
5. Eval cost optimization
6. Eval report template (model card)

## Cross-references
- [[oraculo-model-evaluation]] · [[oraculo-benchmarking]] · [[demeter-ab-testing]]

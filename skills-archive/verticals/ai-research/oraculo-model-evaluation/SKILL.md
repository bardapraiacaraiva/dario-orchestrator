---
name: oraculo-model-evaluation
description: LLM evaluation — HELM, BIG-Bench, MMLU, custom evals. Triggers em "LLM evaluation", "HELM", "BIG-Bench", "MMLU", "HumanEval", "MT-Bench", "AlpacaEval", "Arena".
license: MIT
parent_agent: oraculo-director
compliance: [research_integrity]
---

# ORACULO-MODEL-EVALUATION

## Benchmarks chave
- **MMLU (Massive Multitask):** 57 subjects, 0-shot/5-shot
- **HumanEval:** code generation 164 problems
- **MBPP:** Mostly Basic Python Problems
- **GSM8K:** grade school math
- **MATH:** competition math
- **HellaSwag:** common sense reasoning
- **TruthfulQA:** truthfulness
- **MT-Bench:** multi-turn conversation
- **AlpacaEval:** instruction following
- **Chatbot Arena (LMSYS):** human preference rankings
- **HELM (Stanford):** holistic evaluation
- **BIG-Bench (Google):** 200+ tasks

## Eval frameworks
- **lm-evaluation-harness (EleutherAI)** — standard
- **HELM (Stanford)** — broader scope
- **OpenAI Evals** — open-source framework
- **DeepEval** — pytest-style
- **Promptfoo** — config-driven
- **TruLens** — RAG eval focus

## Eval dimensions
- **Capability:** accuracy on tasks
- **Alignment:** follows instructions, ethical
- **Robustness:** adversarial, perturbations
- **Calibration:** confidence vs accuracy
- **Latency:** speed per token
- **Cost:** $/M tokens
- **Hallucination:** factuality (FACTSCORE)

## Templates
1. Eval suite design (custom domain)
2. Statistical significance (bootstrap)
3. LLM-as-judge framework (with bias mitigation)
4. Human eval protocol (inter-annotator agreement)
5. Continuous eval pipeline (CI/CD for models)
6. Eval reporting (model card section)

## Cross-references
- [[oraculo-benchmarking]] · [[oraculo-evaluation-frameworks]] · [[demeter-ml-pipelines]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-model-evaluation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-model-evaluation:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->

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

---
name: oraculo-llm-fine-tuning
description: LLM fine-tuning — LoRA, QLoRA, full fine-tune, PEFT, DPO, ORPO. Triggers em "fine-tuning", "LoRA", "QLoRA", "PEFT", "DPO", "ORPO", "instruction tuning", "domain adaptation".
license: MIT
parent_agent: oraculo-director
---

# ORACULO-LLM-FINE-TUNING

## Methods
- **Full fine-tune:** all parameters trained ($$$, full GPU)
- **LoRA (Low-Rank Adaptation):** decompose weight updates (95% savings)
- **QLoRA:** quantized LoRA (4-bit) for consumer GPUs
- **PEFT (Parameter-Efficient Fine-Tuning):** family of methods
- **DPO (Direct Preference Optimization):** alternative to RLHF
- **ORPO:** preference learning + SFT combined
- **Instruction tuning:** SFT on prompt-response pairs
- **Domain adaptation:** continued pretraining on domain corpus

## Stack
- **Hugging Face transformers + PEFT**
- **TRL (Transformer Reinforcement Learning)** — RLHF library
- **axolotl** — config-driven fine-tuning
- **LLaMA-Factory** — training UI
- **Unsloth** — 2x speed fine-tuning
- **Together.AI / Replicate** — managed fine-tuning
- **OpenAI fine-tuning** — managed (GPT-4o-mini, GPT-4.1; ~~GPT-3.5~~ deprecated 2025-07)

## Hardware
- **Consumer:** RTX 4090 (24GB) — QLoRA 7-13B
- **Prosumer:** RTX 6000 Ada (48GB) — QLoRA 70B
- **Workstation:** 4x A100 (320GB) — full 70B
- **Server:** 8x H100 (640GB) — large training
- **Cloud:** RunPod, Vast.ai, Lambda Labs (hourly)

## Data requirements
- **Instruction tuning:** 1K-10K examples
- **Style transfer:** 100-1K examples
- **Domain adaptation:** 100M+ tokens
- **Preference learning:** 5K-50K paired examples

## Templates
1. Fine-tuning project setup
2. Dataset curation + cleaning
3. Hyperparameter search
4. Eval before deploy
5. Deployment (vLLM, TGI, Ollama)
6. Cost calculator (hours × GPU rate)

## Cross-references
- [[demeter-ml-pipelines]] · [[oraculo-evaluation-frameworks]] · [[oraculo-multimodal-research]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-llm-fine-tuning** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-llm-fine-tuning:**

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

---
name: oraculo-multimodal-research
description: Multimodal AI — VLMs, audio, video, embodied, omni-models. Triggers em "multimodal", "VLM", "vision language model", "GPT-4V", "Gemini multimodal", "CLIP", "Flamingo", "omni-model".
license: MIT
parent_agent: oraculo-director
---

# ORACULO-MULTIMODAL-RESEARCH

## Multimodal categories
- **Vision-Language (VLM):** GPT-4V, Gemini, Claude, LLaVA
- **Audio-Language:** Whisper, AudioPaLM, music gen (MusicGen)
- **Video:** Sora (OpenAI), Veo (Google), Movie Gen (Meta), Runway
- **3D:** point clouds, NeRF, Gaussian splatting
- **Embodied:** robotics + language (RT-2 Google)
- **Omni-models:** GPT-4o, Gemini 1.5/2, Claude 3.5+ — handle all natively

## Architecture patterns
- **Cross-attention:** image features → language model
- **Adapter modules:** lightweight modality bridges
- **Unified tokenization:** images → tokens (ViT patches)
- **Multimodal LLMs native:** trained on mixed data from start

## Eval benchmarks
- **MMMU:** Multi-discipline Multimodal Understanding
- **MMBench:** general visual reasoning
- **MathVista:** math + vision
- **POPE:** hallucination evaluation
- **AudioBench:** audio understanding
- **VideoMME:** video understanding

## Stack
- **HuggingFace Transformers + accelerate**
- **LangChain multimodal**
- **LlamaIndex multimodal**
- **Replicate** — hosted model APIs
- **Together.AI** — open model hosting

## Templates
1. Multimodal benchmark suite
2. VLM fine-tuning pipeline
3. Multimodal RAG architecture
4. Hallucination measurement
5. Cross-modal evaluation
6. Embodied agent simulation

## Cross-references
- [[oraculo-model-evaluation]] · [[oraculo-llm-fine-tuning]] · [[oraculo-rag-research]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-multimodal-research** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-multimodal-research:**

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

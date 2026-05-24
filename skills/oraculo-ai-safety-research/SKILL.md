---
name: oraculo-ai-safety-research
description: AI safety methodologies — interpretability, mech interp, scalable oversight. Triggers em "AI safety", "interpretability", "mechanistic interpretability", "mech interp", "circuit analysis", "Anthropic interp", "responsible AI".
license: MIT
parent_agent: oraculo-director
compliance: [audit_immutable, ai_governance, responsible_disclosure]
---

# ORACULO-AI-SAFETY-RESEARCH

## Sub-fields
- **Mechanistic Interpretability:** understand neural circuits
- **Behavioral Interpretability:** input-output patterns
- **Scalable Oversight:** humans supervise superhuman AI
- **Robustness:** adversarial, distribution shift
- **Honesty:** model says what it believes
- **Corrigibility:** model accepts correction
- **Capability evaluations:** dangerous capabilities (METR, Apollo)
- **Power-seeking:** resource acquisition behaviors

## Mechanistic interpretability key concepts
- **Circuits:** specific computations within neural network
- **Features:** what concepts neurons encode (sparse autoencoders)
- **Polysemanticity:** neurons encoding multiple concepts
- **Superposition:** more features than neurons (compressed)
- **Activation patching:** intervention experiments
- **Attribution patching:** scalable activation patching
- **Logit lens:** track predictions through layers

## Stack
- **TransformerLens** — interp library
- **nnsight (NDIF)** — distributed interp
- **Anthropic interpretability** — leading research lab
- **Apollo Research** — model evals
- **METR (ARC Evals)** — frontier capability evals
- **Redwood Research** — safety research

## Key papers/projects 2024-2026
- "Mapping the Mind of a Large Language Model" (Anthropic 2024, paper estudou Claude 3 Sonnet — referência histórica)
- "Sleeper Agents" (Anthropic — deceptive AI)
- "Sparse Autoencoders" — feature discovery
- "Constitutional AI" — alignment without RLHF
- "Frontier Models" eval frameworks (METR)

## Templates
1. Interp experiment design
2. Circuit identification protocol
3. Sparse autoencoder training
4. Adversarial robustness test
5. Capability eval framework
6. Safety case template

## Cross-references
- [[oraculo-alignment-research]] · [[sphinx-ai-security]] · [[lex-ai-governance]] · [[nomos-eu-ai-act-pt]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-ai-safety-research** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-ai-safety-research:**

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

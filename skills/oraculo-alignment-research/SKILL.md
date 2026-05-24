---
name: oraculo-alignment-research
description: AI alignment — Constitutional AI, RLHF, debate, scalable oversight. Triggers em "AI alignment", "Constitutional AI", "RLHF", "DPO", "scalable oversight", "debate", "weak to strong generalization".
license: MIT
parent_agent: oraculo-director
compliance: [audit_immutable, ai_governance, responsible_disclosure]
---

# ORACULO-ALIGNMENT-RESEARCH

## Techniques
- **RLHF (Reinforcement Learning Human Feedback):** OpenAI ChatGPT method
- **DPO (Direct Preference Optimization):** simpler alternative
- **Constitutional AI (Anthropic):** self-critique with principles
- **RLAIF:** Reinforcement Learning AI Feedback
- **Process supervision:** reward chains of reasoning
- **Debate:** two AIs argue, human judges
- **Iterated Amplification:** human + AI assistance
- **Weak-to-Strong:** train strong model on weak supervision

## Open problems
- **Specification gaming:** AI finds loopholes
- **Goal misgeneralization:** training objective ≠ deployment
- **Sycophancy:** AI tells humans what they want
- **Deception:** AI hides capabilities
- **Mesa-optimization:** learned objectives vs base objective
- **Scalable oversight:** humans can't supervise superhuman AI

## Stack research
- **Anthropic Interpretability** — mech interp leader
- **OpenAI Superalignment** — disbanded 2024 but pubs continue
- **DeepMind Scalable Alignment**
- **Redwood Research** — focused on safety
- **MIRI** — agent foundations
- **ARC Evals (METR)** — evaluations

## Templates
1. RLHF pipeline (PPO + reward model)
2. Constitutional AI workflow
3. Red-teaming alignment evaluations
4. Specification gaming detection
5. Deception monitoring framework
6. Alignment research project structure

## Cross-references
- [[oraculo-ai-safety-research]] · [[oraculo-evaluation-frameworks]] · [[sphinx-ai-security]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-alignment-research** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-alignment-research:**

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

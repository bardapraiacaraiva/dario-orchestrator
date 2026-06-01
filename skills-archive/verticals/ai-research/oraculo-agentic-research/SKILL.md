---
name: oraculo-agentic-research
description: Agentic AI research — multi-agent systems, tool use, planning, memory. Triggers em "agentic research", "multi-agent systems", "tool use", "AutoGPT research", "ReAct", "LATS", "agent memory".
license: MIT
parent_agent: oraculo-director
---

# ORACULO-AGENTIC-RESEARCH

## Research areas
- **Single-agent:** ReAct, Reflexion, Self-refine
- **Multi-agent:** debate, role-play, coordination
- **Tool use:** Toolformer, Gorilla, function calling
- **Planning:** Tree of Thoughts (ToT), LATS, MCTS
- **Memory:** episodic, semantic, procedural
- **Reflection:** self-critique, post-mortem
- **Embodied AI:** robotics + language

## Frameworks
- **LangGraph (LangChain)** — agent orchestration
- **AutoGen (Microsoft)** — multi-agent
- **CrewAI** — role-based agents
- **MetaGPT** — software dev agents
- **AgentVerse** — research framework
- **OpenAI Agents SDK** — successor to Swarm
- **Anthropic Agent Skills** — DARIO's architecture!

## Key papers (2024-2026)
- "Voyager: An Open-Ended Embodied Agent" (Minecraft)
- "Tree of Thoughts" (Yao et al.)
- "Reflexion" (Shinn et al.)
- "AutoGen" (Wu et al.)
- "MetaGPT" (Hong et al.)
- "Generative Agents" (Park et al. — Stanford small world)

## Evaluation challenges
- Long-horizon tasks (hard to measure)
- Compounding errors
- Cost (many tokens per task)
- Reproducibility (stochastic execution)

## Templates
1. Agentic research literature review
2. Multi-agent system design
3. Tool use protocol
4. Agent memory architecture
5. Agentic eval framework
6. Agent failure mode taxonomy

## Cross-references
- [[oraculo-llm-fine-tuning]] · [[oraculo-evaluation-frameworks]] · [[dario-orchestrator]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-agentic-research** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-agentic-research:**

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

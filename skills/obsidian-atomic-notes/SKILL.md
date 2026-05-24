---
name: obsidian-atomic-notes
description: Atomic notes — one idea per note, evergreen notes, durable knowledge. Triggers em "atomic notes", "evergreen notes", "Andy Matuschak", "permanent notes", "Zettelkasten atomic".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification]
---

# OBSIDIAN-ATOMIC-NOTES

## Filosofia
**One idea per note. Reusable. Self-contained. Densely linked.** Andy Matuschak's evergreen notes.

## Princípios
- **Atomic:** uma ideia por nota (não capítulo)
- **Concept-oriented:** título = ideia (não tópico amplo)
- **Densely linked:** mínimo 3 links saída
- **Reusable:** descontextualizada da sua origem
- **Evergreen:** maturidade evolui ao longo do tempo

## Quando usar
- Bootstrap de Zettelkasten / evergreen system
- Refactor de notas "long form" → atomic
- Quality audit de notas existentes
- Teach team to write atomic

## Anti-patterns
- ❌ "My thoughts on book X" — não atomic
- ❌ "Project planning notes" — não atomic
- ❌ Single notes >1000 words (probably múltiplas ideias)
- ❌ Untitled notes / dated titles

## Templates
1. Atomic note template (concept-oriented title + 3 links min + tags)
2. Evergreen note maturity stages (fleeting → literature → permanent → evergreen)
3. Note splitting workflow (long → atomic)
4. Link density audit (graph view metrics)

## Cross-references
- [[obsidian-zettelkasten-method]] · [[obsidian-second-brain]] · [[obsidian-cross-referencing]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-atomic-notes** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-atomic-notes:**

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

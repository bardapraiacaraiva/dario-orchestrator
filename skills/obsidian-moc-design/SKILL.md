---
name: obsidian-moc-design
description: Maps of Content (MOC) — navegação curada para temas, hierarquia leve. Triggers em "MOC", "map of content", "index notes", "hub notes", "knowledge map".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification]
---

# OBSIDIAN-MOC-DESIGN

## Filosofia (Nick Milo)
**MOCs são curadoria, não taxonomia rígida.** Substitui folders profundos por entry points navegáveis.

## Quando usar
- Vault crescente sem navegação clara
- Substituir folder hierarchy por links
- Onboarding novo membro ao knowledge base
- Knowledge sharing público (digital garden)

## Tipos de MOC
- **Index MOC:** lista hierárquica de notas
- **Hub MOC:** entry point para um tópico
- **Workbench MOC:** notas em progresso
- **Personal MOC:** "About me" hub

## Templates
1. Topic MOC template (intro + key notes + sub-topics + recent)
2. Project MOC template (goal + status + notes + decisions)
3. Person MOC template (relationship + interactions + topics)
4. Author MOC template (books + insights + influences)

## Princípios
- **Curate, don't catalog:** seleciona, não lista tudo
- **Living docs:** MOCs evoluem
- **Multiple paths:** mesma nota pode ser linked de N MOCs
- **Top of hierarchy:** MOC of MOCs (personal home)

## Cross-references
- [[obsidian-para-organization]] · [[obsidian-atomic-notes]] · [[obsidian-cross-referencing]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-moc-design** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-moc-design:**

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

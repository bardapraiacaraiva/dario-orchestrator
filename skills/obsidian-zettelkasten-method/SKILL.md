---
name: obsidian-zettelkasten-method
description: Zettelkasten (Luhmann) — Fleeting/Literature/Permanent notes, ID system, evergreen knowledge. Triggers em "Zettelkasten", "Luhmann", "permanent notes", "literature notes", "Sönke Ahrens".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification]
---

# OBSIDIAN-ZETTELKASTEN-METHOD

## Origem
Niklas Luhmann produziu 70+ livros + 400+ artigos usando 90K Zettel (slip notes).

## Tipos de notas
1. **Fleeting:** capturas rápidas (inbox)
2. **Literature:** resumos de fontes (com cite)
3. **Permanent:** ideias atomicas, evergreen
4. **Index/Structure:** MOCs equivalent

## Workflow (Ahrens "How to Take Smart Notes")
```
Read → Highlight → Literature note → Permanent note → Link → Index
```

## Sistema de ID
- Luhmann original: 1, 1a, 1a1, 1a1a... (hierarquia inferida)
- Folgezettel digital: timestamp YYYYMMDDhhmm
- Or descriptive slug: `concept-name`

## Templates
1. Zettelkasten setup em Obsidian (folders + templates)
2. Literature note template (source + key points + my thoughts)
3. Permanent note template (atomic + densely linked)
4. Folgezettel naming convention
5. Index note (Structure-Zettel) examples

## Cross-references
- [[obsidian-atomic-notes]] · [[obsidian-second-brain]] · [[obsidian-cross-referencing]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-zettelkasten-method** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-zettelkasten-method:**

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

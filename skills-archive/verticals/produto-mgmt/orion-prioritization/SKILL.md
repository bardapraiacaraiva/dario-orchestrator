---
name: orion-prioritization
description: Frameworks de prioritização — RICE, ICE, MoSCoW, Kano, WSJF, Cost of Delay. Triggers em "prioritization", "RICE", "ICE", "MoSCoW", "Kano", "WSJF", "priorização".
license: MIT
parent_agent: orion-director
compliance: [data_privacy_by_design]
---

# ORION-PRIORITIZATION

## Quando usar
- Backlog grooming (100+ items, qual primeiro?)
- Quarterly planning trade-offs
- Roadmap commit decisions
- Effort vs impact alignment com eng
- Stakeholder pushback ("why not feature X first?")

## Frameworks (quando usar cada um)
- **RICE (Intercom):** R × I × C / E — quando tens dados quantitativos
- **ICE (Sean Ellis):** Impact × Confidence × Ease — quando velocidade > precisão
- **MoSCoW:** Must/Should/Could/Won't — para scope MVP
- **Kano:** basic/performance/excitement — para feature mix
- **WSJF (SAFe):** Cost of Delay / Job Size — para enterprise/agile
- **Opportunity Scoring (Ulwick):** importance + satisfaction
- **Buy a Feature:** workshop colaborativo com stakeholders

## Templates
1. RICE spreadsheet template (com formulae)
2. ICE workshop facilitation guide
3. MoSCoW MVP scope template
4. Kano model survey
5. Cost of Delay calculator

## Anti-patterns
- ❌ HiPPO (Highest Paid Person's Opinion)
- ❌ Loudest customer wins
- ❌ Squeaky wheel (last bug fixed first)
- ❌ Frameworks treated as oracle (eles informam, não decidem)

## Cross-references
- [[orion-roadmap-planning]] · [[orion-product-strategy]] · [[demeter-ab-testing]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-prioritization** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-prioritization:**

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

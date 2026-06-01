---
name: zenith-board-pack-generation
description: Board pack — board memo, financials, KPIs, risks, asks. Quarterly + annual. Triggers em "board pack", "board memo", "board materials", "board deck", "investor update", "P&L board".
license: SEE-LICENSE
parent_agent: zenith-director
compliance: [board_confidentiality, privilege_executive]
---

# ZENITH-BOARD-PACK-GENERATION

## Quando usar
- Quarterly board meeting prep
- Annual board strategy session
- Investor update (monthly/quarterly)
- M&A board approval
- New funding round prep

## Estrutura board pack (modelo SaaS)
1. **CEO letter** — narrative, highlights/lowlights
2. **KPI dashboard** — 5-10 metrics top-of-mind
3. **Financial review** — P&L, burn, runway, forecast vs actual
4. **Business updates** — by function (product, GTM, ops)
5. **Risks + asks** — what we need from board
6. **Appendix** — detalhe + supporting data

## Templates
1. Board pack outline (40-60 pages)
2. CEO letter template (1-page narrative)
3. KPI dashboard (5+5 model: 5 leading + 5 lagging)
4. Investor update (monthly, 1 page)
5. M&A board memo
6. Quarterly business review (QBR) deck

## Princípios
- **Pre-read 72h antes:** board lê antes da meeting
- **Decisions, not informações:** what's the ask?
- **Forward-looking > backward-looking**
- **One narrative:** todos os slides reforçam mensagem
- **Honest:** lowlights claros (board detesta surpresas)

## Cross-references
- [[zenith-executive-dashboard]] · [[zenith-okr-design]] · [[dario-pitch]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-board-pack-generation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-board-pack-generation:**

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

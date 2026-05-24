---
name: zenith-scenario-planning
description: Scenario planning — Shell scenarios, alternative futures, plausible futures. Triggers em "scenario planning", "Shell scenarios", "Pierre Wack", "alternative futures", "future thinking", "cenários".
license: SEE-LICENSE
parent_agent: zenith-director
compliance: [privilege_executive]
---

# ZENITH-SCENARIO-PLANNING

## Filosofia (Pierre Wack, Shell)
**Plan against multiple plausible futures, not point estimates.** Premortem para 4 mundos diferentes.

## Quando usar
- Strategic uncertainty alta (geopolitical, technology disruption)
- Long-term planning (5-10y horizon)
- M&A under uncertainty
- Regulatory change anticipation
- Climate / sustainability transition

## Método (4-scenario grid)
1. **Identify critical uncertainties** — driving forces with high impact + high uncertainty
2. **Select 2 axes** — orthogonal, plausible
3. **Build 4 scenarios** — quadrants (e.g., high/low tech adoption × high/low regulation)
4. **Narratives:** name each, write story (how do we get there?)
5. **Implications:** strategy per scenario
6. **Robust strategy:** what works em todos?
7. **Indicators:** sinais que indicam qual cenário se está a materializar

## Templates
1. Driving forces workshop
2. 2×2 scenario grid template
3. Scenario narrative (10-page story per quadrant)
4. Strategic implications matrix
5. Early warning indicators dashboard
6. Scenario refresh cadence (annual)

## Cross-references
- [[zenith-strategic-planning]] · [[zenith-monte-carlo]] · [[zenith-war-gaming]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-scenario-planning** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-scenario-planning:**

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

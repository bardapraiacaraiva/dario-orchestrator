---
name: zenith-succession-planning
description: Leadership succession — talent grid (9-box), succession plans, board succession, CEO transition. Triggers em "succession planning", "talent grid", "9-box", "CEO transition", "leadership pipeline", "key person risk".
license: SEE-LICENSE
parent_agent: zenith-director
compliance: [privilege_executive, board_confidentiality]
---

# ZENITH-SUCCESSION-PLANNING

## Quando usar
- CEO transition (10y+ tenure ou retirement)
- C-level succession (CFO, COO, etc.)
- Board succession (term limits, refresh)
- Family business transition (next gen)
- Founder transition (founder-led → professional management)

## Frameworks
- **9-Box Grid:** performance × potential
- **Bench strength:** how many ready + how soon (Ready Now / 1-2y / 3-5y)
- **Emergency succession:** if CEO hit-by-bus tomorrow
- **Long-term succession:** 3-5y planned transition
- **Internal vs external:** trade-offs

## Templates
1. 9-box assessment template (per C-level position)
2. Successor profile (current capacities + gaps + dev plan)
3. Emergency succession plan (24h activation)
4. CEO transition playbook (announce → onboard → handoff)
5. Board succession grid (skills × tenure × diversity)
6. Founder transition roadmap (5y horizon)

## Princípios
- **Don't tell the candidate:** prematurely creates expectations
- **Multiple successors:** 2-3 per role mínimo
- **Active development:** stretch assignments, exposure
- **Board involvement:** CEO succession = board job
- **External benchmark:** even when internal favorite

## Cross-references
- [[pessoa-sucessao]] · [[zenith-board-pack-generation]] · [[pessoa-orgdesign]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-succession-planning** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-succession-planning:**

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

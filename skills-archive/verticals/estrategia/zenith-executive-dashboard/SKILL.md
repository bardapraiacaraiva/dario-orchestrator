---
name: zenith-executive-dashboard
description: Executive dashboards — CEO/CFO/COO dashboards, leading vs lagging, narrative-driven. Triggers em "executive dashboard", "CEO dashboard", "CFO dashboard", "board dashboard", "executive KPIs".
license: SEE-LICENSE
parent_agent: zenith-director
compliance: [privilege_executive]
---

# ZENITH-EXECUTIVE-DASHBOARD

## Filosofia
**5-10 metrics max. Leading + lagging. Single narrative.** Executives have 30 seconds.

## Quando usar
- CEO dashboard greenfield
- Board pack KPI section
- All-hands metric pack
- M&A target performance tracking
- PE portfolio dashboard

## Métricas por role
- **CEO:** revenue + NPS + employee NPS + cash runway + strategic OKR
- **CFO:** ARR growth + gross margin + burn + DSO + cash runway
- **COO:** customer health + ops uptime + ticket SLA + delivery on-time
- **CRO:** ARR + pipeline + win rate + sales cycle + NRR
- **CPO:** activation + retention + NPS + NSM + roadmap delivery

## Templates
1. CEO dashboard (5+5 model)
2. Board pack KPI page
3. SaaS metrics dashboard (CAC, LTV, NRR, churn, magic number)
4. PE portfolio dashboard (across companies)
5. M&A target performance tracking

## Princípios
- **5 metrics, not 50**
- **Trend over snapshot:** 12-month trend
- **Vs target + vs PY**
- **Color carefully:** semáforo green/yellow/red
- **Annotated:** spike → "why"

## Cross-references
- [[zenith-board-pack-generation]] · [[zenith-okr-design]] · [[demeter-bi-dashboard]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-executive-dashboard** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-executive-dashboard:**

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

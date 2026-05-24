---
name: mercurius-sales-ops
description: Sales Ops + RevOps — Salesforce admin, tooling stack, processes, automations. Triggers em "sales ops", "RevOps", "Salesforce admin", "sales tools", "sales stack", "sales process".
license: MIT
parent_agent: mercurius-director
compliance: [audit_trail]
---

# MERCURIUS-SALES-OPS

## RevOps function
- **Salesforce admin** (or HubSpot, Pipedrive)
- **Tool stack management** — integration + adoption
- **Process design** — opportunity stages, MEDDIC fields
- **Data quality** — dedupe, enrichment, hygiene
- **Reporting + dashboards** — pipeline, activity, forecast
- **Sales automations** — sequences, alerts, handoffs

## Stack (típico SaaS)
- **CRM:** Salesforce (enterprise), HubSpot (SMB), Pipedrive (small)
- **Sales engagement:** Outreach, Salesloft, Apollo
- **Call intelligence:** Gong, Chorus
- **CPQ:** Salesforce CPQ, DealHub, PandaDoc
- **e-Signature:** DocuSign, Adobe Sign
- **Data:** ZoomInfo, Apollo, Clearbit
- **Forecasting:** Clari, BoostUp, InsightSquared
- **Sales enablement:** Highspot, Seismic

## Salesforce opportunity stages (recommended)
1. Discovery (10%)
2. Qualified (25%)
3. Proposal/Demo (50%)
4. Negotiation (75%)
5. Verbal Close (90%)
6. Closed Won (100%)
7. Closed Lost (0%)

## Templates
1. Salesforce data model (Account/Opp/Contact)
2. MEDDIC custom fields setup
3. Sales process documentation
4. Tool selection scorecard
5. Data quality SOP
6. Reporting dashboard library (10 default)
7. Automation playbook (handoffs, alerts)

## Cross-references
- [[mercurius-pipeline-forecasting]] · [[mercurius-comp-plan]] · [[demeter-data-quality]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-sales-ops** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-sales-ops:**

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

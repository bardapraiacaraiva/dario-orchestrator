---
name: atlas-fin-aml-monitoring
description: AML transaction monitoring — rules, ML detection, SARs to COAF (BR) + UIF (PT). Triggers em "AML monitoring", "transaction monitoring", "COAF", "UIF Portugal", "SAR", "suspicious activity", "AMLD6".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable, sanctions_realtime]
---

# ATLAS-FIN-AML-MONITORING

## Marco
- **BR:** Lei 9.613/1998 + Circular Bacen 3978/2020 + COAF
- **PT:** Lei 83/2017 + UIF Portugal
- **EU:** AMLD6 (Directive 2024/1640) — applicable Jul 2027
- **FATF Recommendations** (40+9)

## Stack
- **NICE Actimize** — enterprise líder
- **SAS AML** — banking traditional
- **Hummingbird (now ComplyAdvantage)** — modern
- **Trapets** — Nordics
- **Quantexa** — graph-based, network analysis
- **BR-specific:** Spline, Avantia, IDtech

## Detection rules (típicas)
- **Structuring:** múltiplas transações just below threshold
- **Unusual velocity:** spike inexplicado
- **High-risk countries:** transferências OFAC, FATF blacklist
- **PEP transactions:** politicamente exposto + alto valor
- **Round numbers:** R$ 10.000, R$ 50.000 (money laundering signals)
- **New account, large transaction:** D-7 risk
- **Dormant → active:** account "wake up" pattern

## Workflow
```
1. Real-time monitoring (rules + ML)
2. Alert triage (level 1)
3. Investigation (level 2)
4. SAR filing decision
5. Submit COAF (BR) / UIF (PT)
6. Recordkeeping (5 years BR, 7 EU)
```

## Templates
1. AML monitoring rules library (50+ rules)
2. Alert triage workflow
3. SAR template COAF + UIF
4. Investigation case file structure
5. Annual independent review framework
6. Training curriculum AML staff

## Cross-references
- [[atlas-fin-sanctions-screening]] · [[atlas-fin-kyc-onboarding]] · [[nomos-kyc-aml-pt]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-aml-monitoring** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-aml-monitoring:**

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

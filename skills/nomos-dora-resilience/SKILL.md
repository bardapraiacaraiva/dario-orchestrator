---
name: nomos-dora-resilience
description: DORA — Digital Operational Resilience Act, Regulamento (UE) 2022/2554. ICT risk, incident reporting, TLPT, third-party. Triggers em "DORA", "Digital Operational Resilience Act", "TLPT", "ICT risk", "Regulamento 2022/2554", "Resilience Act".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [dora_testing_schedule, audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-DORA-RESILIENCE

## Marco
- **Regulamento (UE) 2022/2554 (DORA)** — Digital Operational Resilience Act
- **Application date:** 17 Jan 2025
- **Aplicação a:** todas entidades financeiras EU (bancos, seguradoras, fundos, fintechs, payment institutions, crypto)
- **5 pillars:** ICT Risk Management, Incident Reporting, Resilience Testing, Third-Party Risk, Information Sharing

## 5 Pillars DORA

### 1. ICT Risk Management
- Framework alinhado com NIS2
- Board-level oversight
- Annual review
- Documented policies (ICT security, change mgmt, BCM)

### 2. Incident Reporting
- Major ICT incident → 4h initial notification BdP/CMVM
- 72h intermediate report
- 1 month final report
- Voluntary reporting cyber threats

### 3. Resilience Testing
- **Basic testing:** annual (vulnerability assessments, scenario-based)
- **TLPT (Threat-Led Penetration Testing):** every 3 years for significant entities
- TLPT must use external testers (not in-house)

### 4. Third-Party ICT Risk
- ICT service provider register
- Concentration risk monitoring
- Critical ICT services contractual requirements
- ESAs designation of "Critical ICT Third-Party Providers" (CTPPs)

### 5. Information Sharing (voluntary)
- Cyber threat intelligence exchange

## Quando usar
- DORA gap analysis (entity financeira PT)
- ICT incident workflow setup
- TLPT engagement preparation
- ICT contracts revision (40+ mandatory clauses)
- Operational resilience board reporting

## Templates
1. DORA gap analysis 5 pillars
2. ICT risk management framework
3. Incident classification + reporting workflow
4. TLPT scoping + RoE
5. ICT third-party register
6. Contract review checklist (Art. 30 mandatory clauses)
7. Board operational resilience pack

## Coimas
- **Significant entities:** até 2% annual turnover
- **CTPPs:** até 1% daily worldwide turnover during non-compliance period

## Cross-references
- [[nomos-bdp-banking-pt]] · [[aegis-compliance-frameworks]] · [[aegis-incident-response]] · [[aegis-third-party-risk]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-dora-resilience** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-dora-resilience:**

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

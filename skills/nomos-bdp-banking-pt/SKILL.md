---
name: nomos-bdp-banking-pt
description: Banco de Portugal — supervisão prudencial, AML, capital requirements, RGICSF. Triggers em "Banco de Portugal", "BdP", "supervisão bancária PT", "RGICSF", "capital requirements", "Aviso BdP", "Carta Circular BdP".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [bdp_regulatory_reporting_gate, audit_immutable]
jurisdiction: Portugal
---

# NOMOS-BDP-BANKING-PT

## Marco
- **RGICSF (Regime Geral das IC e SF)** — DL 298/92 (multi-amended)
- **CRD V/CRR 2** — Capital Requirements (EU 2019/878, 2019/876)
- **BRRD II** — Bank Recovery and Resolution Directive
- **PSD2 + DL 91/2018** — Payment Services
- **Aviso BdP 2/2018** — Continuidade negócio
- **Aviso BdP 3/2020** — Cybersec
- **Circulares BdP** — interpretação prática

## Quando usar
- IC (Instituição de Crédito) authorization request
- Anti-money laundering program setup
- ICAAP/ILAAP submission
- Recovery plan + resolution plan
- Operational resilience (DORA combined)
- Stress testing EBA/BdP

## Pillars (Basel III/IV)
- **Pillar 1:** minimum capital requirements (CET1 ≥ 4.5%, T1 ≥ 6%, total ≥ 8%)
- **Pillar 2:** SREP (Supervisory Review) + ICAAP
- **Pillar 3:** market discipline + disclosures

## Templates
1. ICAAP documentation structure
2. ILAAP (liquidity) framework
3. Recovery plan template (8 sections RGICSF)
4. Operational risk loss data collection
5. AML/CFT policy (Lei 83/2017)
6. Suspicious Transaction Report (UIF)
7. RAS (Risk Appetite Statement) board-approved

## Compliance gates
- CET1 ratio monitoring (auto-alert if < buffer)
- ICAAP annual deadline (31 March)
- Liquidity coverage ratio (LCR ≥ 100%)
- NSFR (Net Stable Funding Ratio ≥ 100%)
- Large exposures monitoring

## Cross-references
- [[nomos-dora-resilience]] · [[nomos-kyc-aml-pt]] · [[nomos-mifid-ii-pt]] · [[atlas-fin-regulatory-reporting-bcb]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-bdp-banking-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-bdp-banking-pt:**

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

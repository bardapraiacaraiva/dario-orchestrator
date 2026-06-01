---
name: kirion-ifrs-16-leases
description: IFRS 16 leases — RoU asset, lease liability, off-balance to on-balance. Triggers em "IFRS 16", "leases accounting", "RoU asset", "lease liability", "operating lease", "finance lease", "CPC 06".
license: SEE-LICENSE
parent_agent: kirion-director
compliance: [ifrs_16_reporting, audit_immutable]
---

# KIRION-IFRS-16-LEASES

## Marco
- **IFRS 16 (2019)** — replaces IAS 17
- **CPC 06 (R2)** — BR equivalent
- **US GAAP ASC 842** — similar mas mantém operating distinction
- **Lessor accounting:** unchanged largely
- **Lessee accounting:** dramatic change — quase tudo on-balance sheet

## Lessee accounting
- **At inception:** record RoU asset + Lease liability
- **RoU asset:** = Lease liability + initial costs + restoration
- **Lease liability:** PV of lease payments at IBR (Incremental Borrowing Rate)
- **Subsequent:** depreciate RoU + interest expense on liability
- **Cash flow:** principal in financing + interest in operating

## Exemptions IFRS 16
- **Short-term:** ≤ 12 months
- **Low-value:** ≤ ~US$ 5K
- **(Lessor accounting:** distinguish operating vs finance lease)

## Quando aplica
- Real estate leases (office, retail, warehouse)
- Equipment leases (machinery, vehicles, IT)
- Mining rights
- Power Purchase Agreements (PPAs) — careful: maybe IFRS 16 if specific asset

## Templates
1. Lease classification decision tree
2. RoU asset + Lease liability calculation
3. IBR determination
4. Reassessment triggers (modifications)
5. Disclosure template per IFRS 16 paras 51-60
6. Lease modifications accounting

## Cross-references
- [[kirion-leasing-strategy]] · [[conta-relatorios]] · [[zenith-board-pack-generation]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-ifrs-16-leases** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-ifrs-16-leases:**

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

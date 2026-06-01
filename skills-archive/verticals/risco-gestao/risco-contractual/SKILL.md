---
name: risco-contractual
description: "Contract compliance — obligation tracking, SLA monitoring, penalty management, contract lifecycle"
version: "1.0"
---

# RISCO-CONTRACTUAL: Contract Compliance Skill

## When to Activate

**Trigger words (PT):** contrato, obrigacoes contratuais, sla, penalidades, renovacao contrato, clausulas, incumprimento, garantia, prazo, rescisao, aditamento, compliance contratual
**Trigger words (EN):** contract, contractual obligations, sla, penalties, contract renewal, clauses, breach of contract, warranty, deadline, termination, amendment, contract compliance, contract management

## Step-by-Step Workflow

### Phase 1: Contract Inventory
1. Catalog all active contracts (clients, vendors, partners, leases, licenses)
2. Record key metadata: parties, dates, value, renewal terms, governing law
3. Classify by type: service, procurement, lease, license, employment, NDA
4. Classify by risk: high (>EUR 100K or critical operations), medium, low
5. Designate contract owner per agreement
6. Store originals in secure, searchable repository

### Phase 2: Obligation Extraction
1. Review each contract for obligations (ours and counterparty)
2. Extract: deliverables, milestones, payment terms, reporting requirements
3. Extract: SLAs, KPIs, performance metrics
4. Extract: penalty/liquidated damages clauses
5. Extract: termination triggers, notice periods
6. Create obligation register with deadlines and owners

### Phase 3: SLA Monitoring
1. Define SLA metrics and measurement methodology
2. Establish data collection and reporting cadence
3. Track SLA performance vs target (monthly dashboard)
4. Calculate SLA credits/penalties when breached
5. Trigger escalation for repeated SLA failures
6. Document SLA waivers or exceptions

### Phase 4: Penalty & Dispute Management
1. Track penalty triggers and calculation formulas
2. Issue penalty notices per contractual procedure
3. Document disputes and counterparty responses
4. Escalation path: account manager → legal → mediation → litigation
5. Maintain dispute register with status and financial exposure
6. Settle or enforce per cost-benefit analysis

### Phase 5: Renewal & Expiry Management
1. Calendar all renewal/expiry dates (alert at 180, 90, 30 days)
2. Assess contract performance before renewal decision
3. Renegotiate terms based on performance data
4. Decide: renew, renegotiate, terminate, or re-tender
5. Ensure no auto-renewal without conscious decision
6. Transition plan for contract termination/change of vendor

### Phase 6: Compliance Monitoring
1. Periodic compliance checks against obligation register
2. Audit counterparty compliance (sub-contractor cascade)
3. Track regulatory changes affecting contract terms
4. Amendment management: proper execution and filing
5. Annual contract portfolio review for risk concentration
6. Report to management on contract risk profile

## Commands Table

| Command | Description |
|---------|-------------|
| `risco contract inventory` | Contract portfolio register template |
| `risco contract obligations` | Obligation extraction checklist |
| `risco contract sla` | SLA tracking dashboard |
| `risco contract penalty` | Penalty management procedure |
| `risco contract renewal` | Renewal/expiry calendar |
| `risco contract review` | Contract compliance review template |
| `risco contract risk` | Contract risk assessment |
| `risco contract template` | Standard contract clause library |

## Output Template

```markdown
# Contract Compliance Report — [Organization]
**Date:** YYYY-MM-DD | **Period:** [Q/Year] | **Total Active Contracts:** X

## 1. Portfolio Summary
| Category | Count | Total Value | High Risk | Expiring <90d |
|----------|-------|-------------|-----------|---------------|

## 2. Obligation Tracker (Top Items)
| Contract | Obligation | Owner | Deadline | Status | Risk |
|----------|-----------|-------|----------|--------|------|

## 3. SLA Performance
| Contract | SLA Metric | Target | Actual | Status | Penalty |
|----------|-----------|--------|--------|--------|---------|

## 4. Renewal Calendar (Next 6 Months)
| Contract | Counterparty | Value | Expiry | Action | Decision Date |
|----------|-------------|-------|--------|--------|---------------|

## 5. Active Disputes
| Contract | Issue | Exposure (EUR) | Status | Next Step |
|----------|-------|---------------|--------|-----------|

## 6. Recommendations
| # | Issue | Risk | Action | Priority |
|---|-------|------|--------|----------|

## 7. Next Review: YYYY-MM-DD
```

## Red Flags

- No central contract register (contracts scattered or lost)
- Contract obligations not extracted or tracked
- Auto-renewals triggered without review
- SLA breaches not monitored or not invoking penalty clauses
- Contracts expired but services still being provided/received
- No termination notice sent within required notice period
- Amendments verbal only (not properly documented/signed)
- Key person dependency for contract knowledge (no handover)
- No counterparty compliance verification
- Penalty clauses never enforced despite repeated breaches
- Concentration risk: single vendor for critical operations
- RGPD/data processing clauses missing from vendor contracts


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **risco-contractual** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in risco-contractual:**

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

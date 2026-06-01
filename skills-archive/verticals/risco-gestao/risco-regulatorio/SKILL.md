---
name: risco-regulatorio
description: "Regulatory monitoring — legislative change tracking, compliance calendar, regulatory impact assessment"
version: "1.0"
---

# RISCO-REGULATORIO: Regulatory Monitoring Skill

## When to Activate

**Trigger words (PT):** regulatorio, legislacao, diario da republica, regulamento, directiva, transposicao, obrigacao legal, calendario de compliance, impacto regulatorio, lei nova, alteracao legislativa
**Trigger words (EN):** regulatory, legislation, regulation, directive, transposition, legal obligation, compliance calendar, regulatory impact, new law, legislative change, regulatory monitoring, horizon scanning

## Step-by-Step Workflow

### Phase 1: Regulatory Universe Mapping
1. Identify all applicable regulations by jurisdiction (PT, EU, international)
2. Categorize by domain: corporate law, tax, employment, data protection, AML, sector-specific, environmental, H&S, consumer protection
3. Map regulations to business units/processes responsible
4. Document: regulation name, reference, effective date, supervisory authority
5. Identify sector-specific regulators (BdP, CMVM, ASF, ASAE, CNPD, APA, ACT, ANACOM)

### Phase 2: Horizon Scanning
1. Monitor sources:
   - Diario da Republica (dre.pt) — PT legislation
   - EUR-Lex — EU legislation and proposals
   - Sector regulator websites and newsletters
   - Industry associations and legal advisors
   - Government consultation portals (consultalex.gov.pt)
2. Flag: new laws, amendments, draft proposals, consultations, guidance
3. Assess relevance to organization (applicable / watch / not applicable)
4. Weekly regulatory scan report to compliance team

### Phase 3: Impact Assessment
1. For each relevant change:
   - Summarize change and effective date
   - Identify affected processes, systems, people, contracts
   - Assess compliance gap (what needs to change)
   - Estimate effort and cost to comply
   - Define implementation timeline
2. Risk-rate non-compliance consequences (fines, sanctions, reputational)
3. Present to management for resource allocation

### Phase 4: Compliance Calendar
1. Build rolling 12-month calendar with all regulatory deadlines
2. Include: filing dates, reporting deadlines, renewal dates, training due dates
3. Assign owners to each obligation
4. Set reminders: 90, 60, 30, 7 days before deadline
5. Track completion status (done, in progress, overdue)
6. Monthly calendar review with compliance team

### Phase 5: Implementation Tracking
1. Create project plan for each significant regulatory change
2. Track: policy updates, process changes, system changes, training
3. Document evidence of compliance (policies, records, screenshots)
4. Conduct post-implementation verification
5. Update regulatory register with new status

### Phase 6: Regulatory Reporting
1. Annual regulatory compliance report to Board
2. Quarterly update on regulatory changes pipeline
3. Immediate escalation for high-impact changes
4. Maintain regulatory correspondence register
5. Document regulatory inspections and outcomes

## Commands Table

| Command | Description |
|---------|-------------|
| `risco reg scan` | Regulatory horizon scan report |
| `risco reg calendar` | Compliance calendar template |
| `risco reg impact` | Regulatory impact assessment |
| `risco reg universe` | Regulatory universe mapping |
| `risco reg track` | Implementation tracking dashboard |
| `risco reg report` | Regulatory compliance summary |
| `risco reg deadline` | Upcoming deadlines alert |
| `risco reg filing` | Filing and reporting obligations list |

## Output Template

```markdown
# Regulatory Monitoring Report — [Organization]
**Date:** YYYY-MM-DD | **Period:** [Month/Quarter] | **Compliance Officer:** [Name]

## 1. Regulatory Changes Pipeline
| # | Regulation | Type | Effective Date | Impact | Status |
|---|-----------|------|---------------|--------|--------|
| | | New/Amendment/Repeal | | High/Med/Low | |

## 2. Compliance Calendar (Next 90 Days)
| Deadline | Obligation | Authority | Owner | Status |
|----------|-----------|-----------|-------|--------|

## 3. Overdue Items
| Obligation | Original Deadline | Days Overdue | Risk | Owner |
|-----------|------------------|-------------|------|-------|

## 4. Implementation Progress
| Regulation | Start | Target | % Complete | Blocker |
|-----------|-------|--------|-----------|---------|

## 5. Regulatory Universe Summary
| Domain | Regulations | Compliant | Gaps | Watch List |
|--------|-----------|-----------|------|------------|

## 6. Regulatory Inspections/Inquiries
| Date | Authority | Subject | Outcome | Actions |
|------|-----------|---------|---------|---------|

## 7. Next Review: YYYY-MM-DD
```

## Red Flags

- No systematic regulatory monitoring process
- Regulatory changes discovered after effective date
- Compliance calendar missing or not actively maintained
- Deadlines missed without detection
- No impact assessment for significant regulatory changes
- Single person dependency for regulatory knowledge
- Sector-specific regulations not mapped
- EU directives not tracked during transposition period
- No Board-level reporting on regulatory compliance
- Regulatory correspondence not logged or followed up
- Historical compliance gaps never remediated
- No budget allocated for regulatory change implementation


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **risco-regulatorio** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in risco-regulatorio:**

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

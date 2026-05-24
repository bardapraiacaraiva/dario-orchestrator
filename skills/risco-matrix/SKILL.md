---
name: risco-matrix
description: "Risk matrix — likelihood x impact scoring, heat map generation, mitigation planning, risk register management"
version: "1.0"
---

# RISCO-MATRIX: Risk Assessment Matrix Skill

## When to Activate

**Trigger words (PT):** matriz de risco, avaliacao de risco, probabilidade, impacto, mapa de calor, registo de riscos, mitigacao, apetite ao risco, risco residual, risco inerente, tolerancia ao risco
**Trigger words (EN):** risk matrix, risk assessment, likelihood, impact, heat map, risk register, mitigation, risk appetite, residual risk, inherent risk, risk tolerance, risk scoring, risk owner

## Step-by-Step Workflow

### Phase 1: Context & Scope
1. Define assessment scope (organization, project, process, or product)
2. Identify stakeholders and risk owners
3. Establish risk appetite and tolerance thresholds
4. Select scoring methodology (qualitative 5x5, semi-quantitative, quantitative)
5. Define risk categories (strategic, operational, financial, compliance, reputational, cyber)

### Phase 2: Risk Identification
1. Conduct workshops with stakeholders
2. Review historical incidents and near-misses
3. Analyze industry benchmarks and threat intelligence
4. Use PESTEL for external risks, value chain for internal
5. Document each risk with: ID, title, description, category, cause, consequence

### Phase 3: Risk Scoring
1. Score LIKELIHOOD (1-5):
   - 1 = Rare (<5% / once in 10+ years)
   - 2 = Unlikely (5-20% / once in 5-10 years)
   - 3 = Possible (20-50% / once in 1-5 years)
   - 4 = Likely (50-80% / once per year)
   - 5 = Almost certain (>80% / multiple times per year)
2. Score IMPACT (1-5):
   - 1 = Negligible (< EUR 10K, no disruption)
   - 2 = Minor (EUR 10-50K, minor disruption <1 day)
   - 3 = Moderate (EUR 50-250K, disruption 1-5 days)
   - 4 = Major (EUR 250K-1M, disruption 5-30 days)
   - 5 = Critical (> EUR 1M, existential threat)
3. Calculate inherent risk score = Likelihood x Impact
4. Apply existing controls assessment
5. Calculate residual risk score

### Phase 4: Heat Map
1. Plot risks on 5x5 matrix grid
2. Color zones: Green (1-4), Yellow (5-9), Orange (10-15), Red (16-25)
3. Identify risk clusters and concentration areas
4. Compare inherent vs residual heat maps

### Phase 5: Mitigation Planning
1. For each risk above tolerance: define treatment strategy
   - **Avoid**: eliminate the activity causing risk
   - **Reduce**: implement controls to lower likelihood/impact
   - **Transfer**: insurance, outsourcing, contracts
   - **Accept**: document rationale, monitor
2. Assign risk owner and action owner
3. Set deadlines and budget for mitigation actions
4. Define KRIs (Key Risk Indicators) for monitoring

### Phase 6: Risk Register Maintenance
1. Update register quarterly (or upon trigger events)
2. Track mitigation action completion
3. Re-score risks after control implementation
4. Report to management/board on risk profile changes
5. Annual full reassessment

## Commands Table

| Command | Description |
|---------|-------------|
| `risco matrix create` | Build new risk matrix from scratch |
| `risco matrix score` | Score a specific risk (likelihood x impact) |
| `risco matrix heatmap` | Generate heat map visualization |
| `risco matrix register` | Create/update risk register |
| `risco matrix mitigate` | Mitigation plan for specific risk |
| `risco matrix report` | Board-level risk summary report |
| `risco matrix kri` | Define KRIs for top risks |
| `risco matrix compare` | Compare inherent vs residual risk profiles |

## Output Template

```markdown
# Risk Assessment Report — [Scope]
**Date:** YYYY-MM-DD | **Assessor:** [Name] | **Review Period:** [Q/Year]

## 1. Heat Map (5x5)
|           | Negligible(1) | Minor(2) | Moderate(3) | Major(4) | Critical(5) |
|-----------|:---:|:---:|:---:|:---:|:---:|
| Almost Certain(5) | 5 | 10 | 15 | 20 | 25 |
| Likely(4)          | 4 | 8  | 12 | 16 | 20 |
| Possible(3)        | 3 | 6  | 9  | 12 | 15 |
| Unlikely(2)        | 2 | 4  | 6  | 8  | 10 |
| Rare(1)            | 1 | 2  | 3  | 4  | 5  |

## 2. Risk Register (Top Risks)
| ID | Risk | Category | L | I | Inherent | Controls | L | I | Residual | Owner | Treatment |
|----|------|----------|---|---|----------|----------|---|---|----------|-------|-----------|

## 3. Risk Profile Summary
- Total risks identified: X
- Critical (RED): X | High (ORANGE): X | Medium (YELLOW): X | Low (GREEN): X
- Risks above tolerance: X

## 4. Mitigation Actions
| Risk ID | Action | Owner | Deadline | Status | Budget |
|---------|--------|-------|----------|--------|--------|

## 5. KRIs
| KRI | Target | Current | Trend | Alert Threshold |
|-----|--------|---------|-------|-----------------|

## 6. Next Review: YYYY-MM-DD
```

## Red Flags

- Risk matrix not updated in >12 months
- No risk owner assigned to critical/high risks
- Mitigation actions overdue with no escalation
- All risks clustered in green zone (possible underestimation)
- No distinction between inherent and residual risk
- Risk appetite not defined or communicated
- No KRIs or early warning indicators in place
- Risk register exists only as static document (not actively managed)
- Board/management not receiving risk reports
- Same risks persisting quarter after quarter with no progress
- Impact scoring inconsistent across departments
- Emerging risks (cyber, climate, geopolitical) not considered


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **risco-matrix** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in risco-matrix:**

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

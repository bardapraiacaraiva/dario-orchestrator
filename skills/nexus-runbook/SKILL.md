---
name: nexus-runbook
description: "Runbooks — incident response procedures, escalation paths, post-mortem templates, known issues catalog"
version: "1.0"
---

# NEXUS-RUNBOOK: Operational Runbooks Skill

## When to Activate

**Trigger words (PT):** runbook, procedimento operacional, resposta a incidentes, escalacao, post-mortem, problemas conhecidos, procedimento de emergencia, on-call, troubleshooting
**Trigger words (EN):** runbook, operational procedure, incident response, escalation, post-mortem, known issues, emergency procedure, on-call, troubleshooting, playbook, blameless, root cause

## Step-by-Step Workflow

### Phase 1: Runbook Library Structure
1. Organize runbooks by category:
   - `incident/` — incident response playbooks
   - `operations/` — routine operational procedures
   - `maintenance/` — scheduled maintenance procedures
   - `known-issues/` — catalog of known issues and workarounds
   - `post-mortems/` — incident post-mortem reports
2. Naming convention: `CATEGORY-SERVICE-ACTION.md`
3. Version control: Git-managed, PR-reviewed changes
4. Searchable index with tags and symptoms
5. Ownership: each runbook has an author and reviewer

### Phase 2: Incident Response Runbooks
1. Standard structure per runbook:
   - **Symptoms**: what triggers this runbook (alerts, customer reports, monitoring)
   - **Impact**: what is affected and severity
   - **Diagnosis**: step-by-step triage commands
   - **Remediation**: fix steps with exact commands
   - **Verification**: how to confirm the issue is resolved
   - **Escalation**: when and to whom
   - **Follow-up**: post-incident tasks
2. Runbooks for common incidents:
   - Service down / health check failing
   - High latency / timeout errors
   - Database connection exhaustion
   - Disk space full
   - Certificate expired
   - Memory leak / OOM kill
   - DDoS attack
   - Data corruption
   - Deployment failure / rollback needed

### Phase 3: Escalation Matrix
1. Define escalation tiers:
   - **L1**: on-call engineer — initial triage, execute runbooks
   - **L2**: senior engineer / team lead — complex investigation
   - **L3**: architecture / principal — systemic issues, design changes
   - **Management**: when customer-facing, SLA-breaching, or extended duration
2. Escalation triggers: time-based (no resolution in X minutes), severity-based
3. Communication channels per tier: PagerDuty, phone, Slack, email
4. Contact directory: primary + backup for each role, updated monthly
5. External escalation: cloud provider support, vendor support

### Phase 4: Post-Mortem Process
1. Post-mortem required for: all P1, all P2 >30min, any data loss, any customer-facing
2. Timeline: draft within 48h, review within 1 week
3. Blameless culture: focus on systems, not individuals
4. Post-mortem structure:
   - Incident summary (1 paragraph)
   - Timeline (minute-by-minute from detection to resolution)
   - Root cause analysis (5 Whys technique)
   - Contributing factors
   - Impact assessment (users, revenue, SLA)
   - What went well
   - What went poorly
   - Action items (with owners and deadlines)
5. Post-mortem review meeting with involved teams
6. Track action item completion

### Phase 5: Known Issues Catalog
1. Document each known issue:
   - Symptoms and detection method
   - Affected systems and users
   - Root cause (if known)
   - Workaround (immediate mitigation)
   - Permanent fix status and timeline
   - Risk if workaround fails
2. Link known issues to monitoring alerts
3. Review and clean up resolved issues quarterly
4. Customer-facing known issues page (if applicable)

### Phase 6: Maintenance & Improvement
1. Runbook review: annually or after each use (whichever comes first)
2. Game Days: simulate incidents to test runbooks
3. On-call handoff: include runbook updates in handoff notes
4. New service onboarding: runbook creation as part of production readiness
5. Runbook effectiveness metrics: time to resolve using runbook vs without
6. Automate common runbook steps where possible (self-healing)

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus runbook create` | Generate runbook from template |
| `nexus runbook incident` | Incident response playbook template |
| `nexus runbook escalation` | Escalation matrix template |
| `nexus runbook postmortem` | Post-mortem report template |
| `nexus runbook known` | Known issues catalog template |
| `nexus runbook review` | Runbook quality audit |
| `nexus runbook index` | Searchable runbook index generator |
| `nexus runbook gameday` | Game Day exercise planner |

## Output Template

```markdown
# Runbook: [SERVICE] — [ISSUE]
**Author:** [Name] | **Reviewed:** YYYY-MM-DD | **Last Used:** YYYY-MM-DD

## Symptoms
- Alert: `[alert name and condition]`
- Customer report: [description]
- Dashboard: [what to look for]

## Impact
- Severity: [P1/P2/P3/P4]
- Affected: [services, users, regions]

## Diagnosis
1. `[command to check service status]`
2. `[command to check logs]`
3. `[command to check dependencies]`
4. Expected output: [what normal vs abnormal looks like]

## Remediation
1. `[exact command to fix]`
2. `[second step if needed]`
3. Wait X minutes for propagation
4. Verify: [verification step]

## Verification
- [ ] Service healthy: `[health check command]`
- [ ] Alert resolved: [check monitoring]
- [ ] Customer impact cleared: [how to verify]

## Escalation
| Condition | Escalate To | Contact |
|-----------|------------|---------|
| No resolution in X min | L2 | [name/channel] |
| Customer-facing | Management | [name/channel] |
| Data loss suspected | Security + L3 | [name/channel] |

## Follow-Up
- [ ] Post-mortem if P1/P2
- [ ] Update monitoring if gap found
- [ ] Update this runbook if steps changed
```

## Red Flags

- No runbooks for critical services
- Runbooks outdated (reference deprecated tools or procedures)
- No post-mortem process after major incidents
- Escalation contacts outdated or single point of contact
- On-call rotation without runbook access
- Known issues undocumented (tribal knowledge only)
- Post-mortem action items never completed
- Game Days never conducted
- Runbooks written but never tested
- Blameful post-mortem culture (people hide incidents)
- No runbook creation required for new service launch
- Automated alerts without corresponding runbook reference


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nexus-runbook** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nexus-runbook:**

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

---
name: aegis-soc-operations
description: SOC operations — MITRE ATT&CK, detection engineering, alert triage, MTTR optimization. Triggers em "SOC", "Security Operations Center", "MITRE ATT&CK", "detection engineering", "SOAR", "alert triage".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_immutable]
---

# AEGIS-SOC-OPERATIONS

## Quando usar
- SOC greenfield setup
- Detection engineering program
- Alert fatigue mitigation
- MTTR/MTTD improvement
- Tier 1/2/3 SOC structure

## Frameworks
- **MITRE ATT&CK** — adversary tactics + techniques (matrix)
- **MITRE D3FEND** — defensive countermeasures
- **Lockheed Cyber Kill Chain** — 7 stages
- **Pyramid of Pain (Bianco):** hash → IP → domain → tools → TTP
- **Diamond Model:** adversary / capability / infrastructure / victim

## SOC tiers
- **Tier 1:** triagem inicial, escalation (90% volume, 10% complexity)
- **Tier 2:** investigation + containment
- **Tier 3:** advanced threat hunting + IR
- **SOC Manager:** runbook + metrics

## Templates
1. Detection use case library (ATT&CK-mapped)
2. Detection engineering SDLC (idea → develop → test → deploy → tune)
3. Alert triage SOP (SOAR-ready)
4. SOC metrics dashboard (MTTD/MTTR/FP rate)
5. Threat hunting hypotheses + IOAs (Indicators of Attack)

## Métricas
- **MTTD:** Mean Time To Detect
- **MTTR:** Mean Time To Respond
- **False Positive rate:** <5% target
- **Coverage:** % ATT&CK techniques detected
- **Dwell time:** attacker presence before detection

## Cross-references
- [[aegis-siem-integration]] · [[aegis-edr-management]] · [[aegis-incident-response]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-soc-operations** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-soc-operations:**

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

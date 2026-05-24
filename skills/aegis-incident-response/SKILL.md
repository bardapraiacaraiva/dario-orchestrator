---
name: aegis-incident-response
description: Incident Response — NIST SP 800-61, playbooks, tabletop exercises, communication. Triggers em "incident response", "IR", "NIST 800-61", "playbook", "tabletop", "breach response", "ransomware response".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_immutable, lgpd_security_marker]
---

# AEGIS-INCIDENT-RESPONSE

## Marco
- **NIST SP 800-61 Rev 2** — Computer Security IR Handbook
- **ISO 27035** — IR management
- **SANS PICERL** — Prep/Identify/Contain/Eradicate/Recover/Lessons
- **MITRE Threat-Informed Defense**

## Quando usar
- IR plan from scratch
- Active incident in progress
- Tabletop exercises
- Post-incident review
- Ransomware response
- Data breach (LGPD/GDPR communication ≤72h)

## NIST IR lifecycle
1. **Preparation:** team + tools + comms + retainer
2. **Detection & Analysis:** triagem + scope
3. **Containment & Eradication:** stop bleeding
4. **Recovery:** restore + verify clean
5. **Post-Incident:** lessons learned + improve

## Templates
1. IR plan + playbooks (ransomware, BEC, data breach, account compromise)
2. Tabletop exercise scenarios
3. Breach communication template (LGPD ANPD 72h)
4. Chain of custody form
5. Post-mortem template
6. IR retainer SOW (external firm)

## Comms
- **Internal:** IR team Slack channel + war room
- **Executive:** updates 2-4h cadence durante incident
- **Legal:** counsel envolvido cedo
- **Regulators:** ANPD (LGPD), SEC (US), DPA (GDPR)
- **Customers:** factual + timeline + mitigation

## Cross-references
- [[aegis-digital-forensics]] · [[aegis-soc-operations]] · [[risco-bcp]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-incident-response** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-incident-response:**

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

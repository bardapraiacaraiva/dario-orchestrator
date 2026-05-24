---
name: aegis-siem-integration
description: SIEM — Splunk, ELK, Sentinel, QRadar, Wazuh. Log aggregation, correlation, detection rules. Triggers em "SIEM", "Splunk", "ELK", "Microsoft Sentinel", "QRadar", "Wazuh", "log aggregation", "correlation rules".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_immutable]
---

# AEGIS-SIEM-INTEGRATION

## Quando usar
- SIEM selection (greenfield ou migration)
- Log source onboarding
- Detection rule writing (Sigma)
- SIEM cost optimization (ingestion)
- Migration: legacy → cloud-native

## Stack
- **Splunk Enterprise / Cloud** — líder histórico
- **Microsoft Sentinel** — cloud-native, líder Azure
- **Elastic SIEM (ELK)** — open-source enterprise
- **IBM QRadar** — enterprise legado
- **Wazuh** — open-source SIEM + XDR
- **Datadog Cloud SIEM** — observability + security
- **Devo / Exabeam / Securonix** — alternatives

## Log sources prioritárias
- **Identity:** AD/Entra ID, Okta auth logs
- **Endpoint:** EDR, Sysmon, audit logs
- **Network:** Firewall, proxy, DNS, NetFlow
- **Cloud:** AWS CloudTrail, GCP Audit Logs, Azure Activity
- **Apps:** Web server, app logs, database audit

## Templates
1. SIEM architecture (collectors → ingestion → storage → analytics)
2. Sigma detection rule library
3. Log source onboarding checklist
4. Cost optimization playbook (filter at source, retention tiering)
5. Detection rule lifecycle (idea → tune → production → retire)

## Detection rules (Sigma)
- Vendor-agnostic format
- Translates to Splunk SPL, KQL (Sentinel), ES Query DSL
- Public rule library: SigmaHQ/sigma

## Cross-references
- [[aegis-soc-operations]] · [[aegis-edr-management]] · [[aegis-cloud-security]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-siem-integration** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-siem-integration:**

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

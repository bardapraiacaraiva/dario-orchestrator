---
name: aegis-edr-management
description: EDR/XDR — CrowdStrike Falcon, SentinelOne, Microsoft Defender, Cortex XDR. Triggers em "EDR", "XDR", "CrowdStrike", "SentinelOne", "Defender for Endpoint", "Cortex XDR", "endpoint detection".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit]
---

# AEGIS-EDR-MANAGEMENT

## Quando usar
- EDR selection (greenfield)
- Migration legacy AV → modern EDR
- Detection tuning (false positives)
- Threat hunting via EDR data
- Containment workflows

## Stack
- **CrowdStrike Falcon** — líder Gartner
- **SentinelOne Singularity** — autonomous AI
- **Microsoft Defender for Endpoint** — bundled Microsoft
- **Palo Alto Cortex XDR** — XDR completo
- **SophosLabs Intercept X**
- **Trend Micro Vision One**
- **Bitdefender GravityZone**
- **Open-source:** Wazuh, Velociraptor

## Templates
1. EDR selection scorecard (detection + cost + management + integration)
2. Onboarding playbook (deploy + tune + train)
3. Detection tuning workflow (FP analysis + suppression)
4. EDR-based threat hunting queries
5. Containment playbook (isolate, kill process, evict)

## Princípios
- **Don't block silently:** alert humano antes de block
- **Allowlist obrigatória:** dev tools, scripts internos
- **Tune progressively:** 30/60/90d ramp-up
- **Network containment:** EDR pode isolar host
- **Integrar com SIEM:** raw events para correlação

## Cross-references
- [[aegis-soc-operations]] · [[aegis-incident-response]] · [[aegis-cloud-security]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-edr-management** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-edr-management:**

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

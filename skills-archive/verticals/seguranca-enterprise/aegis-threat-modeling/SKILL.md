---
name: aegis-threat-modeling
description: Threat modeling — STRIDE, PASTA, LINDDUN, attack trees, OWASP Threat Dragon. Triggers em "threat modeling", "STRIDE", "PASTA", "LINDDUN", "attack tree", "modelagem de ameaças".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [audit_immutable]
---

# AEGIS-THREAT-MODELING

## Quando usar
- New system design (greenfield)
- Major architecture change
- Pre-pentest (focar test scope)
- Compliance requirement (ISO 27001 A.14)
- Post-incident retrospective

## Frameworks
- **STRIDE (Microsoft):** Spoofing/Tampering/Repudiation/Info Disclosure/DoS/Elevation
- **PASTA:** 7 stages, risk-centric
- **LINDDUN:** privacy-focused (Linkability/Identifiability/Non-repudiation/Detectability/Unawareness/Non-compliance)
- **Attack trees (Schneier):** hierarchical attacks
- **OCTAVE:** asset-centric
- **VAST:** scalable for agile

## Templates
1. STRIDE analysis per component (data flow diagram + threats)
2. Attack tree template
3. LINDDUN privacy threat model
4. Threat library (kb of common threats)
5. Mitigation tracking (threat → control → status)

## Stack
- **OWASP Threat Dragon** (open-source)
- **Microsoft Threat Modeling Tool**
- **IriusRisk** (enterprise)
- **ThreatModeler**
- **PyTM** (code-as-threat-model)

## Cross-references
- [[aegis-secure-sdlc]] · [[aegis-pentest-methodology]] · [[aegis-soc-operations]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-threat-modeling** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-threat-modeling:**

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

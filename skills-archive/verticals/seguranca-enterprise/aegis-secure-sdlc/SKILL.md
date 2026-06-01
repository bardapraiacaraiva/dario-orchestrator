---
name: aegis-secure-sdlc
description: Secure SDLC — SAST, DAST, SCA, IAST, threat modeling, secure coding. Triggers em "Secure SDLC", "SAST", "DAST", "SCA", "Snyk", "Checkmarx", "Veracode", "shift left security".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, secure_coding]
---

# AEGIS-SECURE-SDLC

## Filosofia
**Shift left + shield right.** Security em todas fases SDLC, não só pre-prod.

## Frameworks
- **OWASP SAMM:** Software Assurance Maturity Model
- **BSIMM:** Building Security In Maturity Model
- **NIST SSDF (SP 800-218)** — Secure Software Dev Framework
- **Microsoft SDL** — classic reference

## SAST / DAST / SCA / IAST
- **SAST:** Static analysis (Checkmarx, Veracode, Snyk Code, Semgrep)
- **DAST:** Dynamic, runtime (OWASP ZAP, Burp Suite, Acunetix)
- **SCA:** Software Composition (Snyk Open Source, Mend, Dependabot)
- **IAST:** Interactive (Contrast Security, Synopsys Seeker)
- **Container scan:** Trivy, Grype, Snyk Container

## Templates
1. Secure SDLC policy + RACI
2. Threat modeling per major feature (lightweight)
3. CI security gates (lint + SAST + SCA + secret scan + IaC scan)
4. Pre-prod DAST automation
5. Security champions program (1 per team)
6. Vuln remediation SLA matrix

## Pipeline (gates típicos)
```
PR open → secret scan + SAST → tests
Merge → SCA + container scan
Pre-deploy → DAST + IaC scan
Post-deploy → DAST scheduled + runtime
```

## Cross-references
- [[aegis-threat-modeling]] · [[aegis-vulnerability-management]] · [[builder-ci-cd]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-secure-sdlc** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-secure-sdlc:**

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

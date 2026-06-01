---
name: sphinx-osint-investigations
description: Open-source intelligence — Maltego, Shodan, social, image, blockchain. Triggers em "OSINT", "open source intelligence", "Maltego", "Shodan", "social media intel", "Trace Labs", "Bellingcat".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable, responsible_disclosure]
---

# SPHINX-OSINT-INVESTIGATIONS

## Categorias
- **HUMINT (Human):** people, organizations
- **SOCMINT (Social Media):** Twitter/X, LinkedIn, Instagram, Telegram
- **GEOINT (Geospatial):** satellite, street view, exif
- **IMINT (Image):** reverse image, manipulation detection
- **TECHINT (Technical):** infrastructure, ASN, DNS
- **FININT (Financial):** corporate records, beneficial owners
- **CYBINT (Cyber):** malware infrastructure, breach data

## Stack
- **Maltego** — transform-based investigations
- **Shodan + Censys** — internet exposure
- **theHarvester** — email/subdomain enumeration
- **SpiderFoot** — automated OSINT
- **OSINT Framework** (osintframework.com) — links library
- **Bellingcat Online Investigation Toolkit**
- **Trace Labs CTF** — community methodology
- **Blockchain:** Chainalysis, Elliptic, OXT.me

## Use cases
- Threat actor attribution
- M&A due diligence
- Insider threat investigation
- Brand protection (impersonation)
- Counter-disinformation
- Missing persons (Trace Labs)

## Templates
1. OSINT investigation methodology
2. Maltego graph (case template)
3. Person investigation playbook
4. Company investigation playbook
5. Infrastructure pivot patterns
6. Chain of custody OSINT evidence

## Cross-references
- [[sphinx-threat-intel-platforms]] · [[sphinx-dark-web-monitoring]] · [[aegis-pentest-methodology]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-osint-investigations** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-osint-investigations:**

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

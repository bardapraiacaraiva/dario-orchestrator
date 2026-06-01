---
name: sphinx-dark-web-monitoring
description: Dark web intel — credential leaks, brand monitoring, threat actor chatter. Triggers em "dark web monitoring", "credential leak", "Tor", "ransomware blog", "HaveIBeenPwned", "DarkOwl", "Intel 471".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable, classified_handling, responsible_disclosure]
---

# SPHINX-DARK-WEB-MONITORING

## Sources
- **Tor hidden services (.onion):** marketplaces, forums
- **I2P:** alternative anonymous network
- **Telegram channels:** ransomware, hacking
- **Discord:** gaming + hacking subcultures
- **Paste sites:** Pastebin, Hastebin (clearnet)
- **Ransomware leak blogs:** double extortion sites
- **Initial Access Brokers (IAB)** markets

## Stack
- **DarkOwl** — dark web search platform
- **Intel 471** — premium threat intel
- **Recorded Future Hidden** — dark web data
- **Cybersixgill** — threat actor profiles
- **Flashpoint** — extremism + cyber
- **HaveIBeenPwned** (free): credential breach
- **ZeroFox** — brand protection

## Use cases
- Credential leak detection (employees, customers)
- IP/data leak monitoring
- Brand impersonation
- Executive threat monitoring
- M&A target dark web profile
- Insider threat (employees selling access)

## Templates
1. Dark web monitoring requirements
2. Keyword + selector library
3. Alert triage workflow
4. Credential rotation playbook
5. Executive threat dashboard
6. Takedown coordination (TAKEDOWN.com)

## Cross-references
- [[sphinx-osint-investigations]] · [[sphinx-threat-intel-platforms]] · [[aegis-security-awareness]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-dark-web-monitoring** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-dark-web-monitoring:**

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

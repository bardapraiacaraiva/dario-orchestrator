---
name: sphinx-zero-day-management
description: 0day disclosure, exploit dev for defense, bounty programs, CVE coordination. Triggers em "zero day", "0day", "CVE", "responsible disclosure", "exploit development", "bug bounty", "ZDI", "HackerOne".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [responsible_disclosure, classified_handling, audit_immutable]
---

# SPHINX-ZERO-DAY-MANAGEMENT

## Disclosure models
- **Full disclosure:** public immediately (controversial)
- **Coordinated (CVD):** vendor → patch → public (standard)
- **Responsible:** give vendor 90 days
- **No disclosure:** government / IC reservation

## Bug bounty programs
- **HackerOne** — largest platform
- **Bugcrowd** — alternative
- **Intigriti** — EU-focused
- **YesWeHack** — France
- **Vendor self-managed:** Google, Microsoft, Apple

## Marketplaces (controversial)
- **ZDI (Zerodium):** acquires 0days for offensive
- **Crowdfense** — similar
- **Government exclusive** — US, Israel, etc.

## Exploit development
- **Memory corruption:** buffer overflow, UAF, type confusion
- **Web:** SQLi, XSS, deserialization, SSRF
- **Logic flaws:** authn/authz bypass
- **Crypto:** padding oracle, timing attacks
- **Hardware:** Spectre/Meltdown variants

## Templates
1. CVD process (timeline, escalation)
2. Bug bounty program design
3. CVE submission template
4. Patch verification framework
5. Exploit weaponization (for defense)
6. Internal 0day handling policy

## Cross-references
- [[sphinx-reverse-engineering]] · [[aegis-vulnerability-management]] · [[aegis-pentest-methodology]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-zero-day-management** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-zero-day-management:**

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

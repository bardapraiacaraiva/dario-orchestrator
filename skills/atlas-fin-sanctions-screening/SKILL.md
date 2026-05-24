---
name: atlas-fin-sanctions-screening
description: Sanctions screening — OFAC, EU, UN, BR (COAF), real-time + batch. Triggers em "sanctions screening", "OFAC", "EU sanctions", "UN sanctions", "BR COAF", "watchlist screening", "Refinitiv World-Check".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [sanctions_realtime, audit_immutable]
---

# ATLAS-FIN-SANCTIONS-SCREENING

## Listas sanções principais
- **OFAC SDN (US)** — Specially Designated Nationals
- **EU Consolidated List**
- **UN Security Council Sanctions**
- **UK HMT Sanctions List**
- **BR COAF / Bacen** — listas internas
- **PT BdP** — sanctions PT-specific
- **HMT (UK)** — Treasury sanctions list

## Stack
- **Refinitiv World-Check** — líder
- **Dow Jones Risk & Compliance** — premium
- **LexisNexis Bridger** — enterprise
- **ComplyAdvantage** — modern API-first
- **Sanctions.io** — developer-friendly
- **Acuris (now Moody's)** — Risk integrated

## Screening modes
- **Real-time:** transaction-time check (mandatory)
- **Daily batch:** customer base re-screen (lists update)
- **Onboarding:** KYC moment
- **Periodic refresh:** annual high-risk customers

## Match handling
- **True positive:** confirmed match → block + escalate
- **False positive:** similar name, different person → whitelist
- **Partial match:** require manual review
- **Fuzzy match:** transliteration (Mohammed = Muhammad)

## Templates
1. Sanctions screening architecture (real-time API)
2. List update automation (Refinitiv feed)
3. False positive review workflow
4. PEP screening (separate from sanctions)
5. Annual screening audit report
6. Sanctions program governance

## Cross-references
- [[atlas-fin-aml-monitoring]] · [[atlas-fin-kyc-onboarding]] · [[aegis-third-party-risk]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-sanctions-screening** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-sanctions-screening:**

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

---
name: euterpe-programmatic
description: Programmatic advertising — DSPs, RTB, retargeting, supply path optimization. Triggers em "programmatic", "DSP", "RTB", "real time bidding", "retargeting", "DV360", "The Trade Desk", "Amazon DSP", "Criteo".
license: MIT
parent_agent: euterpe-director
compliance: [lgpd_marketing, gdpr_marketing]
---

# EUTERPE-PROGRAMMATIC

## Ecosystem
- **Advertisers** → **DSP** → **AdExchange (SSP)** → **Publishers**
- **DMP:** Data Management Platform (audience data)
- **CDP:** Customer Data Platform (1st party data)

## DSPs líderes
- **The Trade Desk (TTD)** — independent líder
- **DV360 (Google Display & Video 360)** — bundled Google
- **Amazon DSP** — strong retail intent
- **Adobe Advertising Cloud**
- **Xandr (Microsoft)** — TV + display
- **MediaMath** — independent

## Cookie deprecation 2025+
- **Chrome:** Topics API + FLEDGE (Protected Audience)
- **Safari:** ITP (Intelligent Tracking Prevention) — already strict
- **Firefox:** ETP
- **Alternatives:** UID 2.0 (TTD), ID5, RampID (LiveRamp)
- **Contextual targeting:** revival (no cookies needed)
- **CTV (Connected TV):** cookie-free environment

## SPO (Supply Path Optimization)
- Direct deals > open exchange
- Avoid reseller chains (transparency)
- ads.txt + sellers.json verification
- Header bidding (publisher-side)

## Templates
1. DSP selection scorecard
2. Programmatic strategy by funnel stage
3. Frequency cap optimization
4. SPO audit framework
5. Cookieless preparation roadmap
6. CTV programmatic playbook

## Cross-references
- [[euterpe-paid-search]] · [[euterpe-paid-social]] · [[euterpe-attribution-multi-touch]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-programmatic** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-programmatic:**

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

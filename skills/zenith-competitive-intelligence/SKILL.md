---
name: zenith-competitive-intelligence
description: Competitive intelligence — market intel, war room, OSINT, competitor profiling. Triggers em "competitive intelligence", "CI", "market intel", "OSINT", "competitor profile", "battle card".
license: SEE-LICENSE
parent_agent: zenith-director
compliance: [legal_osint_only, no_industrial_espionage]
---

# ZENITH-COMPETITIVE-INTELLIGENCE

## Quando usar
- New product launch (competitor reaction)
- Pricing decision (competitor matching)
- M&A target tracking
- Sales enablement (battle cards)
- Strategic planning (market context)

## Sources legítimas
- **OSINT:** SEC filings, press releases, job posts, patents, LinkedIn
- **Customer interviews:** "who else are you considering?"
- **Win/loss analysis:** sales pipeline data
- **Reverse engineering:** product teardowns
- **Conferences + analyst reports:** Gartner/Forrester
- **Web scraping:** pricing pages, product changelogs
- **Trial accounts:** legitimate (ToS-compliant)

## Anti-patterns (illegal/unethical)
- ❌ Industrial espionage (employees, leaks)
- ❌ Misrepresentation (pose as customer when not)
- ❌ Hacking / unauthorized access
- ❌ Bribery / paying for confidential info

## Templates
1. Competitor profile (1-pager per competitor)
2. Battle card (for sales: "vs X")
3. Market intel digest (weekly/monthly)
4. Win/loss interview script
5. War room setup (Slack channel + Notion + alerts)
6. Patent landscape analysis

## Cross-references
- [[zenith-war-gaming]] · [[zenith-strategic-planning]] · [[a360-nicho]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-competitive-intelligence** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-competitive-intelligence:**

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

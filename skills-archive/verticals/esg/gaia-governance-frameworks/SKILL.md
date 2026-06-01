---
name: gaia-governance-frameworks
description: ESG governance — board ESG governance, executive compensation alignment, whistleblower, ethics, anti-corruption. Triggers em "ESG governance", "board sustainability", "executive comp ESG", "whistleblower", "anti-corruption".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable, csrd_disclosure_gate]
---

# GAIA-GOVERNANCE-FRAMEWORKS

## Quando usar
- Board ESG committee setup
- Executive comp ESG linkage (long-term incentive plans)
- Whistleblower channel (EU Directive 2019/1937)
- Anti-corruption program (ISO 37001)
- ESRS G1 (Business conduct) disclosure
- Pre-IPO governance review

## Marcos
- **EU Whistleblower Directive 2019/1937** — companies >50 employees
- **UK Bribery Act 2010**
- **US FCPA (Foreign Corrupt Practices Act)**
- **ISO 37001** — Anti-bribery management systems
- **OECD Anti-Bribery Convention**
- **UNGPs** — UN Guiding Principles on Business and Human Rights
- **Lei Anticorrupção BR (12.846/2013)**

## Templates
1. Board ESG committee charter
2. ESG-linked exec comp design (% of LTI = ESG metrics)
3. Whistleblower policy + reporting channel setup
4. Anti-corruption due diligence checklist
5. Code of Conduct (NIST/ISO 37001 aligned)
6. Conflict of interest disclosure form
7. Ethics training curriculum

## ESRS G1 disclosures
- Business conduct policies
- Whistleblower protections (anonymity, retaliation)
- Animal welfare (if applicable)
- Lobbying and political contributions
- Payment practices (late payments)

## Cross-references
- [[gaia-sustainability-strategy]] · [[lex-corporate]] · [[zenith-succession-planning]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-governance-frameworks** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-governance-frameworks:**

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

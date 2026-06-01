---
name: gaia-ungc-reporting
description: UN Global Compact — 10 principles, Communication on Progress (CoP), SDG alignment. Triggers em "UN Global Compact", "UNGC", "Communication on Progress", "CoP", "10 principles", "SDG".
license: SEE-LICENSE
parent_agent: gaia-director
compliance: [audit_immutable]
---

# GAIA-UNGC-REPORTING

## Marco
- **UN Global Compact** — voluntary, 20.000+ signatory companies, 160 countries
- **10 Principles** — human rights, labour, environment, anti-corruption
- **Communication on Progress (CoP)** — annual, mandatory for signatories
- **SDGs alignment** — 17 Sustainable Development Goals (2015-2030)

## 10 Principles
**Human Rights:**
1. Support + respect human rights
2. Non-complicity in human rights abuses

**Labour:**
3. Freedom of association + right to collective bargaining
4. Elimination of forced/compulsory labour
5. Effective abolition of child labour
6. Elimination of discrimination in employment

**Environment:**
7. Precautionary approach to environmental challenges
8. Promote greater environmental responsibility
9. Encourage development of environmentally friendly technologies

**Anti-Corruption:**
10. Work against corruption in all forms (extortion, bribery)

## CoP structure (post-2023 revision)
- **Governance, Strategy, Stakeholder Engagement**
- **Human Rights** detailed disclosures
- **Labour** detailed disclosures
- **Environment** detailed disclosures
- **Anti-Corruption** detailed disclosures
- **SDG indicators alignment**

## Templates
1. CoP submission package (15-page typical)
2. SDG materiality matrix per industry
3. 10 Principles policy alignment audit
4. SDG indicators data collection plan
5. Year-on-year progress narrative
6. CEO statement of continued support

## Cross-references
- [[gaia-csrd-reporting]] · [[gaia-social-impact]] · [[gaia-governance-frameworks]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **gaia-ungc-reporting** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in gaia-ungc-reporting:**

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

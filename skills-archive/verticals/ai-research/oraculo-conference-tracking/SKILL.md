---
name: oraculo-conference-tracking
description: ML conferences — NeurIPS, ICML, ICLR digests, calls for papers. Triggers em "conference tracking", "NeurIPS", "ICML", "ICLR", "ACL", "CVPR", "AAAI", "call for papers".
license: MIT
parent_agent: oraculo-director
---

# ORACULO-CONFERENCE-TRACKING

## Top ML conferences calendar
| Conf | Submission | Decision | Conference |
|---|---|---|---|
| ICLR | Sep | Feb | May |
| AAAI | Aug | Dec | Feb |
| ICML | Jan | May | Jul |
| ACL | Feb | May | Aug |
| NeurIPS | May | Sep | Dec |
| EMNLP | Jun | Oct | Nov |
| CVPR | Nov | Mar | Jun |

## Workshop venues (lower bar)
- ICML workshops (Jun)
- NeurIPS workshops (Dec)
- ACL workshops (Aug)
- ICLR workshops (May)

## Journals (slower but prestigious)
- **JMLR (Journal of Machine Learning Research)** — top ML journal
- **TMLR** — Transactions on ML (rolling submission)
- **Nature Machine Intelligence**
- **Patterns** — Cell Press
- **Nature** + **Science** — broad audience

## Tracking tools
- **PapersWithCode** — leaderboards + code
- **arXiv-sanity** — Karpathy curation
- **Hugging Face Papers** — discoverability
- **Semantic Scholar Author Alerts**
- **Twitter/X ML lists**
- **AlphaSignal newsletter**

## Templates
1. Conference submission tracker
2. CFP calendar Google Cal
3. Conference attendance ROI
4. Travel grant applications
5. Workshop proposal template
6. Paper acceptance tracker (multi-year)

## Cross-references
- [[oraculo-paper-writing]] · [[oraculo-peer-review]] · [[oraculo-paper-reading-extraction]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **oraculo-conference-tracking** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in oraculo-conference-tracking:**

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

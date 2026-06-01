---
name: euterpe-content-distribution
description: Content distribution — multi-channel, syndication, repurposing, amplification. Triggers em "content distribution", "content syndication", "repurposing", "amplification", "content marketing".
license: MIT
parent_agent: euterpe-director
---

# EUTERPE-CONTENT-DISTRIBUTION

## Framework 1-9-90
- **1 piece:** pillar content (long-form blog, video, podcast)
- **9 pieces:** derivatives (clips, quotes, infographics)
- **90 distributions:** atomized across channels

## Channels distribution
- **Owned:** blog, newsletter, podcast (highest control)
- **Earned:** PR, media coverage, organic social
- **Paid:** ads, sponsorships, boosted social
- **Shared:** social, communities, partners

## Atomization patterns
- **Video → clips → Reels/Shorts/TikTok**
- **Podcast → transcript → blog → social quotes**
- **Webinar → recording + slides + emails + tweets**
- **Long blog → newsletter → LinkedIn post → Twitter thread**
- **Research → infographic → SlideShare → press release**

## Stack
- **Buffer, Hootsuite** — scheduling líderes
- **Sprout Social** — enterprise
- **Later** — visual platforms focus
- **Repurpose.io** — automation
- **Descript** — video/audio editing + repurposing
- **Opus Clip** — AI video clips

## Templates
1. Content calendar (3-month view)
2. Repurposing workflow (1 → 9 → 90)
3. Channel-specific format guide
4. Cross-promotion checklist
5. Content amplification budget allocation
6. UTM tracking per channel

## Cross-references
- [[dario-content]] · [[euterpe-paid-social]] · [[seo-content]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-content-distribution** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-content-distribution:**

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

---
name: ui-design
description: Use this to design a nice UI in single html as inspiration & UI exploration.
---

Only code in HTML/Tailwind in a single code block. 
Any CSS styles should be in the style attribute. 
Start with a response, then code and finish with a response. 
Don't mention about tokens, Tailwind or HTML. 
Always include the html, head and body tags. 
Use lucide icons for javascript, 1.5 strokewidth. 
Unless style is specified by user, design in the style of Linear, Stripe, Vercel, Tailwind UI (IMPORTANT: don't mention names). 
Checkboxes, sliders, dropdowns, toggles should be custom (don't add, only include if part of the UI). 
Be extremely accurate with fonts. For font weight, use one level thinner: for example, Bold should be Semibold. 
Titles above 20px should use tracking-tight. 
Make it responsive. Avoid setting tailwind config or css classes, use tailwind directly in html tags. 
If there are charts, use chart.js for charts (avoid bug: if your canvas is on the same level as other nodes: h2 p canvas div = infinite grows. h2 p div>canvas div = as intended.). 
Add subtle dividers and outlines where appropriate. 
Don't put tailwind classes in the html tag, put them in the body tags. 
If no images are specified, use these Unsplash images like faces, 3d, render, etc. 
Be creative with fonts, layouts, be extremely detailed and make it functional. If design, code or html is provided, IMPORTANT: respect the original design, fonts, colors, style as much as possible. 
Don't use javascript for animations, use tailwind instead. Add hover color and outline interactions. 
For tech, cool, futuristic, favor dark mode unless specified otherwise. 
For modern, traditional, professional, business, favor light mode unless specified otherwise. Use 1.5 strokewidth for lucide icons and avoid gradient containers for icons. 
Use subtle contrast. For logos, use letters only with tight tracking. 
Avoid a bottom right floating DOWNLOAD button.

<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **ui-design** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in ui-design:**

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

---
name: scroll-animations
description: Use when triggering animations on scroll - reveal effects, parallax, sticky headers, progress indicators, or any scroll-linked motion.
---

# Scroll Animations

Apply Disney's 12 principles to scroll-triggered motion.

## Principle Application

**Squash & Stretch**: Elements can compress slightly while scrolling fast, settle when stopped.

**Anticipation**: Content should be slightly visible before full reveal. Start animations at 10-20% visibility.

**Staging**: Reveal content in reading order. Top-to-bottom, left-to-right progression.

**Straight Ahead vs Pose-to-Pose**: Define clear "hidden" and "revealed" poses. Scroll position interpolates between them.

**Follow Through & Overlapping**: Stagger reveals. First element triggers at 20% viewport, next at 25%, etc.

**Slow In/Slow Out**: Use ease-out for reveals triggered by scroll. Content settles into place.

**Arcs**: Parallax elements move on curves relative to scroll. Slight horizontal offset as vertical scroll occurs.

**Secondary Action**: Fade + slide + scale can combine for richer reveals.

**Timing**:
- Reveal animation: 400-600ms (allows scroll to continue)
- Parallax: real-time, 1:1 or fractional ratios
- Sticky transitions: 200-300ms

**Exaggeration**: Subtle for scroll - users control the pace. Let scroll speed be the exaggeration.

**Solid Drawing**: Elements should never jump or teleport. Smooth interpolation at all scroll positions.

**Appeal**: Scroll animations should reward exploration, not obstruct it.

## Timing Recommendations

| Scroll Animation | Duration | Trigger Point | Easing |
|-----------------|----------|---------------|--------|
| Fade In | 500ms | 20% visible | ease-out |
| Slide Up | 600ms | 15% visible | ease-out |
| Parallax | real-time | continuous | linear |
| Sticky Header | 200ms | threshold | ease-out |
| Progress Bar | real-time | continuous | linear |
| Section Reveal | 600ms | 25% visible | ease-out |

## Implementation Patterns

```css
/* Scroll-triggered reveal */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 500ms ease-out, transform 600ms ease-out;
}

.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* CSS-only parallax */
.parallax-container {
  perspective: 1px;
  overflow-y: auto;
}

.parallax-slow {
  transform: translateZ(-1px) scale(2);
}
```

## Intersection Observer Pattern

```javascript
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  },
  { threshold: 0.2, rootMargin: '0px 0px -10% 0px' }
);

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

## Scroll-Linked Animation (CSS)

```css
@keyframes reveal {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.scroll-reveal {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 50%;
}
```

## Key Rules

1. Never block scroll or hijack scroll behavior
2. Animations should complete within viewport, not require precise scroll position
3. Trigger early (10-20% visible) so animation completes before full view
4. Provide `prefers-reduced-motion` alternative - instant reveals, no parallax
5. Test on mobile - scroll animations must be smooth at 60fps


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **scroll-animations** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in scroll-animations:**

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

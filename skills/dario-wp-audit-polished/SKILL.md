---
name: dario-wp-audit-polished
description: "Self-polishing WordPress + WooCommerce audit — autonomous variant of dario-wp-audit. Internally runs generate → critique → revise → final within one Claude Code session. Use when audit must ship as client deliverable without human polish. Triggers: 'wp audit polished', 'wordpress autónomo', 'audit ready-to-ship'."
argument-hint: "[site URL + stack + business context + audit scope]"
allowed-tools: Read, Write, Glob, Grep, WebFetch
license: MIT
---

# DARIO Skill — WordPress / WooCommerce Audit (Self-Polishing)

Padrão A wrapper around `dario-wp-audit`. Base autonomous ceiling ~85. Production polished hits ~91 (recently promoted tier A). Wrapper formalizes the polish step. **Zero marginal API cost under Claude Max.**

## When to use this vs `dario-wp-audit`

| Situation | Use |
|---|---|
| Quick internal site check | `dario-wp-audit` |
| Audit delivered as client PDF/Notion page | **`dario-wp-audit-polished`** |
| Audit triggering invoice (paid deliverable) | **`dario-wp-audit-polished`** |
| Audit driving security/perf remediation roadmap | **`dario-wp-audit-polished`** |

---

## Workflow (5 steps, MUST execute all in order)

### Step 1 — GENERATE v1

Execute full `dario-wp-audit` workflow:
- WebFetch + analysis: performance, security, SEO, content, plugin bloat, theme health, checkout flow (if Woo), accessibility, PT legal compliance
- Categorize findings: CRITICO / IMPORTANTE / OTIMIZAÇÃO
- Prioritization roadmap by impact × effort

Mark: `### DRAFT v1 (internal — not delivered)`.

### Step 2 — SELF-CRITIQUE (5-dim, 0-100)

Audits are gamed by generic findings ("update plugins"). Score for specificity to THIS site.

```
1. Specificity (0-20) — Findings reference actual plugins/themes/URLs from this site?
   (Not "outdated plugins" — name plugin + version + risk)
2. Actionability (0-20) — Each finding has concrete fix step + estimated effort?
   (Not "improve performance" — "enable WP Rocket cache, est. 4h")
3. Completeness (0-20) — All 8 audit dimensions covered?
   (perf / security / SEO / content / plugins / theme / checkout / a11y / PT legal)
4. Accuracy (0-20) — Severity ratings defensible? Fix recommendations technically correct?
   (E.g., "uses outdated jQuery" but site uses native JS = 8/20)
5. Tone (0-20) — Client-facing register (not "your site is bad" — "we identified X opportunities")?
```

Document with reasoning per dim + Total + Weakest dim(s) + Specific issues for v2.

### Step 3 — DECISION GATE

- **TOTAL ≥ 92:** output v1
- **TOTAL ≥ 80 AND no dim < 14:** revise
- **TOTAL < 80 OR any dim < 14:** STOP, request fuller WebFetch / specific URLs / plugin list

### Step 4 — REVISE → v2

Targeted fixes:
- Specificity weak: re-WebFetch + name plugins/themes/URLs concretely
- Actionability weak: add fix steps + effort + cost estimate per finding
- Completeness weak: add missing audit dimension (most common: a11y or PT legal)
- Accuracy weak: re-verify findings (cross-check with WebFetch evidence)
- Tone weak: re-write client-facing voice

Output v2.

### Step 5 — RE-SCORE + OUTPUT FINAL

Re-run critique. Output best with metadata + executive summary.

---

## A/B Test Protocol

**Baseline:** dario-wp-audit production_avg = 91 (recently tier A promoted, per polish_target_50_2026_05_24.md).
**Threshold:** ≥+2pts lift on 3 real briefings (lower threshold because skill already polished).
**Test briefings:** Vivenda Creative Home audit / Lisbon Dog Care audit / Cuidaí production audit.

---

## Red flags

- ❌ Generic findings without naming actual plugins → Specificity fail
- ❌ "Improve performance" without metric + target → Actionability fail
- ❌ Skip a11y or PT legal (DL 79/2024) → Completeness fail
- ❌ Severity inflation ("CRITICO" everywhere) → Accuracy + tone fail

---

<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every finding + recommendation must carry an EXPLICIT label.

- 🔵 **verified** — confirmed via WebFetch / Lighthouse / plugin list scan
- 🟡 **assumed** — likely true given evidence but needs admin panel access to confirm
- 🟢 **projection** — performance/SEO lift estimate post-fix

**Why:** audits mix verified findings (page loads slow at LCP 5.2s) with assumed issues (probably has bloated plugins) and projected fixes (will improve LCP to 2.5s after fix). Client + dev team needs to know which to act on first.

❌ NOT delivery-ready:
```
Site is slow. Has too many plugins. SEO needs work. Fix expected: 3 weeks.
```

✅ Delivery-ready:
```
CRITICO performance:
- LCP 5.2s mobile 🔵 verified (Lighthouse 2026-05-24, /produtos page)
- 38 plugins activos, 12 sem update >6 meses 🔵 verified (WP admin scan)
- Probable cause: Elementor + 4 page builders coexistindo 🟡 assumed (precisa admin access)

IMPORTANTE SEO:
- Sem schema markup Product/Organization 🔵 verified (View source check)
- Meta descriptions duplicadas em 8 páginas 🔵 verified (Screaming Frog crawl)

OTIMIZAÇÃO:
- Fix LCP → estimado 2.1s pós-WP Rocket + image conversion 🟢 projection
- Schema fix → estimated +12-18% rich results SERP 🟢 projection (Schema.org case studies)

Status mix: 4 🔵 · 1 🟡 · 2 🟢
Roadmap: 1 sprint CRITICO → 2 sprints IMPORTANTE → contínuo OTIMIZAÇÃO
```
<!-- gate7:end -->

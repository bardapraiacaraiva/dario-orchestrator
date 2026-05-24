---
name: nomos-anac-aviation-pt
description: ANAC PT — Autoridade Nacional Aviação Civil, drones (UAS), aviação comercial, aeroportos, ANACOM coordination. Triggers em "ANAC", "drone PT", "UAS", "EASA", "aviação PT", "aeroporto", "ANAC Portugal".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-ANAC-AVIATION-PT

## Marco
- **DL 218/2015** — ANAC atribuições
- **Regulamento (UE) 2018/1139** — EASA
- **Regulamento Execução (UE) 2019/947** — drones UAS
- **Regulamento Delegado (UE) 2019/945** — drones products
- **Regulamento ANAC 1093/2016** — drones PT pré-EASA (revogado parcial)
- **CAA (Civil Aviation Authority) PT** — operacional

## Quando usar
- Operação drone profissional (UAS-PT registo)
- Aviação comercial AOC (Air Operator Certificate)
- Filmagens aéreas com drone
- Aeroporto / heliporto licensing
- Manutenção CAMO certificate
- ATM/ANS provider (NAV Portugal)

## Drone categorias EASA (PT)
- **Open (A1/A2/A3):** sem autorização, peso + altitude limites
- **Specific:** SORA risk assessment, ANAC autorização
- **Certified:** equiparado aviação comercial (delivery, passengers)

## Templates
1. UAS registo PT (operador + drone)
2. SORA (Specific Operations Risk Assessment)
3. Plano voo VLOS / BVLOS
4. Insurance aviação obrigatório (Regulamento 785/2004)
5. Filmagens autorização IGAC + ANAC combined
6. AOC application checklist
7. Just Culture report (incidents)

## Cross-references
- [[nomos-igac-events-pt]] · [[atlas-photo-video]] · [[diva-render-brief]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-anac-aviation-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-anac-aviation-pt:**

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

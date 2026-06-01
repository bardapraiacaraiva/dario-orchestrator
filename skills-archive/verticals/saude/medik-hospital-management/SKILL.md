---
name: medik-hospital-management
description: Gestão hospitalar — NSP (Núcleo Seg Paciente), KPIs, acreditação ONA/Qmentum/JCI. Triggers em "gestão hospitalar", "NSP", "ONA", "Qmentum", "JCI", "acreditação hospitalar", "KPI hospital".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [anvisa_regulatory, cfm_resolutions, audit_trail]
jurisdiction: Brasil
---

# MEDIK-HOSPITAL-MANAGEMENT

## Quando usar
- Setup hospital greenfield ou pequeno porte
- Acreditação ONA (Nível 1/2/3) ou internacional (JCI, Qmentum)
- NSP (Núcleo de Segurança do Paciente) RDC 36/2013
- KPIs hospital + benchmarking
- Lean healthcare implementation

## Marco
- **RDC ANVISA 36/2013** — Núcleo Segurança Paciente
- **RDC ANVISA 63/2011** — BPF serviços de saúde
- **ONA (Org. Nacional Acreditação)** — Manual 2022
- **Qmentum (Accreditation Canada Intl)**
- **JCI (Joint Commission International)**

## KPIs hospitalares chave
- **Taxa de ocupação** (target: 75-85%)
- **Tempo médio de permanência** (TMP)
- **Mortalidade hospitalar** (ajustada por risco)
- **Taxa de cesárea** (Robson 10)
- **Infecção hospitalar** (CIH/CCIH)
- **Re-internação 30d** (qualidade)
- **NPS paciente + colaborador**
- **Custo paciente-dia**

## Templates
1. Acreditação ONA gap analysis
2. NSP setup + comitê + plano
3. Dashboard executivo hospital
4. Comissão de óbitos workflow
5. Lean DRG-based pathways

## Cross-references
- [[medik-clinical-protocols]] · [[medik-rcm-revenue-cycle]] · [[demeter-bi-dashboard]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-hospital-management** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-hospital-management:**

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

---
name: nomos-igac-events-pt
description: IGAC — Inspeção-Geral Atividades Culturais PT, direitos autor, SPA licensing, espetáculos. Triggers em "IGAC", "direitos autor PT", "SPA Portugal", "espetáculo PT", "licença IGAC", "Código Direito Autor".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [audit_immutable]
jurisdiction: Portugal
---

# NOMOS-IGAC-EVENTS-PT

## Marco
- **CDADC (Código Direito de Autor e Direitos Conexos)** — DL 63/85
- **Lei 26/2015** — gestão colectiva (SPA, GDA)
- **DL 23/2014** — espetáculos artísticos
- **DL 124/2013** — entidades de gestão colectiva
- **Lei 5/2010** — comunicação social

## Quando usar
- Licenciar espetáculo / evento música ao vivo
- Licenciar uso música ambiente (lojas, hotéis, restaurantes)
- Empresas streaming + direitos autor (Spotify-like)
- Filmagens espaços públicos
- Festivais — autorização IGAC + Câmara Municipal
- Cinema / produção audiovisual

## SPA / GDA / Audiogest
- **SPA (Sociedade Portuguesa de Autores):** composição (música)
- **GDA (Gestão Direitos Artistas):** interpretação/execução
- **Audiogest:** produtores fonogramas
- **Visapress:** imprensa
- **VOXMUS:** música ambiente

## Tarifas típicas (2026)
- Música ambiente loja pequena: € 200-500/ano
- Restaurante 50 lugares: € 800-1.500/ano
- Hotel 100 quartos: € 3.000-8.000/ano
- Concerto pago < 500 lugares: 5-10% bilheteira
- Festival > 5.000 lugares: 8-12% bilheteira + mínimos

## Templates
1. Licenciamento SPA + GDA + Audiogest combinado
2. Autorização IGAC espetáculo público
3. Contrato encomenda obra (cessão direitos)
4. Termo cedência uso imagem
5. Disclaimer copyright streaming
6. Notificação Câmara Municipal evento

## Cross-references
- [[atlas-entertainment]] · [[lex-ip]] · [[atlas-compliance]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nomos-igac-events-pt** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nomos-igac-events-pt:**

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

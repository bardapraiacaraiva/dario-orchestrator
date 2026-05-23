---
name: builder-mvp-scope
description: >
  Define o scope minimo viavel: o que entra no MVP, o que fica para depois. Cut ruthlessly.
  Prioritiza por impacto vs esforco. Timeline realista. Tech debt budget.
  Use quando: MVP, scope, o que construir primeiro, priorizar features, minimum viable.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — MVP Scope Definition

## Proposito
Cortar sem piedade. O MVP e o MINIMO que valida a hipotese, nao "a versao 1 com tudo".

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-mvp-scope [produto]` | Scope MVP completo |
| `/builder-mvp-scope cut [feature-list]` | Decidir o que cortar |
| `/builder-mvp-scope ice [features]` | ICE scoring (Impact, Confidence, Ease) |

## Framework: ICE Scoring

| Feature | Impact (1-10) | Confidence (1-10) | Ease (1-10) | ICE Score | Decision |
|---------|--------------|-------------------|-------------|-----------|----------|
| Auth | 10 | 10 | 8 | 800 | MVP |
| Dashboard | 8 | 9 | 7 | 504 | MVP |
| Team collab | 6 | 5 | 3 | 90 | V1.1 |
| AI feature | 9 | 4 | 2 | 72 | V1.2 |

**Rule:** ICE > 300 = MVP. ICE 100-300 = V1.1. ICE < 100 = Backlog.

## MVP Checklist
- [ ] Resolve the #1 pain point (only one!)
- [ ] Can a user complete the core job-to-be-done?
- [ ] Can be built in <= 4 weeks?
- [ ] Has a measurable success metric?
- [ ] Tech debt budget: max 20% of MVP time

## Output
1. Feature priority matrix (ICE scored)
2. MVP cut list (IN vs OUT)
3. V1.1 backlog (what was cut and why)
4. Timeline (realistic, with buffer)
5. Tech debt budget allocation

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — ICE scores calculados e defensáveis
- [ ] Cada feature tem os 3 valores (Impact, Confidence, Ease) explícitos, não adivinhados
- [ ] ICE Score = I × C × E (multiplicado, não somado)
- [ ] Threshold aplicado: ≥300 MVP, 100–299 V1.1, <100 backlog — sem excepções silenciosas
- [ ] Features com ICE borderline têm nota de justificação (ex: "90 mas entra no MVP porque é blocker técnico")
- ❌ NOT delivery-ready: "Feature X tem impacto alto, provavelmente MVP"
- ✅ Delivery-ready: "Onboarding flow — Impact 9, Confidence 8, Ease 7 → ICE 504 → MVP"

### Gate 2 — MVP resolve UM pain point, não vários
- [ ] Existe uma única hipótese central declarada ("Validamos que [user] consegue [job-to-be-done] sem [fricção X]")
- [ ] Features IN estão ligadas a esse pain point — features "nice to have" estão OUT
- [ ] A pergunta "pode ser removido e o MVP ainda valida a hipótese?" foi feita a cada feature incluída
- [ ] Não há scope creep disfarçado de "MVP básico"
- ❌ NOT delivery-ready: "O MVP inclui auth, dashboard, notificações, perfil e relatórios"
- ✅ Delivery-ready: "MVP da Cuidai valida: cuidador consegue aceitar turno e registar presença sem telefonema — auth + shift-accept + check-in. Só."

### Gate 3 — Cut list justificada (o que saiu e porquê)
- [ ] Existe secção explícita "OUT do MVP" com cada item e razão concreta
- [ ] Razões são técnicas ou de validação, não "falta tempo" genérico
- [ ] Cliente não fica surpreendido em V1.1 com features que assumia estarem no MVP
- [ ] Cada item OUT tem destino claro: V1.1, V1.2 ou backlog permanente
- ❌ NOT delivery-ready: "Team collaboration fica para depois"
- ✅ Delivery-ready: "Multi-utilizador (ICE 90) → V1.1 após validar que utilizador solo completa core flow; adiciona 3 semanas de dev sem validar hipótese principal"

### Gate 4 — Timeline realista com buffer explícito
- [ ] Timeline em semanas concretas, não "~1 mês"
- [ ] Buffer de 20–30% incluído e visível (não absorvido silenciosamente)
- [ ] Tech debt budget declarado: máx 20% do tempo total de MVP (em horas ou dias)
- [ ] Milestones intermédios definidos (não só "entrega final")
- ❌ NOT delivery-ready: "Estimativa: 3–4 semanas dependendo da complexidade"
- ✅ Delivery-ready: "SAQUEI MVP: 4 semanas base + 1 semana buffer = 5 semanas. Tech debt budget: 8h (20% de 40h dev). Milestone: end wk2 = core flow testável internamente"

### Gate 5 — Métrica de sucesso do MVP definida
- [ ] Existe exactamente uma métrica primária de validação (não "engagement geral")
- [ ] Métrica é mensurável antes de V1.1 arrancar
- [ ] Threshold de sucesso/falha declarado ("se X então avançamos, senão pivotamos")
- [ ] Método de medição identificado (analytics, entrevista, conversion rate, etc.)
- ❌ NOT delivery-ready: "Vamos ver se os utilizadores gostam"
- ✅ Delivery-ready: "LUSOconta MVP: sucesso = 60% dos utilizadores completam onboarding bancário sem suporte humano em 2 semanas pós-launch. Medido via Mixpanel funnel."

### Gate 6 — Output uses CLIENT NAME + REAL data, no placeholder angle-brackets
- [ ] Zero instâncias de `[PRODUCT_NAME]`, `<feature>`, `[CLIENT]`, `[X semanas]`
- [ ] Nome do produto/cliente aparece no título e na hipótese central
- [ ] Números de ICE são específicos do produto (não os exemplos genéricos do template)
- [ ] Datas ou semanas concretas (ex: "semana de 14 Jul") em vez de offsets relativos vagos
- ❌ NOT delivery-ready: "O MVP do [produto] deve focar em [pain point principal]"
- ✅ Delivery-ready: "Pupli MVP — foco: tutor completa primeira reserva de treino sem falar com ninguém. Launch target: 28 Jul."

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados reais do cliente
- 🟡 **assumed** — plausível mas precisa de confirmação do cliente antes de entregar
- 🟢 **projection** — forecast by design (não verificável até execução)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa de verify antes de agir no scope. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
```
Auth — Impact 10, Confidence 10, Ease 8 → ICE 800 → MVP
Timeline: 4 semanas. Tech debt budget: 8h.
Sucesso = 60% conversão no onboarding.
```
*(reader assume que todos os ICE scores, a timeline e a métrica são factos validados — podem ser suposições do builder)*

✅ Delivery-ready:
```
🔵 Auth — Impact 10, Confidence 10, Ease 8 → ICE 800 → MVP
   (confirmado: blocker técnico, sem auth o core flow não funciona)
🟡 Onboarding flow — Impact 9, Confidence 7, Ease 6 → ICE 378 → MVP
   (ease estimado pelo builder; confirmar com dev lead antes de fechar scope)
🟢 Timeline total: 5 semanas (4 base + 1 buffer)
   (projection baseada em velocity estimada; ajustar após sprint 1)
🟡 Métrica de sucesso: 60% utilizadores completam core flow sem suporte
   (threshold proposto pelo builder; cliente precisa de validar o que define "sucesso" para este MVP)
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — ICE scores de ease/confidence validados com dev lead e PO; substituir estimativas com actuals
- [ ] All 🔵 citations added — fontes dos dados confirmados referenciadas (sessão de discovery, backlog existente, entrevistas de utilizador)
- [ ] All 🟢 projections labeled as such ao cliente — timeline e métricas de sucesso apresentadas como forecast, não como compromisso fixo

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# MVP Scope — Tributario.AI

**Hipótese central:** Contabilista consegue gerar resposta fiscal fundamentada para cliente
em <5 min, sem pesquisar manualmente no Portal das Finanças.

**Launch target:** 4 semanas (sprint início 1 Jul → entrega 26 Jul, buffer até 2 Ago)

---

## Feature Priority Matrix (ICE Scored)

| Feature | Impact | Confidence | Ease | ICE | Decisão |
|---|---|---|---|---|---|
| Upload doc fiscal + parse automático | 10 | 9 | 7 | 630 | ✅ MVP |
| Query em linguagem natural → resposta fundamentada | 10 | 8 | 6 | 480 | ✅ MVP |
| Citação automática de artigo legal | 9 | 8 | 7 | 504 | ✅ MVP |
| Histórico de queries por cliente | 7 | 9 | 8 | 504 | ✅ MVP |
| Export PDF da resposta | 6 | 9 | 8 | 432 | ✅ MVP |
| Multi-utilizador / equipa | 6 | 7 | 3 | 126 | 🔜 V1.1 |
| Integração AT (Autoridade Tributária) API | 8 | 3 | 2 | 48 | 📋 V1.2 |
| Painel de auditoria compliance | 5 | 5 | 3 | 75 | 📋 Backlog |
| White-label para ROC | 4 | 4 | 2 | 32 | 📋 Backlog |

**Threshold aplicado:** ≥300 MVP · 100–299 V1.1 · <100 Backlog

---

## MVP — IN (5 features)

1. **Upload + parse** — suporte PDF e XML (e-fatura). Base de tudo.
2. **Query NL → resposta** — core job-to-be-done. Sem isto não há produto.
3. **Citação legal automática** — diferenciador vs ChatGPT genérico; confiança do contabilista.
4. **Histórico por cliente NIF** — mínimo para uso profissional real.
5. **Export PDF** — output utilizável em contexto real de cliente.

---

## OUT do MVP — Cut List

| Feature | ICE | Motivo do corte | Destino |
|---|---|---|---|
| Multi-utilizador | 126 | Valida com 1 user solo primeiro; +3 sem dev | V1.1 (semana 8) |
| Integração AT API | 48 | API instável + auth complexa; parse de PDF cobre 90% casos | V1.2 (Q4) |
| Painel auditoria | 75 | Só relevante após base de utilizadores estabelecida | Backlog |
| White-label ROC | 32 | Mercado secundário; não valida hipótese principal | Backlog permanente |

---

## Timeline (5 semanas total)

| Semana | Datas | Milestone |
|---|---|---|
| Wk 1 | 1–5 Jul | Upload + parse PDF/XML funcional internamente |
| Wk 2 | 8–12 Jul | Query NL → resposta com citação legal (demo interno) |
| Wk 3 | 15–19 Jul | Histórico NIF + Export PDF + QA com 2 contabilistas beta |
| Wk 4 | 22–26 Jul | Bug fixes, polish, onboarding de 5 beta users |
| Buffer | 29 Jul–2 Ago | Margem para blocker inesperado (não usado = launch antecipado) |

**Tech debt budget:** 8h (20% de 40h dev total)
Alocado a: shortcuts de parsing edge cases — a refatorar em V1.1.

---

## Métrica de Sucesso MVP

**Primária:** 70% dos beta users completam query → PDF exportado sem pedir ajuda,
nas primeiras 2 semanas de uso.
**Medição:** logging interno de sessão (upload → export completo).
**Threshold:** ≥70% → avançar V1.1. <70% → entrevistar users e pivotar antes de escalar.
```

---

## Output anti-patterns

- **ICE somado em vez de multiplicado** — Impact 9 + Confidence 8 + Ease 7 = 24, não 504; invalida toda a priorização
- **MVP com >7 features "core"** — se tudo é prioritário, nada é; o corte não foi feito
- **Cut list sem destino** — dizer "fora do MVP" sem V1.1/V1.2/backlog deixa o cliente sem roadmap
- **Timeline sem buffer visível** — buffer absorvido silenciosamente é garantia de atraso surpresa
- **Hipótese central ausente** — lista de features sem a pergunta que o MVP vai responder não é scope, é wishlist
- **Métrica vaga** — "vemos se funciona" ou "bom feedback" não é mensurável nem accionável
- **Tech debt budget omitido** — sem limite declarado, shortcuts de MVP tornam-se dívida invisível
- **Placeholder angles no output final** — `[inserir produto]`, `<timeline>`, `[N semanas]` no entregável ao cliente
- **ICE scores copiados do template** — Auth 800, Dashboard 504 genéricos em vez de scores calculados para o produto real

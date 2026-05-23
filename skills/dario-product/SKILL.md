---
name: dario-product
description: "Product development — PRDs, user stories, MVP scoping, sprint planning, feature prioritization (RICE/ICE), technical specs, launch checklists, product roadmaps, competitive feature analysis. Triggers on: 'product', 'produto', 'PRD', 'user story', 'MVP', 'sprint', 'feature', 'roadmap produto', 'launch', 'lancamento', 'backlog', 'spec tecnica'."
license: MIT
---

# DARIO Product — Product Development & Management

## When to activate

- Building a new product (SaaS, app, platform)
- Writing PRD (Product Requirements Document)
- MVP scoping and prioritization
- Sprint planning for development team
- Feature prioritization (RICE/ICE scoring)
- Technical specification for developers
- Product launch checklist
- Competitive feature analysis

## Modules

### 1. PRD Generator (Product Requirements Document)

```markdown
## PRD — [Product Name] — [Feature/Version]

### Overview
- **Product:** [name]
- **Feature:** [what we're building]
- **Owner:** [PM name]
- **Date:** [YYYY-MM-DD]
- **Status:** [draft | review | approved | in-dev | shipped]

### Problem Statement
[Who has this problem? How do we know? What's the impact?]

### Goals & Success Metrics
| Goal | Metric | Target | Measurement |
|---|---|---|---|
| [goal 1] | [metric] | [target] | [how to measure] |

### User Stories
As a [persona], I want to [action], so that [benefit].
- US-001: As a [user], I want to [do X], so that [value]
- US-002: ...
- US-003: ...

### Scope
**In scope:** [what we ARE building]
**Out of scope:** [what we are NOT building — important to be explicit]
**Future consideration:** [things we might build later but not now]

### Requirements
#### Functional
1. [FR-001] System shall [requirement]
2. [FR-002] ...

#### Non-Functional
1. [NFR-001] Performance: page load < 2s
2. [NFR-002] Security: RGPD compliant
3. [NFR-003] Accessibility: WCAG 2.1 AA

### User Flow
```
[Step 1] → [Step 2] → [Decision] → [Step 3a] / [Step 3b] → [End]
```

### Wireframes / Mockups
[Links or descriptions of UI]

### Technical Considerations
- Stack: [recommended tech stack]
- APIs: [external integrations needed]
- Data model: [key entities and relationships]
- Dependencies: [what needs to exist before this can be built]

### Timeline
| Phase | Duration | Deliverable |
|---|---|---|
| Design | 1 week | Wireframes + approval |
| Development | 2-3 weeks | Working feature |
| QA | 1 week | Bug-free on staging |
| Launch | 2 days | Production deploy |

### Risks
| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| [risk 1] | [H/M/L] | [H/M/L] | [what we do about it] |

### Sign-off
- [ ] PM: [name]
- [ ] Tech Lead: [name]
- [ ] Design: [name]
- [ ] Stakeholder: [name]
```

### 2. MVP Scoper

Reduce a full product vision to minimum viable:

```markdown
## MVP Scope — [Product]

### Core Value Proposition (1 sentence)
[What is the ONE thing this product does that makes it worth using?]

### Must-Have (launch blockers)
1. [Feature] — because [without this, product has no value]
2. ...

### Should-Have (week 2-4 after launch)
1. [Feature] — because [improves retention but not critical for day 1]
2. ...

### Nice-to-Have (month 2+)
1. [Feature] — because [polishes experience]
2. ...

### Explicitly Excluded (say NO)
1. [Feature] — because [too complex / not validated / scope creep]
2. ...

### MVP Validation Criteria
- [ ] [X] users signed up in first [Y] days
- [ ] [Metric] reaches [threshold]
- [ ] Qualitative feedback: [what we need to hear]

### Estimated Effort
| Component | Effort | Who |
|---|---|---|
| Frontend | [X days] | [developer] |
| Backend | [X days] | [developer] |
| Design | [X days] | [designer] |
| Total | [X days] | |
```

### 3. Feature Prioritization (RICE)

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---|---|---|---|---|---|---|
| [feature 1] | [users/quarter] | [1-3] | [50-100%] | [person-months] | [R*I*C/E] | [rank] |

**Impact scale:**
- 3 = Massive (game-changer)
- 2 = High (significant improvement)
- 1 = Medium (noticeable)
- 0.5 = Low (minimal)
- 0.25 = Minimal (almost none)

### 4. Sprint Planning

```markdown
## Sprint [N] — [Start Date] to [End Date]

### Sprint Goal
[1 sentence: what we're trying to achieve this sprint]

### Backlog
| # | Story | Points | Assignee | Status |
|---|---|---|---|---|
| US-001 | [user story] | [1-13] | [name] | [todo/doing/done] |

### Capacity
| Team Member | Available Days | Story Points Capacity |
|---|---|---|
| [name] | [X days] | [~X points] |

### Definition of Done
- [ ] Code reviewed and merged
- [ ] Tests passing (unit + integration)
- [ ] Deployed to staging
- [ ] QA approved
- [ ] Documentation updated (if API change)
```

### 5. Technical Specification

```markdown
## Tech Spec — [Feature]

### Architecture
[High-level diagram or description]

### Data Model
```
Entity: [Name]
  - id: UUID (PK)
  - field_1: string (required)
  - field_2: integer (nullable)
  - created_at: timestamp
  - updated_at: timestamp

Relations:
  - [Entity A] 1:N [Entity B]
```

### API Endpoints
| Method | Path | Description | Auth |
|---|---|---|---|
| GET | /api/v1/[resource] | List all | Bearer token |
| POST | /api/v1/[resource] | Create new | Bearer token |

### Security Considerations
- [ ] Input validation on all endpoints
- [ ] Rate limiting
- [ ] RGPD: data retention policy
- [ ] Encryption at rest for PII

### Performance Requirements
- Response time: < 200ms p95
- Throughput: [X] requests/second
- Database: indexed queries only
```

### 6. Launch Checklist

```markdown
## Launch Checklist — [Product/Feature]

### Pre-Launch (T-7 days)
- [ ] All features tested on staging
- [ ] Performance tested (load test if applicable)
- [ ] Security review completed
- [ ] RGPD compliance verified
- [ ] Analytics tracking configured
- [ ] Error monitoring active (Sentry/equivalent)
- [ ] Backup and rollback plan documented
- [ ] Support team briefed

### Launch Day (T-0)
- [ ] Deploy to production
- [ ] Smoke test critical flows
- [ ] Monitor error rates (first 2 hours)
- [ ] Monitor performance metrics
- [ ] Social media announcement
- [ ] Email announcement to existing users
- [ ] Update marketing site

### Post-Launch (T+7 days)
- [ ] Review analytics (usage, errors, feedback)
- [ ] Address critical bugs (P1/P2)
- [ ] Collect user feedback (CSAT survey)
- [ ] Retrospective with team
- [ ] Update roadmap based on learnings
```

## Integration Points

- **dario-brand** → Product positioning and messaging
- **dario-offer** → Pricing and packaging for SaaS products
- **lucas-analytics** → Product metrics tracking
- **dario-ios-hig** → iOS-specific product design
- **A360 lp-builder** → Product landing pages
- **dario-sop** → Operational procedures for product team

## Red Flags

- Never ship without a rollback plan
- Never skip security review for products handling user data
- MVPs should be genuinely minimal — resist feature creep
- RICE scores should be challenged, not just calculated
- Technical specs need developer input, not just PM wishful thinking

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

---

### Gate 1 — Problem Statement tem evidência real, não suposição

- [ ] O problema está ligado a uma persona concreta (não "utilizadores em geral")
- [ ] Existe pelo menos uma métrica de impacto ("X horas perdidas por semana", "Y% churn atribuível")
- [ ] A source da evidência está indicada (entrevistas, dados analytics, benchmark)
- [ ] Não há frases tipo "acreditamos que" sem dados a suportar

❌ NOT delivery-ready: `"Os utilizadores têm dificuldade em gerir os seus documentos."`
✅ Delivery-ready: `"82% dos contabilistas da LUSOconta (n=17, entrevistas Jan 2025) perdem >3h/semana a reconciliar extratos — custo estimado €4.200/mês em tempo."`

---

### Gate 2 — Goals & Success Metrics são SMART e mensuráveis

- [ ] Cada goal tem um metric owner (quem mede)
- [ ] Targets têm baseline + prazo (não apenas "aumentar X%")
- [ ] Método de medição está especificado (GA4, Mixpanel, query SQL, etc.)
- [ ] Máximo 4 goals — se tiver mais, consolidar

❌ NOT delivery-ready: `"Meta: aumentar engagement. Medição: ver analytics."`
✅ Delivery-ready: `"Meta: activação D7. Metric: % users que criam 1ª guia ≤7 dias após registo. Baseline: 23%. Target: 45% até Q2. Owner: Ana Costa via Mixpanel cohort report."`

---

### Gate 3 — Scope tem "Out of scope" explícito e justificado

- [ ] "Out of scope" lista ≥3 itens com motivo ("too complex / não validado / scope creep")
- [ ] "Future consideration" está separado de "Out of scope"
- [ ] User stories cobrem happy path + pelo menos 1 edge case
- [ ] US-IDs estão numerados (US-001, US-002…) para rastreabilidade

❌ NOT delivery-ready: `"Out of scope: funcionalidades avançadas."`
✅ Delivery-ready: `"Out of scope: integração com ERP (Primavera) — dependência externa, fase 2. Exportação PDF multi-idioma — não validado com utilizadores. App mobile — equipa sem capacidade iOS em Q1."`

---

### Gate 4 — RICE/Prioritização tem números reais, não estimativas vagas

- [ ] Reach está em utilizadores/quarter com fonte (não "muitos utilizadores")
- [ ] Effort está em person-days (não "médio" ou "grande")
- [ ] RICE score calculado e features ranked por score, não por opinião
- [ ] Features com RICE < threshold definido estão explicitamente depriorizadas

❌ NOT delivery-ready: `"Feature A — Reach: alto, Impact: 3, Confidence: alta, Effort: médio → Priority: 1"`
✅ Delivery-ready: `"Notificações push — Reach: 340 users/Q, Impact: 2, Confidence: 70%, Effort: 0.5 PM → RICE: 952. Dashboard analytics — Reach: 120, Impact: 3, Confidence: 60%, Effort: 2 PM → RICE: 108. → Notificações prioritárias."`

---

### Gate 5 — Sprint Plan tem capacidade real e Definition of Done fechada

- [ ] Cada story point está assignada a uma pessoa (não "team")
- [ ] Capacidade calculada com dias reais (descontando férias, reuniões, buffer 20%)
- [ ] Story points totais ≤ capacidade total da equipa
- [ ] Definition of Done inclui critério de QA + deploy environment específico

❌ NOT delivery-ready: `"Sprint 3 — backlog: 34 pontos. Equipa: 3 devs."`
✅ Delivery-ready: `"Sprint 3 (20-31 Jan) — Rui: 8 dias úteis = 16pts. Marta: 6 dias (2 dias férias) = 12pts. Total capacity: 28pts. Backlog comprometido: 26pts. DoD: PR aprovado por 2 reviewers + testes Cypress passing + deploy em staging.cuidai.pt."`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets por preencher

- [ ] Zero instâncias de `[Product Name]`, `[PM name]`, `[metric]`, `[name]` no output final
- [ ] Datas são concretas (não `[YYYY-MM-DD]`)
- [ ] Stack tech mencionada é a stack real do cliente (não `[recommended tech stack]`)
- [ ] Sign-off lista nomes reais dos stakeholders

❌ NOT delivery-ready: `"Owner: [PM name] | Stack: [recommended tech stack] | Date: [YYYY-MM-DD]"`
✅ Delivery-ready: `"Owner: Pedro Alves | Stack: Next.js 14 + Supabase + Vercel | Date: 2025-02-03"`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## PRD — SAQUEI — Feature: Simulador de Crédito Instantâneo v1.0

### Overview
- **Produto:** SAQUEI (plataforma de crédito ao consumo Portugal)
- **Feature:** Simulador de crédito no frontend público (pré-login)
- **Owner:** Catarina Mendes (Product Lead)
- **Date:** 2025-02-03
- **Status:** approved — in-dev

### Problem Statement
**Quem:** Potenciais clientes SAQUEI na fase de consideração (visitam landing page mas não convertem).
**Evidência:** Heatmaps Hotjar (Jan 2025, n=4.200 sessões): 67% dos visitantes saem na página de pricing
sem interagir. Exit survey (n=89): 41% indicam "não percebi quanto ficaria a pagar."
**Impacto:** Taxa de conversão visita→registo actual: 3,2%. Benchmark sector (Cofidis PT): ~6,8%.
Gap de €18.000/mês em receita estimada assumindo ticket médio €850.

### Goals & Success Metrics
| Goal | Metric | Baseline | Target | Prazo | Owner |
|---|---|---|---|---|---|
| Aumentar conversão landing | Visita → registo | 3,2% | 5,5% | 30 dias pós-launch | Catarina (GA4) |
| Reduzir abandono pricing | Exit rate pricing page | 67% | <45% | 30 dias pós-launch | Catarina (Hotjar) |
| Engajamento simulador | % sessões com ≥1 simulação | 0% | 35% | 14 dias pós-launch | Dev (Mixpanel) |

### User Stories
- **US-001:** Como visitante não registado, quero inserir o montante e prazo desejados e ver a
  prestação mensal imediatamente, para decidir se o crédito cabe no meu orçamento.
- **US-002:** Como visitante, quero ver a TAE e TAEG calculadas automaticamente, para comparar
  com outras ofertas de forma transparente (requisito legal DL 74-A/2017).
- **US-003:** Como visitante que simulou, quero clicar "Pedir agora" e ter o valor pré-preenchido
  no formulário de registo, para não repetir o que já introduzi.
- **US-004 (edge case):** Como visitante que introduz montante fora do range (< €500 ou > €5.000),
  quero ver uma mensagem clara do limite disponível, para não ficar confuso.

### Scope
**In scope:**
- Slider interactivo: montante €500–€5.000 (step €100), prazo 6–48 meses (step 6)
- Cálculo em tempo real: prestação, TAE, TAEG, custo total
- CTA "Pedir agora" com pass de parâmetros para registo
- Versão mobile-first (60% do tráfego SAQUEI é mobile)

**Out of scope:**
- Simulação pós-login (existente, não tocar) — risco de regressão alto, sprint separado
- Comparador multi-produto — não validado, complexidade desnecessária para v1
- Integração com motor de scoring (Experian) — dado pré-login, sem dados do utilizador

**Future consideration (Q3 2025):**
- A/B test slider vs. input directo
- Simulação com seguro de proteção de pagamentos

### Requirements
#### Functional
1. [FR-001] Slider de montante actualiza resultados em <150ms (debounce 100ms)
2. [FR-002] Fórmula de cálculo de prestação: anuidade francesa com TAN 9,9% (fixo v1)
3. [FR-003] Exibição obrigatória: prestação, TAN, TAE, TAEG, custo total crédito (DL 74-A/2017)
4. [FR-004] CTA passa query params `?amount=XXXX&term=YY` para `/register`
5. [FR-005] Validação: montante fora [500, 5000] mostra inline error, não bloqueia UI

#### Non-Functional
1. [NFR-001] Performance: First Contentful Paint <1,2s (Core Web Vitals — Lighthouse ≥90)
2. [NFR-002] Acessibilidade: WCAG 2.1 AA — slider operável por teclado
3. [NFR-003] Sem cookies ou recolha de dados PII no simulador pré-login (RGPD)

### User Flow
```
Landing page → Ajusta slider (montante + prazo) → Vê prestação em real-time
    → Clica "Pedir agora" → Registo com dados pré-preenchidos → Funil de crédito
    ↓ (edge)
Montante fora de range → Inline message "Disponível entre €500 e €5.000"
```

### Technical Considerations
- **Stack:** React 18 + TypeScript (existente), styled-components, deploy Vercel
- **Cálculo:** Pure JS (sem API call) — fórmula anuidade francesa, TAN hardcoded v1
- **APIs:** Nenhuma nova em v1 — parâmetros passados via URL para `/register` (Next.js routing)
- **Data model:** Sem persistência — state local apenas
- **Dependências:** Design system SAQUEI v2.1 (slider component a criar ou adaptar de Radix UI)

### Timeline
| Phase | Duração | Deliverable | Responsável |
|---|---|---|---|
| Design | 3 dias (3–5 Fev) | Figma aprovado por Catarina | Rita Santos (Design) |
| Dev | 5 dias (6–12 Fev) | Feature em staging.saquei.pt | João Ferreira (Dev) |
| QA | 2 dias (13–14 Fev) | 0 bugs críticos, Lighthouse ≥90 | Mariana Cruz (QA) |
| Launch | 17 Fev | Deploy prod + Mixpanel event live | João + Catarina |

### RICE — Priorização contexto backlog Q1
| Feature | Reach | Impact | Confidence | Effort | RICE |
|---|---|---|---|---|---|
| Simulador pré-login (esta) | 4.200 visits/Q | 3 | 80% | 0.5 PM | **20.160** |
| Notificações push aprovação | 1.200 users/Q | 2 | 60% | 0.3 PM | **4.800** |
| Dashboard analytics cliente | 800 users/Q | 2 | 70% | 1.5 PM | **747** |

→ Simulador é prioridade #1 Q1 por margem larga.

### Risks
| Risco | Prob | Impact | Mitigação |
|---|---|---|---|
| Fórmula cálculo incorrecta (compliance) | M | H | Validação com advogado DL 74-A/2017 antes de dev (5 Fev) |
| Slider performance em dispositivos low-end | L | M | Teste em Android 8 + Chrome 90 durante QA |
| Design system sem slider → atraso | M | M | Fallback: Radix UI Slider com tema SAQUEI |

### Sign-off
- [x] PM: Catarina Mendes — 2025-02-03
- [ ] Tech Lead: João Ferreira — pendente revisão FR-001
- [ ] Design: Rita Santos — pendente Figma v2
- [ ] CEO/Stakeholder: Miguel Pinto — aprovação final 6 Fev
```

---

## Output anti-patterns

- **Angle-brackets no output final:** entregar PRD com `[PM name]`, `[metric]`, `[YYYY-MM-DD]` por preencher — o cliente recebe um template, não um documento
- **Problem Statement sem dados:** "os utilizadores querem X" sem entrevistas, analytics ou evidência quantificada
- **RICE com inputs vagos:** Impact "alto", Effort "médio" — torna a priorização indistinguível de opinião
- **Out of scope vazio ou genérico:** omitir o que NÃO se vai construir é a causa mais comum de scope creep em sprint
- **Sprint sem capacidade calculada:** comprometer 40 story points com equipa de 2 devs sem verificar dias disponíveis
- **Goals sem baseline:** "aumentar conversão 50%" sem saber o valor actual é impossível de validar
- **User stories só happy path:** não documentar edge cases (inputs inválidos, estados de erro, utilizador sem permissão) garante bugs em produção
- **Tech spec sem dependências:** não listar o que tem de existir antes de começar a feature atrasa sprints inteiros
- **Launch checklist copiada genericamente:** itens como "testar funcionalidades" sem especificar environment, responsável e critério de pass/fail
- **Sign-off sem nomes reais:** "Tech Lead: [name]" num documento aprovado é um risco de governance — quem assinou o quê?

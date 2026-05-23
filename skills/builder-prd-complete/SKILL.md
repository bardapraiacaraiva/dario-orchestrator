---
name: builder-prd-complete
description: >
  PRD (Product Requirements Document) completo: problema, solucao, user stories, criterios
  de aceitacao, wireframes, metricas de sucesso, riscos. De ideia a spec executavel.
  Use quando: PRD, requisitos, spec, user stories, criterios aceitacao, definir produto.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Product Requirements Document

## Proposito
Transformar uma ideia vaga num documento de requisitos que uma equipa (ou o DARIO) pode executar.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-prd-complete [produto]` | PRD completo |
| `/builder-prd-complete user-stories [feature]` | User stories apenas |
| `/builder-prd-complete acceptance [feature]` | Criterios de aceitacao |

## Template PRD

```markdown
# PRD — [Product Name]

## 1. Problem Statement
- Who has this problem?
- How painful is it? (1-10)
- How are they solving it today?
- Why is current solution insufficient?

## 2. Solution Overview
- One-sentence description
- Key differentiator
- Core value proposition

## 3. Target User
- Primary persona (from a360-avatar if available)
- Use cases (top 3)
- Jobs-to-be-done

## 4. User Stories
| # | As a... | I want to... | So that... | Priority |
|---|---------|-------------|-----------|----------|
| US-001 | new user | sign up with email | I can start using the product | Must |
| US-002 | admin | invite team members | my team can collaborate | Should |

## 5. Acceptance Criteria (per user story)
### US-001: Sign up
Given: I'm on the landing page
When: I click "Start Free" and enter my email + password
Then: I receive a verification email within 60 seconds
And: After verifying, I see the onboarding flow

## 6. Features (MVP vs Future)
### MVP (Week 1-4)
- [ ] Auth (email + password)
- [ ] Dashboard (basic)
- [ ] Core feature 1
- [ ] Core feature 2

### V1.1 (Week 5-8)
- [ ] Team collaboration
- [ ] Billing (Stripe)
- [ ] Integrations

## 7. Non-Functional Requirements
- Performance: page load < 2s
- Availability: 99.9% uptime
- Security: OWASP Top 10 compliance
- RGPD: consent, data export, deletion

## 8. Success Metrics
- Activation: 30% of signups complete onboarding
- Retention: 60% WAU after 4 weeks
- Conversion: 5% free → paid in 30 days

## 9. Risks & Mitigations
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Low adoption | High | Medium | Validate with 10 users before building |

## 10. Timeline
| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Discovery | 1 week | PRD + wireframes |
| Design | 1 week | Design system + mockups |
| Build MVP | 3 weeks | Working product |
| Launch | 1 week | Deploy + marketing |
```

## Output
1. PRD.md completo (todas as 10 seccoes)
2. User stories list (prioritizada)
3. Acceptance criteria (testable)
4. MVP scope (cut list)
5. Timeline estimate

## Red Flags
- PRD sem metricas de sucesso — como saber se funcionou?
- User stories sem criterios de aceitacao — ambiguidade
- MVP com mais de 5 features — nao e M (minimum)
- Sem riscos identificados — overconfidence

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Problem Statement tem dor quantificada e persona real

- [ ] "Who has this problem?" responde com persona específica, não "utilizadores"
- [ ] Pain score (1–10) está justificado com evidência (entrevistas, dados, benchmark)
- [ ] Solução atual do utilizador está descrita concretamente (ferramenta/processo, não "manual")
- [ ] Lacuna entre solução atual e proposta está articulada em 1–2 frases
- ❌ NOT delivery-ready: `"Quem tem o problema: utilizadores que precisam de gerir dados"`
- ✅ Delivery-ready: `"Freelancers de contabilidade (30–50 clientes/mês) gastam 4h/semana a exportar PDFs do Portal das Finanças — resolvem hoje com Excel + cópia manual; perde-se rastreabilidade de versões"`

---

### Gate 2 — User Stories seguem formato INVEST e têm prioridade defensável

- [ ] Todas as US têm ID único (US-001, US-002…) e formato "As a… / I want… / So that…" completo
- [ ] Prioridade (Must/Should/Could/Won't) está atribuída com critério explícito (MoSCoW)
- [ ] MVP contém ≤ 5 user stories marcadas "Must"
- [ ] Nenhuma US mistura duas funcionalidades distintas (violação de atomicidade)
- [ ] Pelo menos uma US cobre o happy path end-to-end do core use case
- ❌ NOT delivery-ready: `"US-004 | admin | gerir utilizadores e faturação | poupar tempo | Must"`
- ✅ Delivery-ready: `"US-004 | gestor de conta | exportar relatório mensal em PDF com filtro por cliente | enviar ao TOC sem reformatação manual | Must (blocker para faturação recorrente)"`

---

### Gate 3 — Acceptance Criteria são testáveis por um QA sem contexto adicional

- [ ] Cada US do MVP tem ≥ 1 critério no formato Given/When/Then
- [ ] Critérios incluem valores-limite concretos (timeouts, contagens, formatos)
- [ ] Critérios de erro/edge case cobertos para ≥ 50% das US Must
- [ ] Nenhum critério usa linguagem subjectiva ("rápido", "fácil", "adequado")
- ❌ NOT delivery-ready: `"Then: o utilizador vê uma mensagem de sucesso"`
- ✅ Delivery-ready: `"Then: o utilizador recebe email de confirmação em < 60s com link válido por 24h; se o link expirar, vê erro 'Link expirado — reenviar?' com botão de reenvio"`

---

### Gate 4 — MVP scope é genuinamente mínimo e timeline é credível

- [ ] MVP contém ≤ 5 features, cada uma justificada como blocker para validação
- [ ] Cut list (V1.1+) existe e é explícita — não apenas silêncio sobre features ausentes
- [ ] Timeline tem phases com durações e deliverables, não só "4 semanas"
- [ ] Non-functional requirements têm threshold numérico (não "rápido" ou "seguro")
- [ ] Pelo menos 1 NFR sobre RGPD/privacidade se o produto toca dados pessoais
- ❌ NOT delivery-ready: `"MVP: Auth, Dashboard, Reports, Notifications, Integrations, Billing, Admin panel"`
- ✅ Delivery-ready: `"MVP (3 semanas): Auth email/password, upload de extracto bancário, categorização automática — tudo o resto em V1.1. Cut: convites de equipa, Stripe, exportação CSV"`

---

### Gate 5 — Success Metrics são mensuráveis e têm baseline ou benchmark

- [ ] ≥ 3 métricas com valor-alvo numérico explícito
- [ ] Métricas cobrem pelo menos 2 de: Activation / Retention / Conversion / Revenue
- [ ] Cada métrica especifica janela temporal (30 dias, Semana 4, etc.)
- [ ] Método de medição indicado (Mixpanel, SQL query, form, etc.) para ≥ 1 métrica
- ❌ NOT delivery-ready: `"Sucesso: utilizadores satisfeitos e produto adoptado pela equipa"`
- ✅ Delivery-ready: `"Activation: 40% dos signups completam onboarding (≤ 5 passos) em < 10 min — medido via evento 'onboarding_complete' no Mixpanel — benchmark: média SaaS PT = 28%"`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero placeholders com angle-brackets

- [ ] Produto tem nome real, não `[Product Name]`
- [ ] Persona é específica do cliente, não genérica
- [ ] Nenhum `<inserir>`, `[TBD]`, `[client]`, `[feature]` no documento entregue
- [ ] Riscos são específicos ao contexto (mercado, equipa, tecnologia do cliente), não boilerplate
- ❌ NOT delivery-ready: `"# PRD — [Product Name] … Primary persona: [from a360-avatar if available]"`
- ✅ Delivery-ready: `"# PRD — Tributario.AI · Motor de Alertas Fiscais … Primary persona: Ana, TOC independente, 45 clientes, usa PHC + Portal das Finanças diariamente"`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no PRD output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via entrevistas, dados reais do cliente, ou sessão anterior
- 🟡 **assumed** — plausível dado o contexto, mas precisa de confirmação antes de entregar
- 🟢 **projection** — forecast por design (métrica-alvo, timeline estimada — não verificável hoje)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs. precisa de validação. **Honest transparency > PRD inflado com números inventados.**

---

❌ NOT delivery-ready:
```
## 8. Success Metrics
- Activation: 30% of signups complete onboarding
- Retention: 60% WAU after 4 weeks
- Conversion: 5% free → paid in 30 days

## 10. Timeline
| Build MVP | 3 weeks | Working product |
```
*Reader assume que os 30%, 60%, 5% e "3 semanas" são baseados em dados reais — podem ser benchmarks genéricos ou chutes.*

---

✅ Delivery-ready:
```
## 8. Success Metrics
- 🟢 Activation: 30% de signups completam onboarding (benchmark SaaS B2B — ajustar após semana 1)
- 🟡 Retention: 60% WAU após 4 semanas (assumido com base no segmento freelancer — confirmar com histórico de produto similar)
- 🔵 Conversion: 5% free → paid em 30 dias (validado em entrevista com founder, 12 Mar)

## 3. Target User
- 🔵 Persona primária: freelancers de contabilidade, 30–50 clientes/mês (10 entrevistas, Fev 2025)
- 🟡 Pain score: 8/10 (estimado — não quantificado com dados de suporte ainda)

## 10. Timeline
- 🟢 Build MVP: 3 semanas (estimativa baseline — dependente de stack escolhida e disponibilidade da equipa)
```

---

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — substituir pain scores assumidos, benchmarks de retenção e personas não validadas com dados reais do cliente
- [ ] Todos os itens 🔵 têm fonte citada no PRD (entrevista, data, documento de referência)
- [ ] Todos os itens 🟢 estão explicitamente comunicados ao cliente como projecções — não como compromissos de delivery ou métricas garantidas

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# PRD — SAQUEI · Funcionalidade "Poupança Automática com Regras"

## 1. Problem Statement
- **Quem tem o problema?** Utilizadores SAQUEI 25–38 anos, rendimento variável (freelancers,
  trabalhadores por turnos), que querem poupar mas falham por falta de automatismo
- **Dor:** 8/10 — 67% dos utilizadores SAQUEI (survey Jan 2025, n=312) dizem "esqueço-me
  de transferir" como razão principal para não poupar regularmente
- **Solução atual:** transferência manual mensal para conta poupança — 3 em cada 4 falham
  em Fevereiro
- **Insuficiência:** sem gatilho automático baseado em saldo disponível; concorrente Plum (UK)
  resolve isto, mas não opera em PT

## 2. Solution Overview
- **Uma frase:** Regras configuráveis que movem dinheiro automaticamente para cofre SAQUEI
  quando critérios de saldo/data são cumpridos
- **Diferenciador:** regras baseadas em saldo real (não data fixa) — adequado a rendimento
  variável
- **Core value:** "Poupei sem pensar nisso"

## 3. Target User
- **Persona primária:** Miguel, 31 anos, estafeta Glovo + biscates, rendimento entre
  €800–1.400/mês conforme semana; tem SAQUEI há 4 meses, saldo médio €230
- **Use cases top 3:**
  1. Poupar % do saldo quando ultrapassa threshold ("se tenho > €500, move 10%")
  2. Poupança recorrente semanal valor fixo
  3. Arredondamento de despesas para cofre (round-up)
- **Jobs-to-be-done:** "Quero que o dinheiro 'desapareça' antes de gastar sem pensar"

## 4. User Stories

| #      | As a…          | I want to…                                              | So that…                              | Priority |
|--------|----------------|----------------------------------------------------------|---------------------------------------|----------|
| US-001 | utilizador     | criar regra "se saldo > X€, move Y% para cofre"        | poupo automaticamente em dias bons    | Must     |
| US-002 | utilizador     | activar poupança recorrente semanal (valor fixo)        | tenho ritmo mesmo sem pensar          | Must     |
| US-003 | utilizador     | pausar qualquer regra por 7/14/30 dias                  | tenho controlo em meses difíceis      | Must     |
| US-004 | utilizador     | ver histórico de movimentos automáticos por regra       | percebo quanto poupei via automação   | Should   |
| US-005 | utilizador     | receber notificação push quando regra é executada       | não fico surpreendido com saldo baixo | Should   |
| US-006 | utilizador     | activar round-up de despesas para cofre                 | poupo sem esforço a cada pagamento    | Could    |

## 5. Acceptance Criteria

### US-001: Regra de threshold de saldo
- **Given:** estou no ecrã "Regras de Poupança" e tenho saldo disponível > 0€
- **When:** defino threshold = 500€ e percentagem = 10% e guardo
- **Then:** no dia seguinte às 08:00 (ou no momento se saldo já > 500€), sistema move
  10% do excedente para cofre, arredondado a cêntimo
- **And:** se saldo < 500€, regra não executa e não gera notificação
- **And:** movimento aparece em histórico com etiqueta "Regra automática · Threshold"
- **Edge case:** se transferência falhar (saldo insuficiente por débito simultâneo),
  regra adia 24h e utilizador recebe push "Regra não executada — saldo insuficiente"

### US-003: Pausar regra
- **Given:** tenho ≥ 1 regra activa
- **When:** selecciono "Pausar" e escolho 14 dias
- **Then:** regra muda estado para "Em pausa até DD/MM" e não executa durante período
- **And:** ao fim do período, retoma automaticamente sem acção do utilizador
- **And:** posso retomar manualmente antes do fim da pausa

## 6. Features

### MVP (Semanas 1–3)
- [x] US-001 — Regra threshold de saldo (core diferenciador)
- [x] US-002 — Poupança recorrente semanal
- [x] US-003 — Pausar regra

### V1.1 (Semanas 4–6)
- [ ] US-004 — Histórico por regra
- [ ] US-005 — Push notifications por execução
- [ ] US-006 — Round-up (requer integração mais profunda com processador)

**Cut do MVP (justificação):** histórico e notificações não bloqueiam validação de
adopção; round-up tem dependência técnica externa estimada em +2 semanas

## 7. Non-Functional Requirements
- **Performance:** criação de regra < 1.5s end-to-end; execução de regra (batch) < 5 min
  para 100% da base activa
- **Disponibilidade:** 99.9% uptime no engine de regras (max 8.7h downtime/ano)
- **Segurança:** movimentos requerem re-autenticação se > 7 dias sem login; logs de
  auditoria imutáveis por 5 anos
- **RGPD:** regras e histórico exportáveis via "Download dos meus dados"; eliminação
  de regras em cascata ao fechar conta (< 30 dias)
- **Limites:** máximo 5 regras activas por utilizador (MVP); valor mínimo por regra: 1€

## 8. Success Metrics

| Métrica         | Alvo                          | Janela   | Medição                          |
|-----------------|-------------------------------|----------|----------------------------------|
| Adopção         | 25% dos utilizadores activos criam ≥ 1 regra | Semana 4 | evento `rule_created` · Mixpanel |
| Retenção regras | 60% das regras criadas ainda activas | Dia 30   | SQL: `rules WHERE status=active AND created_at < now()-30d` |
| Poupança gerada | €50/utilizador/mês em média via regras | Mês 2    | soma de `auto_transfers` por user_id |
| Satisfação      | NPS feature ≥ 45              | Mês 1    | in-app survey pós primeira execução |

**Benchmark:** Plum UK reporta 34% adopção na primeira semana; alvo SAQUEI conservador
dado menor awareness de automação em PT

## 9. Risks & Mitigations

| Risco                              | Impacto | Probabilidade | Mitigação                                          |
|------------------------------------|---------|---------------|----------------------------------------------------|
| Utilizadores assustados com "dinheiro a mover sozinho" | Alto | Médio | onboarding explicativo + push de confirmação antes da 1ª execução |
| Race condition saldo (débito simultâneo) | Médio | Alto | lock optimista no momento de leitura de saldo; teste de carga Semana 2 |
| Baixa descoberta da feature        | Alto    | Médio | destacar no dashboard home para utilizadores com saldo > €200 |
| Regulação BdP sobre movimentos automáticos | Alto | Baixo | validar com jurídico SAQUEI antes de Semana 1 |

## 10. Timeline

| Fase        | Duração  | Deliverable                                              |
|-------------|----------|----------------------------------------------------------|
| Discovery   | 3 dias   | PRD validado + protótipo Figma (3 ecrãs) aprovado pelo CEO |
| Build MVP   | 3 semanas | US-001, US-002, US-003 em produção (feature flag 10% users) |
| Beta fechado | 1 semana | 50 utilizadores Miguel-persona; recolha NPS + bugs       |
| Rollout     | 1 semana | 100% base + push de lançamento + post LinkedIn SAQUEI    |
```

---

## Output anti-patterns

- **PRD sem nome real de produto** — `[Product Name]` no título de um documento "completo" é sinal de que o trabalho não começou
- **User stories com duas acções numa** — "gerir utilizadores e configurar faturação" é sempre duas US separadas
- **Acceptance criteria subjectivos** — "Then: experiência é boa" não é testável; QA não consegue pass/fail
- **MVP com 8+ features** — se é tudo Must, o critério de priorização está errado; forçar conversa de trade-offs
- **Métricas de vaidade sem baseline** — "10 000 utilizadores no mês 1" sem comparação com benchmark de mercado é ficção científica
- **Riscos copiados do template** — "Low adoption / High / Medium" sem contextualizar para o produto específico é ruído, não inteligência
- **Timeline sem deliverables concretos** — "Semana 3: desenvolvimento" não diz o que estará feito nem quem valida
- **Seção RGPD ausente** em produtos que processam dados pessoais (qualquer SaaS com auth e dados de utilizador)
- **Cut list silenciosa** — não mencionar o que foi excluído do MVP deixa stakeholders a assumir que "vem a seguir" sem compromisso

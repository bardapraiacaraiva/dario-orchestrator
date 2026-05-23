---
name: dario-support
description: "Customer support & client success — ticket templates, SLA tracking, FAQ generator, client health score, handover protocols, post-sale onboarding, churn prevention, CSAT surveys, support SOPs. Triggers on: 'support', 'suporte', 'ticket', 'SLA', 'cliente insatisfeito', 'churn', 'health score', 'handover', 'manutencao', 'retencao', 'FAQ client'."
license: MIT
---

# DARIO Support — Customer Success & Retention

## When to activate

- Client raises a support issue
- Need to create FAQ for client deliverables
- Client health score check (are they at risk?)
- Project handover (from build to maintenance)
- Post-sale onboarding sequence
- Churn prevention (client signals dissatisfaction)
- SLA tracking and reporting

## Modules

### 1. Client Health Score

```markdown
## Client Health Score — [Client] — [Date]

| Dimension | Weight | Score (1-10) | Weighted |
|---|---|---|---|
| Communication responsiveness | 20% | [X] | [X*0.2] |
| Payment timeliness | 20% | [X] | [X*0.2] |
| Scope satisfaction | 20% | [X] | [X*0.2] |
| Engagement (meetings, feedback) | 15% | [X] | [X*0.15] |
| Upsell potential | 10% | [X] | [X*0.1] |
| Referral likelihood (NPS proxy) | 15% | [X] | [X*0.15] |

**Total Score: [X/10]**

| Score | Status | Action |
|---|---|---|
| 8-10 | HEALTHY | Nurture, ask for referral/testimonial |
| 6-7.9 | NEUTRAL | Schedule check-in, address concerns |
| 4-5.9 | AT RISK | Immediate intervention, manager call |
| <4 | CRITICAL | Escalate to CEO, retention plan |
```

### 2. Ticket Template System

```markdown
## Support Ticket — [#TICK-XXX]

**Client:** [name]
**Priority:** [P1-critical | P2-high | P3-medium | P4-low]
**Category:** [bug | feature-request | question | complaint | change-request]
**SLA:** [P1: 4h | P2: 24h | P3: 48h | P4: 5 days]
**Assigned to:** [team member]
**Status:** [open | in-progress | waiting-client | resolved | closed]

### Description
[What the client reported]

### Steps to Reproduce (if bug)
1. ...

### Expected vs Actual
- Expected: ...
- Actual: ...

### Resolution
[What was done to fix it]

### Time spent
[Xh Xm]

### Follow-up needed?
[yes/no — if yes, what and when]
```

### 3. SLA Tracker

```markdown
## SLA Report — [Month]

| Client | Tickets | Avg Response | SLA Met | SLA Breached | Score |
|---|---|---|---|---|---|
| Atrium | 3 | 6h | 3 | 0 | 100% |
| Vivenda | 5 | 18h | 4 | 1 (P2 breach) | 80% |

### SLA Definitions
| Priority | First Response | Resolution | Escalation |
|---|---|---|---|
| P1 Critical | 4h | 24h | Immediate to CEO |
| P2 High | 24h | 72h | After 48h to director |
| P3 Medium | 48h | 5 days | After 3 days to director |
| P4 Low | 5 days | 10 days | No auto-escalation |
```

### 4. FAQ Generator (per client)

Auto-generate FAQ from project deliverables and common questions:

```markdown
## FAQ — [Client Website/Project]

### Geral
**Q: Como faco login no painel de administracao?**
A: Aceda a [URL]/wp-admin com as credenciais fornecidas na entrega do projecto.

**Q: Como actualizo o conteudo do site?**
A: [Instrucoes especificas ao CMS do cliente]

### SEO
**Q: Quando vou comecar a ver resultados do SEO?**
A: Os primeiros resultados tipicamente aparecem em 3-6 meses. Monitorizamos via GSC e enviamos relatorio mensal.

### Tecnico
**Q: O que fazer se o site ficar em baixo?**
A: Contactar [email suporte] imediatamente (P1). SLA: resposta em 4h.

### Facturacao
**Q: Quando recebo a factura?**
A: Facturas emitidas no dia 1 de cada mes. Pagamento a 30 dias.
```

### 5. Project Handover Protocol

When a build project ends and transitions to maintenance:

```markdown
## Handover — [Client] — [Date]

### 1. Deliverables Entregues
- [ ] Site live em producao
- [ ] Backups configurados (frequencia: [diaria/semanal])
- [ ] SSL certificado e renovacao automatica
- [ ] Analytics configurado (GA4 + GSC)
- [ ] Documentacao de acessos entregue ao cliente

### 2. Acessos Documentados
| Sistema | URL | User | Password Location |
|---|---|---|---|
| WordPress Admin | [url]/wp-admin | [user] | 1Password/vault |
| Hosting | [provider] | [user] | 1Password/vault |
| Domain | [registrar] | [user] | 1Password/vault |
| GA4 | analytics.google.com | [email] | Google account |
| GSC | search.google.com | [email] | Google account |
| GBP | business.google.com | [email] | Google account |

### 3. Manutencao Contratada
| Servico | Incluido | Frequencia |
|---|---|---|
| Updates WordPress core | Sim | Mensal |
| Updates plugins | Sim | Mensal |
| Backups | Sim | Diario |
| Monitoring uptime | Sim | 24/7 |
| Alteracoes conteudo | [X]h/mes | On-demand |
| Suporte tecnico | SLA P2 | On-demand |
| Relatorio SEO | Sim | Mensal |

### 4. Contactos Suporte
- Email: [suporte@agencia.pt]
- SLA: P2 (resposta em 24h)
- Horario: Seg-Sex 9h-18h

### 5. Proximos Passos
- [ ] Reuniao de entrega com cliente (walkthrough)
- [ ] Email de boas-vindas ao suporte
- [ ] Primeiro relatorio em 30 dias
```

### 6. Post-Sale Onboarding Email Sequence

```
Email 1 (Dia 0 — apos assinatura):
Subject: "Bem-vindo/a a [Agencia]! Proximos passos"
Content: O que esperar, timeline, contacto directo

Email 2 (Dia 3):
Subject: "O que precisamos de si para comecar"
Content: Checklist de acessos, conteudos, branding assets

Email 3 (Dia 7):
Subject: "O seu projecto esta em andamento"
Content: Update de progresso, proximo milestone

Email 4 (Dia 14):
Subject: "Primeiro draft pronto para revisao"
Content: Link para staging, como dar feedback

Email 5 (Dia 30):
Subject: "O seu projecto esta live!"
Content: Entrega final, handover, intro ao suporte
```

### 7. Churn Prevention Playbook

| Signal | Trigger | Action |
|---|---|---|
| Nao responde ha 2 semanas | Email sem resposta x2 | Telefonema pessoal do account manager |
| Pagamento atrasado >15 dias | Invoice overdue | Reminder amigavel + check-in |
| Pedido de "pausa" | Cliente pede para pausar servicos | Reuniao para entender, oferecer ajuste |
| Compara com concorrente | Menciona outro fornecedor | Value reinforcement + competitive analysis |
| Feedback negativo | CSAT <3/5 ou review negativa | Escalate to CEO, recovery plan em 48h |
| Sem engagement | Nao abre emails, nao ve relatorios | Check-in pessoal, simplificar comunicacao |

## Integration Points

- **lucas-finance** → Receivables tracking alimenta payment health
- **dario-legal** → Contratos definem SLA e scope
- **dario-email-seq** → Post-sale onboarding sequence
- **lucas-analytics** → Client health score integra no revenue dashboard
- **dario-orchestrator** → Support tickets podem gerar tasks no taskboard

## Red Flags

- NUNCA ignorar um P1 — site em baixo e emergencia
- SLA breaches devem ser comunicados proactivamente ao cliente (nao esconder)
- Client health score <4 = reuniao com CEO em 48h
- Handover incompleto = suporte reactivo caro — investir no handover

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Health Score tem dados reais, não placeholders

- [ ] Todos os 6 campos têm score numérico (1–10), não `[X]`
- [ ] Weighted total está calculado (ex: `8 × 0.20 = 1.60`, soma final visível)
- [ ] Status final (HEALTHY / NEUTRAL / AT RISK / CRITICAL) está declarado
- [ ] Acção recomendada é específica ("agendar call dia 15" ≠ "schedule check-in")
- [ ] Data do health score está preenchida (não `[Date]`)

❌ NOT delivery-ready: `| Payment timeliness | 20% | [X] | [X*0.2] |`
✅ Delivery-ready: `| Payment timeliness | 20% | 9 | 1.80 |` → `**Total Score: 8.15/10 — HEALTHY**`

---

### Gate 2 — Ticket tem prioridade, SLA e assignee concretos

- [ ] Número de ticket gerado (ex: `#TICK-047`), não `#TICK-XXX`
- [ ] Prioridade declarada (P1/P2/P3/P4) com SLA correspondente escrito
- [ ] "Assigned to" tem nome real de pessoa, não `[team member]`
- [ ] Description é o problema real do cliente, não `[What the client reported]`
- [ ] Follow-up tem data concreta se "yes" (ex: "follow-up 23 Jun 09h00")

❌ NOT delivery-ready: `**Assigned to:** [team member]` / `**SLA:** [P1: 4h | P2: 24h]`
✅ Delivery-ready: `**Assigned to:** Ricardo Silva` / `**SLA:** P2 — resposta até 24h (prazo: 22 Jun 17h00)`

---

### Gate 3 — SLA Report tem métricas reais do mês corrente

- [ ] Mês/ano do report está preenchido (ex: "Junho 2025")
- [ ] Pelo menos 2 clientes reais na tabela com tickets contados
- [ ] Breaches identificados com explicação (qual ticket, qual desvio, causa)
- [ ] Score % calculado por cliente (tickets met ÷ total × 100)
- [ ] Acção de remediação mencionada para qualquer breach ≥ P2

❌ NOT delivery-ready: tabela com `[Client]` / `[Avg Response]` / `[Score]` em branco
✅ Delivery-ready: `| Cuidai | 4 | 11h | 4 | 0 | 100% |` + `| Vivenda | 3 | 31h | 2 | 1 (P2 breach #TICK-031, atraso 7h por ausência de dev) | 67% |`

---

### Gate 4 — FAQ é específico ao projecto/cliente, não genérico

- [ ] URL real do painel admin do cliente (não `[URL]/wp-admin`)
- [ ] CMS identificado (WordPress, Webflow, Shopify…) com instruções concretas
- [ ] Pelo menos 1 pergunta de facturação com data real de emissão e IBAN/método
- [ ] Contacto de suporte tem email real (não `[email suporte]`)
- [ ] Secção técnica menciona o provider de hosting real do cliente

❌ NOT delivery-ready: `A: Aceda a [URL]/wp-admin com as credenciais fornecidas`
✅ Delivery-ready: `A: Aceda a https://cuidai.pt/wp-admin — user: admin@cuidai.pt — password em 1Password vault "Cuidai WP"`

---

### Gate 5 — Handover Protocol tem todos os acessos documentados

- [ ] Tabela de acessos tem URL real por sistema (não `[url]/wp-admin`)
- [ ] Password location especifica o vault/ferramenta (ex: "1Password → vault Atrium → entry 'WP Admin'")
- [ ] Manutenção contratada tem horas/mês de conteúdo preenchidas (ex: `2h/mês`)
- [ ] Checklist de deliverables entregues tem checkboxes marcados (`[x]`) com data
- [ ] "Próximos Passos" tem datas ou responsáveis atribuídos

❌ NOT delivery-ready: `| WordPress Admin | [url]/wp-admin | [user] | 1Password/vault |`
✅ Delivery-ready: `| WordPress Admin | https://atrium.pt/wp-admin | atrium_admin | 1Password → vault "Atrium" → "WP Admin" |`

---

### Gate 6 — Output uses CLIENT NAME + REAL data, no placeholder angle-brackets

- [ ] Zero instâncias de `[Client]`, `[Date]`, `[X]`, `[name]`, `[email]`, `[provider]`
- [ ] Cliente nomeado no título de cada módulo entregue
- [ ] Sequência de onboarding tem nome do cliente no subject das emails
- [ ] Churn playbook (se incluído) referencia o sinal real observado no cliente
- [ ] Qualquer data no documento é uma data real (DD Mês AAAA)

❌ NOT delivery-ready: `Subject: "Bem-vindo/a a [Agencia]! Próximos passos"`
✅ Delivery-ready: `Subject: "Bem-vindo à Atelier AI! Próximos passos — projecto website + SEO"`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Client Health Score — Cuidai — 19 Jun 2025

| Dimension                      | Weight | Score (1-10) | Weighted |
|-------------------------------|--------|--------------|---------|
| Communication responsiveness  | 20%    | 8            | 1.60    |
| Payment timeliness            | 20%    | 10           | 2.00    |
| Scope satisfaction            | 20%    | 7            | 1.40    |
| Engagement (meetings, feedback)| 15%   | 6            | 0.90    |
| Upsell potential              | 10%    | 8            | 0.80    |
| Referral likelihood (NPS proxy)| 15%   | 7            | 1.05    |

**Total Score: 7.75/10 — NEUTRAL**
Acção: Agendar check-in 26 Jun com Ana Rodrigues (CEO Cuidai) —
foco em scope satisfaction (módulo agendamentos ainda pendente de feedback).

---

## Support Ticket — #TICK-052

**Client:** Cuidai
**Priority:** P2 — High
**Category:** Bug
**SLA:** Resposta até 24h → prazo 20 Jun 11h00
**Assigned to:** Ricardo Silva
**Status:** in-progress

### Description
Botão "Agendar Consulta" na homepage não redireciona para o formulário
Calendly após deploy de ontem (18 Jun). Reportado por Ana Rodrigues via
email às 11h02.

### Steps to Reproduce
1. Aceder a https://cuidai.pt
2. Clicar em "Agendar Consulta" (hero section, CTA principal)
3. Esperado: redirecionar para https://calendly.com/cuidai/consulta
4. Actual: 404 — link aponta para /agendar (slug removido no deploy)

### Expected vs Actual
- Expected: redirect para Calendly funcional
- Actual: página 404 /agendar

### Resolution
Corrigir href no botão para https://calendly.com/cuidai/consulta.
Deploy via WP Admin > Elementor > Hero Section > CTA Button.
Fix estimado: 30 min.

### Time spent
0h 45m

### Follow-up needed?
Sim — confirmar com Ana Rodrigues até 20 Jun 14h00 que botão funciona
em mobile + desktop. Screenshot de confirmação para fechar ticket.

---

## Handover — Cuidai — 19 Jun 2025

### 1. Deliverables Entregues
- [x] Site live em produção — https://cuidai.pt (19 Jun 2025)
- [x] Backups configurados — diário 03h00, retençao 30 dias (UpdraftPlus → Google Drive Cuidai)
- [x] SSL certificado — Let's Encrypt, renovação automática via Cloudflare
- [x] Analytics configurado — GA4 (G-4KX91MWR2) + GSC verificado
- [x] Documentação de acessos entregue a Ana Rodrigues em 18 Jun (PDF + 1Password share)

### 2. Acessos Documentados
| Sistema        | URL                              | User                  | Password Location                        |
|---------------|----------------------------------|-----------------------|------------------------------------------|
| WordPress Admin| https://cuidai.pt/wp-admin       | ana@cuidai.pt         | 1Password → vault "Cuidai" → "WP Admin" |
| Hosting        | SiteGround → my.siteground.com   | billing@cuidai.pt     | 1Password → vault "Cuidai" → "Hosting"  |
| Domain         | GoDaddy → account.godaddy.com    | ana@cuidai.pt         | 1Password → vault "Cuidai" → "Domínio"  |
| GA4            | analytics.google.com             | analytics@cuidai.pt   | Google Workspace Cuidai                  |
| GSC            | search.google.com/search-console | analytics@cuidai.pt   | Google Workspace Cuidai                  |
| GBP            | business.google.com              | ana@cuidai.pt         | Google Workspace Cuidai                  |

### 3. Manutenção Contratada (Plano Starter — 89€/mês)
| Serviço                  | Incluído | Frequência       |
|--------------------------|----------|------------------|
| Updates WordPress core   | Sim      | Mensal (dia 1)   |
| Updates plugins          | Sim      | Mensal (dia 1)   |
| Backups                  | Sim      | Diário           |
| Monitoring uptime        | Sim      | 24/7 (UptimeRobot)|
| Alterações conteúdo      | 2h/mês   | On-demand        |
| Suporte técnico          | P2 SLA   | On-demand        |
| Relatório SEO            | Sim      | Mensal (dia 5)   |

### 4. Contactos Suporte
- Email: suporte@atelierai.pt
- SLA: P2 (resposta em 24h úteis)
- Horário: Seg–Sex 09h00–18h00

### 5. Próximos Passos
- [ ] Reunião walkthrough com Ana Rodrigues — 23 Jun 10h00 (Google Meet, convite enviado)
- [ ] Email boas-vindas ao suporte enviado — 19 Jun ✓
- [ ] Primeiro relatório SEO — 5 Jul 2025 (Ricardo Silva responsável)
```

---

## Output anti-patterns

- Gerar health score sem calcular o weighted total — entregar tabela com `[X*0.2]` por preencher
- Usar `[Client]`, `[Date]`, `[team member]` no output final — qualquer angle-bracket = não entregável
- Criar FAQ genérica sem URL real, CMS identificado ou contacto de suporte preenchido
- Handover sem password location específico — "1Password/vault" sem nomear o vault não é documentação
- Ticket sem prazo SLA calculado em data/hora concreta — "P2: 24h" sem anchor temporal não é accionável
- Churn playbook sem sinal observado real — listar os sinais genéricos da tabela sem identificar qual se aplica ao cliente
- Sequência de onboarding com `[Agencia]` no subject — cliente recebe email com placeholder visível
- SLA Report sem identificar causa dos breaches — "1 breach" sem explicação não permite remediação
- Health score com status CRITICAL sem acção de escalada concreta (nome do manager, data da call)
- Misturar módulos de clientes diferentes no mesmo output sem separação clara de cabeçalho

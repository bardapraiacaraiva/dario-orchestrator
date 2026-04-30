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

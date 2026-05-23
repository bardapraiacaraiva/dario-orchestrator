---
name: dario-sop
description: SOP (Standard Operating Procedure) generator — creates step-by-step documented procedures for any repeatable process. Uses Operations Squad (Carpenter, Gawande, Gerber). Triggers on "sop", "procedimento", "documentar processo", "checklist operacional", "standard operating procedure", "como fazer".
license: MIT
---

# DARIO Skill — SOP Generator

## Workflow
1. RAG: `search_kb("sop standard operating procedure checklist process", collection: "dario")`
2. Identify the process to document
3. Interview/observe: what steps, what order, what tools, what decisions
4. Write SOP with: objective, scope, steps, decision points, exceptions, QA check
5. Add Gawande checklist (5-9 items) for quality gate
6. Save to Obsidian + optionally ingest in RAG

## SOP template
```
## SOP: [Process Name]
**Version:** 1.0 | **Owner:** [Name] | **Last updated:** [Date]

### Objective
[What this process achieves]

### Trigger
[When to start this process]

### Steps
1. [Action] → [Expected result]
2. [Action] → [Expected result]
...

### Decision points
- If [condition]: do [A]
- If [condition]: do [B]

### Quality checklist
- [ ] [Check 1]
- [ ] [Check 2]
...

### Exceptions
- [Edge case] → [How to handle]

### Tools needed
- [Tool 1]
- [Tool 2]
```

## Common Agency SOPs (ready to generate)

| SOP | Trigger | Typical Steps |
|-----|---------|--------------|
| New client onboarding | Contract signed | Kickoff call → brief → access gathering → baseline audit → timeline → Slack channel |
| Website launch | Site approved | Pre-launch checklist → DNS → SSL → redirects → analytics → indexing → announce |
| Content publication | Article approved | SEO check → images → schema → preview → publish → social → email → GSC |
| Monthly SEO report | 1st of month | GSC data → analytics → rankings → actions → client email |
| Invoice + follow-up | Work delivered | Generate invoice → send → 7-day follow-up → 14-day reminder → escalate |
| Client offboarding | Contract ends | Final delivery → access handover → archive project → feedback request |
| Bug/issue response | Client reports bug | Triage (P1-P3) → acknowledge (<2h) → investigate → fix → verify → close |
| Backup & recovery | Weekly / incident | Verify backups → test restore → document → alert if failed |

## Gawande Checklist Rules (from The Checklist Manifesto)

1. **5-9 items max** — more than 9, people skip them
2. **DO-CONFIRM format** — do the work from memory, THEN run checklist to verify
3. **READ-DO format** — read each item, do it, check it off (for unfamiliar tasks)
4. **Single-page** — if it doesn't fit on one page, it's too long
5. **Test in real conditions** — pilot with the team before finalizing
6. **Version + owner** — every checklist has a responsible person and a date

## Example: Client Onboarding SOP (expanded)

```markdown
## SOP: New Client Onboarding
**Version:** 2.0 | **Owner:** Account Manager | **Last updated:** 2026-04-27

### Objective
Ensure every new client is properly set up within 48h of contract signing with zero missed steps.

### Trigger
Contract signed + payment received (or first invoice sent)

### Steps
1. Create client folder in Obsidian → `01 - Projetos/<Client Name>/`
2. Run `/dario-client-onboard` → auto-creates memory, RAG context, audit baseline
3. Schedule kickoff call (within 3 business days)
4. Send pre-kickoff brief questionnaire (use dario-briefing template)
5. Gather access: hosting, CMS, analytics, GSC, GBP, social accounts
6. Run baseline diagnostic → `/dario-diagnose`
7. If WordPress: run `/dario-wp-audit` + `/dario-woo-audit` (if ecommerce)
8. Create project in orchestrator taskboard → define first sprint tasks
9. Setup communication channel (Slack channel or WhatsApp group)
10. Send welcome email with: timeline, team contacts, how to request support

### Decision points
- If client has WordPress → add wp-audit + woo-audit to sprint 1
- If client is new brand → add dario-brand before any marketing work
- If client has existing SEO → run seo-audit before seo-plan
- If budget < 2000€/month → limit to 1 parallel track; if > 5000€ → 3 parallel

### Quality checklist (DO-CONFIRM)
- [ ] Client folder created in Obsidian
- [ ] Agent memory project file exists
- [ ] All access credentials received and stored securely
- [ ] Baseline diagnostic completed and saved
- [ ] Kickoff call scheduled within 3 business days
- [ ] First sprint tasks created in taskboard
- [ ] Welcome email sent with timeline

### Exceptions
- Client unresponsive after contract → 3-day follow-up → 7-day escalate to owner
- Missing access credentials → document what's missing, proceed with available, flag blocked tasks
- Contract scope unclear → pause onboarding, schedule scope clarification call

### Tools needed
- Claude Code (orchestrator, skills)
- Obsidian vault (D.A.R.I.O)
- Client communication channel
- Access management (1Password or similar)
```

## SOP Complexity Guide

| Complexity | Steps | Format | Review Cycle |
|------------|-------|--------|-------------|
| Simple | 3-5 | Single checklist | 6 months |
| Standard | 6-10 | Template above | 90 days |
| Complex | 11-15 | Split into 2-3 sub-SOPs | 60 days |
| Critical | Any | Add approval gate + training | 30 days |

## Integration

- Pairs with `dario-hr` for team onboarding SOPs
- Pairs with `dario-support` for client-facing SOPs
- Pairs with `dario-client-onboard` — the onboarding SOP is the human wrapper around the automated skill
- Generated SOPs can be ingested into RAG for future reference
- Save complex SOPs as Obsidian notes for team access

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Process> - SOP.md`

## Red Flags

- Never create SOPs for processes that change weekly — those need guidelines, not procedures
- Never exceed 15 steps without splitting into sub-SOPs
- Never skip the "Exceptions" section — edge cases cause the most errors
- Always include "who does what" — a checklist without ownership is decoration
- Review and update SOPs every 90 days or after any incident

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Processo identificado com precisão cirúrgica
- [ ] O nome do processo é específico, não genérico ("Publicação de artigo no blog da Cuidai" vs "content process")
- [ ] O **Trigger** é uma condição mensurável, não uma intenção ("Artigo aprovado por Pedro Matos via comentário Notion" vs "quando estiver pronto")
- [ ] O **Scope** delimita o que está FORA do processo (o que este SOP NÃO cobre)
- [ ] Version + Owner preenchidos com nome real, não cargo genérico

❌ NOT delivery-ready: `**Owner:** Account Manager | **Last updated:** [Date]`
✅ Delivery-ready: `**Owner:** Mariana Fonseca | **Last updated:** 2025-06-11 | **Version:** 1.2`

---

### Gate 2 — Steps com Action → Expected Result verificável
- [ ] Cada step tem verbo de ação no imperativo ("Exporta", "Envia", "Cria")
- [ ] Cada step tem resultado esperado concreto ("→ ficheiro GSC_Jun2025.csv em `/Relatórios/`")
- [ ] Nenhum step tem mais de 2 sub-acções (se tiver, partir em steps separados)
- [ ] Steps estão numerados e em ordem cronológica real, não ideal

❌ NOT delivery-ready: `1. Gather access → proceed to next step`
✅ Delivery-ready: `1. Solicita acesso ao GSC via Google Search Console → Mariana adicionada como "Owner" confirmada por email de notificação Google`

---

### Gate 3 — Decision points cobrem os casos reais do cliente
- [ ] Mínimo 2 decision points (If/Then) documentados
- [ ] Cada ramo tem acção definida, não "consultar equipa"
- [ ] Casos de budget, plataforma e scope estão cobertos se relevantes
- [ ] Decision points reflectem situações já ocorridas, não hipotéticas

❌ NOT delivery-ready: `- If client has WordPress → add wp-audit`
✅ Delivery-ready: `- Se Atrium usar WooCommerce (confirmado): adiciona /dario-woo-audit ao Sprint 1 antes da reunião de kick-off`

---

### Gate 4 — Gawande Checklist válida (5-9 items, formato correcto)
- [ ] Entre 5 e 9 items — nem mais, nem menos
- [ ] Formato declarado: DO-CONFIRM (processo conhecido) ou READ-DO (processo novo)
- [ ] Cada item é verificável por um terceiro sem contexto adicional
- [ ] Checklist cabe numa única página / bloco de markdown sem scroll extenso

❌ NOT delivery-ready: `- [ ] Verificar tudo está bem antes de publicar`
✅ Delivery-ready: `- [ ] URL canónica definida e sem conflito com staging (verificar em Search Console Preview)`

---

### Gate 5 — Exceptions section não está em branco ou genérica
- [ ] Mínimo 3 excepções documentadas com acção específica
- [ ] Cada excepção tem prazo ou escalation path ("→ escala para owner em 24h")
- [ ] Edge cases do cliente específico estão incluídos (não só boilerplate)
- [ ] "Cliente não responde" tem protocolo de 3 níveis (follow-up → escalate → pause)

❌ NOT delivery-ready: `- Edge case → handle appropriately`
✅ Delivery-ready: `- Credenciais de hosting da LUSOconta não fornecidas em 48h → documentar em Obsidian como "bloqueado", notificar Rui Dias por WhatsApp, pausar steps 5-7`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Zero instâncias de `[Client Name]`, `[Date]`, `[Name]`, `[Tool]` no output final
- [ ] Nome do cliente aparece pelo menos 3x no documento (header, decision points, exceptions)
- [ ] Datas são reais ou relativas ("2025-06-11", "D+3 após contrato assinado")
- [ ] Tools listadas são as ferramentas reais do cliente (Obsidian, Notion, 1Password, etc.)

❌ NOT delivery-ready: `**Owner:** [Name] | **Last updated:** [Date]` — angle-brackets no output entregue
✅ Delivery-ready: `**Owner:** Ana Ribeiro (Cuidai) | **Last updated:** 2025-06-11 | Revisto em: 2025-09-11`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact num SOP gerado deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via cliente data, sessão anterior, ou vault/RAG existente
- 🟡 **assumed** — plausível para o processo descrito, mas precisa de confirmação antes de entregar o SOP
- 🟢 **projection** — estimativa por design (prazo esperado, volume típico — não verificável sem execução real)

Output checklist upfront mostra ao leitor exatamente o que está validado vs. o que precisa de sign-off antes de o SOP ir para produção. **Honest transparency > SOP que parece completo mas tem gaps escondidos.**

---

❌ NOT delivery-ready:
```
### Steps
1. Enviar welcome email ao cliente em 24h
2. Criar canal Slack com 3 membros da equipa
3. Correr baseline diagnostic — resultado esperado: score > 70
```
*(Reader assume que os prazos, nomes e métricas são factos — podem ser assumptions sem base no cliente real.)*

✅ Delivery-ready:
```
### Steps
1. Enviar welcome email ao cliente em 🟢 **projection: 24h** (baseline de agência; confirmar SLA contratual)
2. Criar canal Slack com 🟡 **assumed: 3 membros** (Account Manager + Lead + Cliente — confirmar equipa real)
3. Correr baseline diagnostic → resultado esperado: 🔵 **verified: score > 70** (threshold definido em sessão 2025-04-10)
```

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir assumptions com actuals do cliente (owner, ferramentas, nº de steps, SLAs reais)
- [ ] All 🔵 items com citation adicionada — fonte: sessão, vault path, ou documento de referência
- [ ] All 🟢 projections comunicadas explicitamente ao cliente — deixar claro que são estimativas de design, não garantias operacionais
- [ ] Version + Owner preenchidos com dados reais (não placeholders `[Name]` / `[Date]`)
- [ ] SOP pilotado em condições reais antes de marcar como `v1.0 — Production Ready`

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## SOP: Publicação de Artigo SEO — Blog Cuidai
**Version:** 1.3 | **Owner:** Ana Ribeiro | **Last updated:** 2025-06-11
**Review cycle:** 90 dias | **Próxima revisão:** 2025-09-11

### Objective
Garantir que cada artigo publicado no blog cuidai.pt cumpre todos os requisitos
SEO, editorial e de distribuição antes de ficar indexável, sem passos omitidos.

### Trigger
Artigo marcado como "Aprovado" por Ana Ribeiro no quadro Notion
"Editorial Cuidai" (coluna: Pronto para Publicar)

### Scope
Este SOP cobre: revisão final → publicação WordPress → distribuição.
NÃO cobre: criação de conteúdo, briefing SEO, aprovação editorial (ver SOP-EDITORIAL-01).

### Steps
1. Abre o artigo no WordPress (cuidai.pt/wp-admin) → confirma slug limpo
   → resultado: URL sem datas, sem stop words (ex: `/cuidados-alzheimer-casa/`)
2. Cola conteúdo aprovado do Notion → remove formatação residual com "Colar como texto"
   → resultado: zero tags HTML espúrias no editor Gutenberg
3. Corre Yoast SEO → verde em Legibilidade E SEO
   → resultado: keyword principal "cuidados domiciliários Lisboa" com densidade 1-2%
4. Adiciona imagem destacada (formato WebP, max 120KB, alt-text descritivo)
   → resultado: ficheiro nomeado `cuidados-alzheimer-casa-hero.webp` em `/uploads/2025/06/`
5. Adiciona schema FAQ Gutenberg block se artigo tem secção Q&A
   → resultado: preview em Google Rich Results Test sem erros
6. Define data de publicação → clica "Agendar" (não "Publicar" imediato)
   → resultado: post agendado para terça ou quinta, 09h00 Lisboa
7. Após publicação automática: partilha no LinkedIn da Cuidai + Instagram Stories
   → resultado: post LinkedIn com primeiros 150 chars do artigo + link
8. Submete URL no Google Search Console → Inspecionar URL → Solicitar indexação
   → resultado: confirmação "URL está no Google" ou "Indexação solicitada"
9. Actualiza quadro Notion: mover cartão para coluna "Publicado" + adicionar URL final
   → resultado: cartão com link, data e responsável preenchidos

### Decision points
- Se artigo > 2000 palavras: adicionar índice (Table of Contents block) no topo
- Se keyword tem volume > 1000/mês (Ahrefs): adicionar internal links de pelo menos
  2 artigos existentes apontando para este
- Se cuidai.pt estiver em manutenção (plugin WP Maintenance): aguardar janela
  de publicação acordada com Hélder (DevOps), não forçar publicação
- Se artigo tem receitas ou comparações de produtos: adicionar schema HowTo ou
  schema Product — verificar com /dario-schema antes de publicar

### Quality checklist (DO-CONFIRM)
- [ ] Slug sem stop words e sem data
- [ ] Yoast verde em SEO + Legibilidade
- [ ] Imagem WebP < 120KB com alt-text preenchido
- [ ] Data de publicação: terça ou quinta, 09h00
- [ ] URL submetida no GSC para indexação
- [ ] Quadro Notion actualizado com URL final
- [ ] Partilha LinkedIn publicada

### Exceptions
- **Yoast não fica verde após 3 tentativas** → publicar com amarelo, criar tarefa
  no Notion "Optimização pendente — [título]", revisão em 7 dias
- **GSC "URL não pode ser indexada" (bloqueio robots.txt)** → escala para Hélder
  em < 2h via WhatsApp, não publicar até resolver
- **Ana Ribeiro ausente e artigo tem deadline** → Miguel Sousa tem autorização
  para publicar após confirmar checklist completa; notifica Ana por email
- **Instagram Stories falha (conta bloqueada ou API down)** → regista em
  Notion "Distribuição pendente", repete no dia seguinte

### Tools needed
- WordPress admin: cuidai.pt/wp-admin (credenciais em 1Password → vault "Cuidai")
- Notion: quadro "Editorial Cuidai" (link: notion.so/cuidai/editorial)
- Google Search Console: property cuidai.pt (acesso via conta ana@cuidai.pt)
- Yoast SEO Premium (instalado em cuidai.pt)
- Ahrefs: para verificar volume de keyword antes de decisão de internal links
- Canva / Figma: imagens de capa (template "Blog Cuidai Hero" no Canva Team)

### Save location
`05 - Claude - IA/Outputs/2025-06-11 - Publicação Artigo SEO - SOP.md`
```

---

## Output anti-patterns

- **SOP sem Owner real** — "Account Manager" não é dono de nada; se não há pessoa nomeada, o SOP não existe
- **Steps sem resultado esperado** — "Verificar analytics" não é um step; "Exporta relatório GSC Jun2025 → ficheiro .csv em /Relatórios/" é
- **Checklist com > 9 items** — acima de 9, as pessoas saltam itens; partir em sub-SOPs ou eliminar redundâncias
- **Exceptions section em branco ou com "consult the team"** — os edge cases são exactamente onde os processos falham; são obrigatórios
- **Angle-brackets no output entregue** — `[Client Name]`, `[Date]`, `[Tool]` no documento final significa zero personalização
- **Decision points hipotéticos** — "Se o cliente usar WordPress" numa agência onde 100% dos clientes usam WordPress não é uma decisão, é ruído
- **SOP para processos que mudam semanalmente** — se o processo mudou 3x este mês, escreve uma guideline, não um SOP versionado
- **Steps > 15 sem sub-SOPs** — um SOP com 18 steps é dois SOPs com identidade crise
- **Version e Review cycle em branco** — um SOP sem data de revisão é documentação que apodrece; define sempre próxima revisão no header
- **Tools listadas sem localização das credenciais** — "usar 1Password" sem indicar qual vault/entry é inútil em incidente real

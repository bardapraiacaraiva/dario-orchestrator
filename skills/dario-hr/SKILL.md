---
name: dario-hr
description: "HR & team management for agencies — job descriptions, capacity planning, onboarding SOPs, performance reviews, freelancer management, training plans, team culture, hiring workflows. Triggers on: 'contratar', 'hire', 'job description', 'vaga', 'capacity', 'equipa', 'team', 'onboarding colaborador', 'performance review', 'freelancer', 'formacao', 'training'."
license: MIT
---

# DARIO HR — Team & Talent Management

## When to activate

- Need to hire (job description, screening criteria)
- Capacity planning (can we take more projects?)
- Onboarding new team member or freelancer
- Performance review cycle
- Training/upskill plan
- Freelancer management (finding, contracting, quality)
- Team structure redesign

## Modules

### 1. Job Description Generator

Input: role, seniority, skills needed, remote/hybrid/office
Output: Complete JD with:

- Title + department
- Mission (1 sentence)
- Responsibilities (5-8 bullets)
- Requirements (must-have vs nice-to-have)
- Tech stack / tools
- What we offer (benefits, growth, culture)
- Salary range indication (PT market 2026 benchmarks)
- Application process

**Agency-specific roles:**
| Role | Salary Range PT 2026 | Key Skills |
|---|---|---|
| Junior Web Developer | 1.200-1.600 EUR | HTML/CSS, WordPress, basic JS |
| Mid Developer | 1.800-2.500 EUR | React/Next.js, PHP, APIs |
| Senior Developer | 2.800-4.000 EUR | Architecture, DevOps, mentoring |
| SEO Specialist | 1.400-2.200 EUR | GSC, GA4, technical SEO, content |
| Content Writer | 1.000-1.600 EUR | Blog, social, SEO writing, PT+EN |
| Designer | 1.500-2.500 EUR | Figma, brand, UI/UX, motion |
| Project Manager | 2.000-3.000 EUR | Agile, client comms, scope |
| Account Manager | 1.800-2.800 EUR | Client relations, upsell, retention |

### 2. Capacity Planning

```markdown
## Capacity Report — [Mes]

### Team
| Membro | Role | Horas/semana | Projectos activos | Utilizacao |
|---|---|---|---|---|
| [Nome] | Developer | 40h | 3 (Atrium, Vivenda, LUCAS) | 85% |
| [Nome] | SEO | 40h | 2 (Atrium, Dog Care) | 60% |
| [Nome] | Designer | 20h (freelancer) | 1 (Vivenda) | 50% |

### Capacidade disponivel
| Role | Horas livres/semana | Pode absorver |
|---|---|---|
| Developer | 6h | 0.5 projecto pequeno |
| SEO | 16h | 1 projecto medio |
| Designer | 10h | 1 projecto pequeno |

### Conclusao
- Developers: FULL — proximo projecto precisa de contratacao ou freelancer
- SEO: 40% livre — pode aceitar mais 1 cliente
- Design: 50% livre — pode aceitar mais 1 projecto

### Recomendacao
- Contratar freelancer developer para proximos 2 meses (peak season)
- SEO pode absorver novo cliente sem risco
```

### 3. Onboarding SOP (novo colaborador)

**Dia 1:**
- [ ] Criar email company
- [ ] Adicionar a Slack/Teams
- [ ] Acesso ao gestor de projectos (Notion/Linear/Asana)
- [ ] Acesso ao repositorio Git
- [ ] Acesso ao hosting/staging
- [ ] Acesso ao Google Workspace / GA4 / GSC
- [ ] Enviar employee handbook
- [ ] Meeting com manager (expectativas, 90-day plan)

**Semana 1:**
- [ ] Tour dos projectos activos
- [ ] Pair programming/trabalho acompanhado
- [ ] Apresentacao aos clientes relevantes
- [ ] Definir objectivos do primeiro mes

**Mes 1:**
- [ ] Review semanal com manager (30min)
- [ ] Primeiro deliverable autonomo
- [ ] Feedback 360 (manager + pares)

**Mes 3 (fim periodo experimental):**
- [ ] Performance review formal
- [ ] Decisao: continuacao / ajuste / fim

### 4. Performance Review Template

```markdown
## Performance Review — [Nome] — [Periodo]

### Objectivos do periodo
| Objectivo | Meta | Resultado | Score |
|---|---|---|---|
| Entregar redesign Vivenda | Ate 31/03 | Entregue 28/03 | 100% |
| Reduzir LCP para <2s em 3 sites | 3 sites | 2 de 3 | 67% |
| Mentor junior developer | 4h/semana | Media 3h/semana | 75% |

### Competencias (1-5)
| Competencia | Score | Notas |
|---|---|---|
| Qualidade tecnica | 4 | Codigo limpo, boas practices |
| Comunicacao | 3 | Precisa melhorar updates ao cliente |
| Autonomia | 4 | Resolve problemas sozinho |
| Colaboracao | 4 | Bom teamwork |
| Crescimento | 5 | Aprendeu React Server Components este Q |

### Feedback qualitativo
**Pontos fortes:** ...
**Areas de melhoria:** ...
**Objectivos proximo periodo:** ...

### Compensacao
- Actual: X EUR
- Proposta: Y EUR (justificacao: ...)
- Proxima revisao: [data]
```

### 5. Freelancer Management

**Base de dados de freelancers:**
```yaml
freelancers:
  - name: "[Nome]"
    specialty: "WordPress Development"
    rate: "35 EUR/h"
    availability: "20h/semana"
    quality_score: 88  # LUCAS quality integration
    projects_completed: 5
    avg_delivery_time: "within deadline"
    contact: "[email]"
    nif: "[NIF]"
    contract: "active"  # active | expired | blacklisted
    notes: "Excelente em custom themes. Fraco em WooCommerce checkout."
```

### 6. Training Plan Generator

Input: role + skill gaps
Output:
- Learning path (cursos, certificacoes, recursos)
- Timeline (semanas)
- Budget estimado
- Metricas de sucesso (como medir se aprendeu)

## Integration Points

- **lucas-finance** → Salarios e pagamentos freelancers entram no P&L
- **dario-legal** → Contratos de trabalho/freelancer
- **lucas-analytics** → Capacity data para workforce planning
- **dario-sop** → SOPs operacionais que novas contratacoes precisam

## Red Flags

- NUNCA aconselhar sobre despedimentos sem remeter para advogado laboral
- Sempre respeitar Codigo do Trabalho PT para prazos, avisos, direitos
- Salarios sao estimativas de mercado — confirmar com recruiter
- Performance reviews devem ser bidirecionais (manager e colaborador)

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Job Description tem salary range PT 2026 + processo concreto

- [ ] Salary range usa benchmarks da tabela (não "a combinar" ou valores genéricos)
- [ ] Must-have vs nice-to-have separados explicitamente (não lista única)
- [ ] Processo de candidatura com steps concretos (e.g., "enviar CV + portfolio para jobs@cuidai.pt")
- [ ] Benefícios listados (remote days, formação, etc.) — não campo vazio
- [ ] Tech stack alinhado com stack real do cliente (não stack genérica)

❌ NOT delivery-ready: "Salário competitivo. Enviar candidatura para o email da empresa."
✅ Delivery-ready: "1.800–2.500 EUR/mês. Stack: React, Next.js, WordPress. Enviar CV + 2 exemplos de trabalho para recrutamento@atrium.pt até 30 Jun 2026."

---

### Gate 2 — Capacity Report tem números reais (nomes, projectos, % utilização)

- [ ] Cada membro tem nome real + role + horas/semana + projectos activos nomeados
- [ ] % utilização calculada (horas projectos / horas disponíveis × 100)
- [ ] "Horas livres" derivadas de dados concretos — não estimativas vagas
- [ ] Conclusão diz EXPLICITAMENTE o que pode ser aceite e o que está bloqueado
- [ ] Recomendação tem acção específica com prazo (freelancer, contratação, redistribuição)

❌ NOT delivery-ready: "Developer está bastante ocupado. Considerar contratar mais recursos."
✅ Delivery-ready: "Miguel (Dev, 40h/sem): projectos Cuidai + Vivenda + ARRECADA = 38h/sem alocados → 95% utilização. FULL. Próximo projecto requer freelancer ou contratação até Ago 2026."

---

### Gate 3 — Onboarding SOP tem datas/responsáveis/sistemas reais do cliente

- [ ] Cada checklist item tem responsável designado (não "alguém do IT")
- [ ] Ferramentas nomeadas com nomes reais (Notion, Linear, Slack — não "gestor de projectos")
- [ ] 90-day plan tem marcos com datas concretas (não "no primeiro mês")
- [ ] Primeiro deliverable autónomo definido explicitamente
- [ ] Review do fim do período experimental tem data fixa agendada

❌ NOT delivery-ready: "Dar acesso às ferramentas. Agendar reunião com o manager."
✅ Delivery-ready: "Dia 1 (02 Jun): Ana (PM) cria email joao@pupli.pt, adiciona ao Slack #dev e ao Linear workspace. Meeting 10h com Rui (CTO) — 90-day plan doc partilhado."

---

### Gate 4 — Performance Review tem scores calculados + compensação justificada

- [ ] Objectivos têm meta mensurável E resultado real (não "bom trabalho")
- [ ] Score % calculado por objectivo + média geral derivada
- [ ] Competências 1–5 com nota qualitativa específica (não score só)
- [ ] Proposta de compensação tem delta e justificação (não "aumento a considerar")
- [ ] Próxima revisão tem data fixa

❌ NOT delivery-ready: "Colaborador tem bom desempenho. Score geral: 4/5. Aumento possível."
✅ Delivery-ready: "Objectivos: média 80.7%. Competências: média 4.0/5. Actual: 2.200 EUR → Proposta: 2.400 EUR (+200 EUR, justificação: entrega Vivenda adiantada + React Server Components certificado). Próxima revisão: Dez 2026."

---

### Gate 5 — Freelancer record tem dados contratuais completos + quality score

- [ ] Rate EUR/h explícito + disponibilidade semanal real
- [ ] NIF / estado contrato (active / expired / blacklisted) preenchido
- [ ] Quality score numérico (0–100) com base em projectos completados
- [ ] Notas de uso incluem pontos fortes E fraquezas específicas
- [ ] Histórico de projectos nomeados (não "vários projectos anteriores")

❌ NOT delivery-ready: "Freelancer de WordPress disponível. Bom trabalho em geral. Contactar se necessário."
✅ Delivery-ready: "Carlos Matos | WordPress Dev | 35 EUR/h | 20h/sem | NIF 234567890 | Quality: 88/100 | 5 projectos (Cuidai, Lisbon Dog Care, LUCAS, Vivenda, ARRECADA) | Forte em custom themes, fraco em WooCommerce checkout avançado."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero angle-brackets `< >`

- [ ] Nenhum `[Nome]`, `[Periodo]`, `[email]`, `[data]` por preencher no output final
- [ ] Cliente identificado em header/título (Cuidai, Atrium, Pupli, etc.)
- [ ] Todos os campos de compensação, datas e ferramentas têm valores concretos
- [ ] Nenhum "X EUR" ou "Y EUR" sem valores substituídos
- [ ] Output pode ser enviado directamente ao cliente sem edição adicional

❌ NOT delivery-ready: "## Performance Review — [Nome] — [Periodo] | Actual: X EUR → Proposta: Y EUR"
✅ Delivery-ready: "## Performance Review — Sofia Rodrigues — Q1 2026 (Jan–Mar) | Actual: 1.800 EUR → Proposta: 2.000 EUR"

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Job Description — Mid Developer | Pupli

**Departamento:** Produto & Engenharia
**Regime:** Remoto (Portugal) | Full-time
**Data abertura:** 02 Jun 2026 | Deadline candidaturas: 30 Jun 2026

---

### Missão
Desenvolver e manter as funcionalidades core da plataforma Pupli,
garantindo performance, escalabilidade e experiência fluida para
tutores e prestadores de serviços de animais.

### Responsabilidades
- Desenvolver features em React/Next.js (App Router) para portal Pupli
- Integrar APIs REST de parceiros (seguradoras, clínicas veterinárias)
- Manter e optimizar base de código WordPress/WooCommerce legado
- Participar em code reviews semanais (Sexta, 10h)
- Colaborar com designer (Figma → código) em novos fluxos de UI
- Monitorizar Core Web Vitals — LCP target <2.0s em produção
- Documentar decisões técnicas no Notion (espaço Engineering)

### Requisitos — Must-Have
- 3+ anos React/Next.js em ambiente de produção
- Experiência com REST APIs e integrações third-party
- WordPress/WooCommerce (manutenção, custom post types)
- Git (GitHub) — PRs, branching, review
- Autonomia: entrega sem micro-gestão

### Requisitos — Nice-to-Have
- Experiência com Vercel / Cloudflare deployment
- Noções de GA4 e Core Web Vitals
- Experiência em startup ou produto SaaS
- Inglês técnico (documentação, dependências)

### Stack Pupli 2026
React 18 · Next.js 14 (App Router) · TypeScript · WordPress 6.5
WooCommerce · MySQL · Vercel · GitHub · Figma · Notion · Slack

### O que oferecemos
- Salário: 2.000–2.400 EUR/mês (consoante experiência)
- Revisão salarial anual (próxima: Jun 2027)
- Remoto 100% — equipamento fornecido (MacBook Air M3)
- Orçamento formação: 500 EUR/ano (cursos, conferências)
- 22 dias férias + feriados PT
- Team day presencial trimestral (Lisboa)

### Processo
1. Candidatura: CV + 2 links de projectos → jobs@pupli.pt
2. Screening call 30min (Ana Ferreira, PM) — até 5 Jul 2026
3. Teste técnico assíncrono (3h, pago 150 EUR) — semana 6 Jul
4. Final interview com CTO (Rui Costa, 1h) — semana 14 Jul
5. Oferta e onboarding previsto: 04 Ago 2026

---

## Capacity Report — Pupli — Jun 2026

| Membro         | Role          | Horas/sem | Projectos activos              | Utilização |
|----------------|---------------|-----------|--------------------------------|------------|
| Rui Costa      | Senior Dev    | 40h       | Pupli core (28h) + reviews (4h)| 80%        |
| Marta Lopes    | Mid Developer | 40h       | Pupli integr. (36h)            | 90%        |
| Carlos Matos   | Dev Freelancer| 20h       | WooCommerce legado (18h)       | 90%        |
| Sofia Rodrigues| Designer      | 40h       | Pupli UI (24h) + Atrium (8h)  | 80%        |
| Ana Ferreira   | PM            | 40h       | Pupli (20h) + Cuidai (14h)    | 85%        |

| Role         | Horas livres/sem | Pode absorver                    |
|--------------|------------------|----------------------------------|
| Senior Dev   | 8h               | Suporte técnico 1 cliente pequeno|
| Mid Dev      | 4h               | NADA — risco burnout             |
| Dev Freelance| 2h               | NADA                             |
| Design       | 8h               | 1 projecto pequeno               |
| PM           | 6h               | 0.5 projecto médio               |

**Conclusão:**
- Dev capacity: CRÍTICA — Marta a 90%, Carlos a 90%
- Design + PM: margem para 1 projecto adicional pequeno
- SEO: sem recurso alocado — bottleneck identificado

**Recomendação:**
- Contratar Mid Developer (JD activa, onboarding 04 Ago 2026)
- Não aceitar novos projectos dev até Ago 2026
- Pupli pode aceitar 1 cliente de design até Jul 2026 sem risco
```

---

## Output anti-patterns

- Salary range genérico ("a combinar", "competitivo") em vez de EUR/mês com fonte PT 2026
- Onboarding SOP sem responsável por cada acção — lista flutuante sem dono
- Performance review com scores sem cálculo explícito (média vaga, não derivada dos dados)
- Capacity report com % de utilização não calculada (estimativa "parece ocupado")
- Freelancer record sem NIF, rate EUR/h, ou estado de contrato — não accionável para pagamento
- JD com "enviar para o email da empresa" em vez de endereço concreto + deadline
- Training plan sem budget estimado e sem métrica de sucesso mensurável
- Placeholder `[Nome]`, `[data]`, `[X EUR]` sobreviventes no output final
- Aviso de despedimento ou conselho laboral directo sem remissão para advogado laboral PT
- Objectivos de performance sem resultado real documentado — só meta sem medição

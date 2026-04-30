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

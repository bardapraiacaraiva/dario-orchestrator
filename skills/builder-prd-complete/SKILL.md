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

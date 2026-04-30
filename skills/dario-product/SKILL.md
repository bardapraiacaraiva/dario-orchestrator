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

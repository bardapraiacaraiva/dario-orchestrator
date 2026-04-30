---
name: client-education
description: "C.L.I.E.N.T. Customer Education — academy design, documentation, webinars, certification programs, and self-service enablement"
version: "1.0"
agent: CLIENT
tags: [education, academy, documentation, webinars, certification, training, enablement]
---

# CLIENT Customer Education Skill

## Triggers

Activate this skill when the user says or implies:
- "customer education", "training program", "customer academy"
- "documentation", "help docs", "user guides"
- "webinar", "educational webinar", "training webinar"
- "certification", "certification program", "credentialing"
- "self-service", "enablement", "product training"
- "learning path", "onboarding training", "knowledge gap"

## Workflow

### Step 1 — Education Needs Assessment
1. **Audience Segmentation**
   - New users (onboarding essentials)
   - Regular users (feature mastery, efficiency tips)
   - Power users (advanced workflows, integrations, API)
   - Admins (configuration, governance, reporting)
   - Executives (dashboards, ROI, strategic use)
2. **Knowledge Gap Analysis**
   - Survey users on confidence levels per feature
   - Analyze support tickets for recurring how-to questions
   - Review feature adoption data (low-adoption = education opportunity)
   - Interview CSMs for common customer struggles
3. **Learning Objectives**
   - Map each audience to specific competencies needed
   - Define measurable outcomes (can do X after completing Y)
   - Prioritize by impact on adoption and retention

### Step 2 — Academy Architecture
1. **Platform Selection**
   - LMS options: Thinkific, Teachable, Skilljar, Docebo, custom
   - Consider: SSO integration, progress tracking, certifications, analytics
2. **Course Structure**
   - **Level 1 — Foundations**: Product basics, core workflows, getting started
   - **Level 2 — Practitioner**: Feature deep dives, best practices, templates
   - **Level 3 — Expert**: Advanced config, integrations, API, automation
   - **Level 4 — Administrator**: Setup, governance, user management, reporting
3. **Content Formats**
   - Video lessons (3-7 min each, screen recordings + talking head)
   - Interactive tutorials (in-app walkthroughs, sandboxes)
   - Written guides with screenshots (step-by-step)
   - Quizzes and knowledge checks
   - Hands-on labs and exercises
   - Downloadable templates and cheat sheets

### Step 3 — Documentation System
1. **Information Architecture**
   - Getting started (quickstart, first steps)
   - Product guides (feature-by-feature documentation)
   - How-to articles (task-based, goal-oriented)
   - Reference docs (API, configuration, data model)
   - Troubleshooting (common issues, error codes)
   - Release notes (what changed, migration guides)
2. **Writing Standards**
   - Plain language, scannable format (headers, bullets, numbered steps)
   - Consistent terminology (maintain glossary)
   - Screenshots updated within 1 sprint of UI changes
   - Every article has: title, summary, steps, related articles, feedback widget
3. **Maintenance Process**
   - Docs reviewed with each product release
   - Stale content flagged via automated checks (>6 months without update)
   - User feedback loop: "Was this helpful?" rating on every page
   - Top search queries with no results = content gap alert

### Step 4 — Webinar Program
1. **Types of Webinars**
   - **Getting Started**: Monthly for new customers
   - **Feature Deep Dive**: Bi-weekly on specific capabilities
   - **Best Practices**: Monthly with customer guest speakers
   - **What's New**: Quarterly product update sessions
   - **Office Hours**: Weekly open Q&A
2. **Production Standards**
   - Professional slides with consistent branding
   - Live demo component (not just slides)
   - Q&A segment (minimum 10 minutes)
   - Recording available within 24 hours
   - Follow-up email with recording, resources, next steps

### Step 5 — Certification Program
1. **Program Design**
   - Prerequisite courses completed
   - Proctored exam (multiple choice + practical scenarios)
   - Passing score: 80%
   - Certificate with name, date, credential ID
   - Renewal requirement: Annual recertification or CE credits
2. **Certification Tiers**
   - Certified User (Level 1-2 courses)
   - Certified Practitioner (Level 2-3 courses + exam)
   - Certified Expert (Level 3-4 courses + advanced exam + project)
3. **Value Proposition**
   - For individuals: Resume credential, LinkedIn badge, career advancement
   - For companies: Proven competency, reduced support needs
   - For vendor: Deeper adoption, stickier product, advocacy pipeline

### Step 6 — Enablement Metrics & Optimization
- Track course completion rates by audience segment
- Correlate education engagement with product adoption
- Measure support ticket reduction after training
- A/B test content formats (video vs. written vs. interactive)
- Collect learner satisfaction scores (post-course survey)

## Commands

```
/client-education academy              — Design full customer academy structure
/client-education docs [product]       — Documentation architecture and standards
/client-education webinar [topic]      — Webinar planning template
/client-education certification        — Certification program design
/client-education path [persona]       — Learning path for a specific persona
/client-education gap-analysis         — Knowledge gap analysis from support data
```

## Output Template

```markdown
# Customer Education Plan: [Product/Company]

## Audience Segments
| Segment | Size | Priority | Key Gaps | Learning Path |
|---------|------|----------|----------|---------------|
| [Segment] | [X] | [H/M/L] | [Gaps] | [Path name] |

## Academy Structure
### Level 1 — Foundations
| Course | Format | Duration | Objective |
|--------|--------|----------|-----------|
| [Course] | [Video/Interactive] | [X min] | [Learner can...] |

### Level 2 — Practitioner
[Same format]

## Webinar Calendar
| Week | Topic | Type | Target Audience | Speaker |
|------|-------|------|-----------------|---------|
| [Week] | [Topic] | [Type] | [Audience] | [Name] |

## Certification Tiers
| Tier | Prerequisites | Exam | Renewal |
|------|---------------|------|---------|
| [Tier] | [Courses] | [Format] | [Cadence] |

## Success Metrics
| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Course completion rate | [X]% | [Y]% | Monthly |
| Support deflection | [X]% | [Y]% | Quarterly |
```

## Red Flags

- Education content not updated after product UI/feature changes
- Courses longer than 60 minutes without breaks or interactive elements
- No tracking of who completed training vs. who needs it
- Documentation with no feedback mechanism (no "was this helpful?")
- Certification exam too easy (>95% pass rate) or too hard (<50% pass rate)
- Webinars with no live demo or Q&A component
- Education program not correlated with product adoption metrics
- Knowledge base search returns no results for common user queries
- Training created without input from support team or CSMs
- Self-service content only in one language when customers are multilingual
- No learning path progression (all content flat, no guided journey)
- Academy launched without promotion plan (if you build it, they won't come)

## Integration Points

- Receives from: `client-onboard` (training needs during onboarding), `client-voc` (feature requests revealing knowledge gaps)
- Feeds into: `client-community` (knowledge base content), `client-health` (training completion as health factor), `client-onboard` (training curriculum)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - CLIENT - Education Plan.md`

## Metrics to Track

- **Course Completion Rate**: Target >70% for enrolled learners
- **Certification Pass Rate**: Target 70-85% (balanced difficulty)
- **Support Deflection**: % reduction in how-to tickets after training
- **Adoption Lift**: Feature adoption increase for trained vs. untrained users
- **Learner Satisfaction**: Post-course NPS or satisfaction score
- **Time to Competency**: Average days from first login to completing Level 1

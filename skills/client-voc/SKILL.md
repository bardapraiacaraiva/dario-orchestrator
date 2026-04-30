---
name: client-voc
description: "C.L.I.E.N.T. Voice of Customer — NPS/CSAT/CES surveys, feedback loops, feature requests, customer advisory board, and closed-loop process"
version: "1.0"
agent: CLIENT
tags: [NPS, CSAT, CES, feedback, voice-of-customer, advisory-board, surveys]
---

# CLIENT Voice of Customer Skill

## Triggers

Activate this skill when the user says or implies:
- "voice of customer", "VoC", "customer feedback"
- "NPS", "Net Promoter Score", "CSAT", "CES"
- "survey", "feedback loop", "customer sentiment"
- "feature request", "product feedback"
- "customer advisory board", "CAB"
- "closed-loop feedback", "listen to customers"

## Workflow

### Step 1 — Survey Program Design
1. **NPS (Net Promoter Score)** — Relationship health
   - Cadence: Quarterly or bi-annually
   - Question: "How likely are you to recommend us?" (0-10)
   - Segments: Promoters (9-10), Passives (7-8), Detractors (0-6)
   - Follow-up: Open-ended "What is the primary reason for your score?"
2. **CSAT (Customer Satisfaction)** — Transactional touchpoints
   - Cadence: After key interactions (support ticket, onboarding, training)
   - Question: "How satisfied were you with [interaction]?" (1-5)
   - Trigger: Automated post-interaction with 24h delay
3. **CES (Customer Effort Score)** — Ease of experience
   - Cadence: After self-service or support interactions
   - Question: "How easy was it to [complete task]?" (1-7)
   - Focus: Identify high-friction moments in the journey

### Step 2 — Feedback Collection Channels
- In-app surveys (microsurveys, NPS widget)
- Email surveys (post-interaction, periodic)
- Support ticket analysis (sentiment, topics)
- Sales call notes and objection logs
- Social media and review sites monitoring
- Customer advisory board sessions
- User community forums and discussions
- QBR feedback and success plan reviews

### Step 3 — Feature Request Management
1. **Capture**: Standardized intake form (requester, use case, business impact, urgency)
2. **Classify**: Category, product area, effort estimate, strategic alignment
3. **Prioritize**: RICE score (Reach x Impact x Confidence / Effort)
4. **Communicate**: Status updates to requesters (received, under review, planned, shipped, declined)
5. **Close Loop**: Notify requester when feature ships, collect feedback on implementation

### Step 4 — Customer Advisory Board (CAB)
- **Composition**: 8-15 customers across segments, mix of promoters and constructive critics
- **Cadence**: Quarterly meetings (2h), annual in-person summit
- **Agenda**: Product roadmap preview, feedback workshops, strategic direction input
- **Governance**: NDA, term limits (2 years), rotation schedule
- **Value Exchange**: Early access to features, executive access, recognition, input on direction

### Step 5 — Closed-Loop Process
1. **Listen**: Collect feedback through all channels
2. **Analyze**: Aggregate themes, sentiment trends, segment patterns
3. **Act**: Route insights to product, support, CS, marketing teams
4. **Follow Up**: Contact respondents with actions taken ("You said X, we did Y")
5. **Measure**: Track impact of changes on subsequent scores

### Step 6 — Reporting & Insights
- Monthly VoC digest: NPS trend, top themes, sentiment shift
- Quarterly deep dive: Segment analysis, cohort comparison, driver analysis
- Annual benchmarking: Industry comparison, year-over-year trends
- Real-time alerts: Detractor responses, critical feedback, viral complaints

## Commands

```
/client-voc program                   — Design full VoC survey program
/client-voc nps [period]              — NPS analysis with driver breakdown
/client-voc feedback [company]        — Consolidated feedback view for account
/client-voc features                  — Feature request backlog with RICE scores
/client-voc cab                       — Customer advisory board planning guide
/client-voc closed-loop [theme]       — Generate closed-loop follow-up for a theme
```

## Output Template

```markdown
# Voice of Customer Report: [Period]

## NPS Summary
- **Score**: [XX] (Previous: [XX], Delta: [+/-X])
- **Responses**: [X] ([X]% response rate)
- **Promoters**: [X]% | **Passives**: [X]% | **Detractors**: [X]%

## Top Themes (by frequency)
| Theme | Mentions | Sentiment | Trend | Action Owner |
|-------|----------|-----------|-------|-------------|
| [Theme 1] | [X] | [Pos/Neg/Mixed] | [up/down] | [Team] |
| [Theme 2] | [X] | [Pos/Neg/Mixed] | [up/down] | [Team] |

## Feature Requests (Top 5 by RICE)
| Feature | RICE Score | Requests | Status |
|---------|------------|----------|--------|
| [Feature] | [XX] | [X] | [Status] |

## Detractor Follow-Up Log
| Customer | Score | Reason | Follow-Up | Resolved |
|----------|-------|--------|-----------|----------|
| [Name] | [X] | [Reason] | [Action] | [Y/N] |

## Closed-Loop Actions Taken
1. [You said X] → [We did Y] → [Impact Z]
```

## Red Flags

- NPS survey response rate below 20% (insufficient sample)
- Detractor responses not followed up within 5 business days
- No closed-loop process (feedback collected but never actioned)
- Feature requests backlog growing with no status updates to requesters
- Customer advisory board with only promoters (no constructive critics)
- Survey fatigue — sending too many surveys to the same contacts
- NPS declining for 2+ consecutive quarters without root cause analysis
- VoC insights not shared with product team in any structured way
- CSAT/CES measured but no one owns the improvement actions
- Feedback themes repeat quarter after quarter with no visible progress
- Customer gives low score but CSM marks it as "resolved" without real action

## Integration Points

- Feeds into: `client-health` (NPS/CSAT as health dimension), `client-renewal` (sentiment before renewal), `client-recovery` (detractor save)
- Receives from: `client-qbr` (QBR feedback), `client-community` (forum sentiment), `client-education` (training feedback)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - CLIENT - VoC Report.md`

## Metrics to Track

- **NPS Score**: Quarterly trend, by segment, by tenure cohort
- **CSAT Average**: By touchpoint type, trend over time
- **CES Average**: By journey stage, trend over time
- **Response Rate**: Target >30% for NPS, >40% for transactional
- **Closed-Loop Rate**: % of detractor responses with follow-up action completed
- **Feature Request Cycle Time**: Average days from request to status update

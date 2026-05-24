---
name: client-community
description: "C.L.I.E.N.T. Community Management — forums, user groups, events, ambassador programs, knowledge base, and peer support networks"
version: "1.0"
agent: CLIENT
tags: [community, forums, user-groups, ambassador, events, peer-support, knowledge-base]
---

# CLIENT Community Management Skill

## Triggers

Activate this skill when the user says or implies:
- "community", "user community", "customer community"
- "forum", "discussion board", "user group"
- "ambassador program", "champion program", "advocate"
- "customer events", "meetups", "user conference"
- "knowledge base", "help center", "self-service"
- "peer support", "community engagement"

## Workflow

### Step 1 — Community Strategy Design
1. **Purpose Definition**: Why does this community exist?
   - Peer support (reduce support tickets)
   - Knowledge sharing (best practices, use cases)
   - Product feedback (ideas, beta testing)
   - Networking (industry connections)
   - Brand advocacy (organic growth)
2. **Platform Selection**
   - Hosted forum (Discourse, Circle, Tribe, Bettermode)
   - Slack/Discord workspace
   - In-app community
   - LinkedIn/Facebook group
   - Hybrid (forum + real-time chat)
3. **Governance Model**
   - Community guidelines and code of conduct
   - Moderation policy (pre/post moderation, escalation)
   - Role hierarchy: Admin > Moderator > Ambassador > Member > New Member
   - Content taxonomy: Categories, tags, pinned resources

### Step 2 — Launch Plan
1. **Pre-Launch (4 weeks)**
   - Seed content: 20+ posts covering FAQs, best practices, how-tos
   - Recruit founding members: 10-20 power users as initial contributors
   - Set up gamification: Points, badges, levels, leaderboards
   - Prepare welcome sequence: Onboarding email, first-post prompt
2. **Launch Week**
   - Invite first cohort (most engaged customers)
   - Host AMA or launch event with product team
   - Daily team engagement (respond to every post within 4 hours)
   - Monitor and fix UX issues in real-time
3. **Post-Launch (ongoing)**
   - Weekly content calendar: themed days, spotlights, challenges
   - Monthly community metrics review
   - Quarterly community health assessment

### Step 3 — Ambassador / Champion Program
1. **Selection Criteria**
   - Active product user (top 10% by engagement)
   - History of helping others (support forums, social media)
   - Positive NPS score (Promoter)
   - Willingness to commit time (2-4 hours/month)
2. **Benefits for Ambassadors**
   - Early access to new features and beta programs
   - Direct line to product team
   - Exclusive events and networking
   - Public recognition (badge, profile highlight, case study)
   - Swag, conference tickets, or monetary incentives
3. **Responsibilities**
   - Answer community questions (minimum X posts/month)
   - Create content (blog posts, tutorials, videos)
   - Provide product feedback and participate in CAB
   - Refer new customers or speak at events

### Step 4 — Event Program
- **Webinars**: Monthly educational sessions (product tips, industry trends)
- **User Groups**: Regional or industry-specific meetups (quarterly)
- **Annual Conference**: Flagship event with keynotes, workshops, networking
- **Office Hours**: Weekly open session with product/CS team
- **Hackathons**: Community-driven innovation events

### Step 5 — Knowledge Base & Self-Service
1. **Content Architecture**
   - Getting started guides
   - Feature documentation with screenshots/videos
   - FAQ by category
   - Troubleshooting guides
   - API documentation (if applicable)
   - Community-contributed templates and recipes
2. **Maintenance Cadence**
   - Review and update articles monthly
   - Archive outdated content
   - Track search queries with no results (content gaps)
   - Version articles for product releases

### Step 6 — Community Health Metrics
- **Engagement**: DAU/MAU, posts per day, response rate
- **Growth**: New members, activation rate, retention rate
- **Support Deflection**: % of questions answered by community (not staff)
- **Content**: User-generated vs. staff-generated ratio
- **Sentiment**: Positive/negative post ratio, flagged content volume
- **Ambassador Impact**: Posts answered, content created, referrals generated

## Commands

```
/client-community strategy             — Design community strategy from scratch
/client-community launch               — Generate community launch plan
/client-community ambassador           — Design ambassador/champion program
/client-community events               — Event program planning
/client-community kb                   — Knowledge base architecture and content plan
/client-community health               — Community health metrics dashboard
```

## Output Template

```markdown
# Community Strategy: [Product/Company Name]

## Mission
[One sentence: why this community exists]

## Platform & Governance
- **Platform**: [Selection with rationale]
- **Governance**: [Model summary]
- **Moderation**: [Policy summary]

## Launch Plan
| Phase | Timeline | Key Actions | Success Metric |
|-------|----------|-------------|----------------|
| Pre-Launch | Weeks 1-4 | [Actions] | [Metric] |
| Launch | Week 5 | [Actions] | [Metric] |
| Growth | Months 2-6 | [Actions] | [Metric] |

## Ambassador Program
- **Criteria**: [Selection rules]
- **Benefits**: [Value proposition]
- **Capacity**: [Target number of ambassadors]
- **Launch**: [Timeline]

## Event Calendar
| Event Type | Frequency | Format | Target Audience |
|------------|-----------|--------|-----------------|
| [Event] | [Cadence] | [Live/Virtual] | [Audience] |

## Health Metrics (Targets)
| Metric | Month 1 | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|---------|----------|
| Members | [X] | [X] | [X] | [X] |
| DAU/MAU | [X]% | [X]% | [X]% | [X]% |
| Support Deflection | [X]% | [X]% | [X]% | [X]% |
```

## Red Flags

- Community launched without seed content (empty forum syndrome)
- No staff engagement in first 30 days (community feels abandoned)
- Response time to community posts exceeds 24 hours consistently
- Ambassador program without clear value exchange (exploitative)
- Community guidelines not enforced (toxic behavior unchecked)
- Knowledge base articles outdated by >6 months
- Community used only as support channel (no engagement or networking value)
- No moderation process for spam, self-promotion, or inappropriate content
- Events with <10% attendance of invited audience
- Community metrics not tracked or reviewed regularly
- User-generated content not surfaced or recognized
- Community platform chosen without considering customer preferences

## Integration Points

- Receives from: `client-voc` (community sentiment as feedback channel), `client-education` (training content for KB)
- Feeds into: `client-health` (engagement as health signal), `client-expansion` (ambassador referrals), `client-voc` (community as feedback source)
- Outputs to: Obsidian `05 - Claude - IA/Outputs/` with naming `YYYY-MM-DD - CLIENT - Community Strategy.md`

## Metrics to Track

- **Community Growth Rate**: New members per month, trend
- **Engagement Rate**: DAU/MAU ratio, target >15%
- **Support Deflection Rate**: % of support queries resolved by community, target >30%
- **Time to First Response**: Average hours for community post to get a reply
- **Ambassador Activity**: Posts, content, referrals per ambassador per month
- **Content Coverage**: % of product features covered in knowledge base


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **client-community** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in client-community:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->

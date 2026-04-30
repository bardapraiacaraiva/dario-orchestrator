---
name: dario-make-blueprint
description: Make.com automation scenario planner — generates module list, triggers, data mappings, error handlers, and test plan for no-code integrations. Triggers on "make", "automação", "make.com", "zapier alternative", "integromat", "cenário make", "scenario".
license: MIT
---

# DARIO Skill — Make.com Automation Blueprint

Designs automation scenarios for Make.com (or transferable to Zapier / n8n). Outputs a blueprint specific enough to implement directly: modules in order, data mappings, error handling, and test cases.

## When to activate

- Client has repetitive manual work between tools
- New integration project (e.g. form → CRM → email → slack)
- Client wants to replace a paid SaaS with Make workflows
- Before quoting automation hours (the blueprint = estimate)

## Workflow

### 1. Gather inputs
- **Trigger event** (what starts the flow)
- **Tools involved** (list all SaaS in the path)
- **End goal** (what successful completion looks like)
- **Data payload** (what fields need to flow)
- **Frequency** (daily batch, real-time, weekly)
- **Error tolerance** (can it fail silently? or must alert?)
- **Budget** (Make operations quota)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "make automation scenario design", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "webhook integration best practices", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "rgpd automation data flow consent", collection: "dario", limit: 5)
```

### 3. Architecture design

#### Identify the trigger
- **Webhook** (real-time, best for instant reactions)
- **Polling** (every N min, cheap but delayed)
- **Schedule** (batch at fixed time)
- **App-native** (Gmail, Sheets, Airtable — 1 op per check)

#### Map the flow (Make lingo)
```
[Trigger]
  ↓
[Module 1: Router/Filter] — conditional logic
  ↓ (branch A)
[Module 2: HTTP request] — API call
  ↓
[Module 3: Data store] — upsert record
  ↓
[Module 4: Notification]
```

#### Apply best practices
- **Error handler** on every critical module (Break, Resume, Commit/Rollback)
- **Sleep** module when hitting rate-limited APIs
- **Aggregator + Iterator** for bulk operations (1 op per batch, not 1 per item)
- **Data store** for idempotency (don't double-process)
- **Router** for conditional flows (cheaper than multiple scenarios)
- **Webhook response** to acknowledge source (don't leave hanging)
- **Log module** (to Sheets or similar) for audit trail

### 4. Op count budget estimate

Make charges per module execution ("op"). Estimate:
- Simple flow (trigger → 3 modules): 4 ops per run
- With router (2 branches): 5-7 ops per run
- With iterator over 10 items: 10 + 3*10 = 40 ops

Monthly: `runs_per_day × 30 × ops_per_run`. Make Core plan = 10K ops/month.

### 5. Error handling pattern

Every critical module should have:
```
[Module] → [Error handler]
              ├── Break (stop scenario)
              ├── Resume (continue with default values)
              ├── Commit (mark success)
              └── Rollback (undo changes)
```

Plus a "tail" error branch that sends a Slack/email alert with scenario ID + error text.

### 6. Data mapping discipline

For each field:
- **Source field** (where it comes from)
- **Transformation** (format date, slug, lowercase, etc.)
- **Target field** (where it goes)
- **Default if missing**
- **Validation rule**

Document as a table — this becomes the spec for the person implementing.

### 7. Test plan

For each scenario:
- **Happy path test** — ideal input, verify end-to-end
- **Missing field test** — required fields absent
- **Duplicate test** — idempotency check
- **API failure test** — what happens if target is down
- **Rate limit test** — many runs in short window
- **Rollback test** — if midway fail, is state clean

### 8. Operations budget + monitoring

Recommend:
- **Make built-in history** (keep 14 days)
- **External logging** (Google Sheet with run ID, timestamp, result)
- **Weekly op review** (are we near quota?)

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: make-blueprint
scenario_name: <name>
trigger: <type>
monthly_ops_estimate: N
---

# Make Blueprint — <Scenario Name>

## Goal
<1-2 sentences>

## Trigger
- Type: webhook | polling | schedule
- Source: <app>
- Detail: <config>

## Flow Diagram
```
[Trigger: Webhook "form submit"]
  ↓
[Filter: email is valid]
  ↓
[HTTP: POST /api/crm/contacts]
  ↓
[Router]
  ├── (new) → [Send welcome email via SendGrid]
  └── (existing) → [Add tag via Airtable]
  ↓
[Log to Google Sheets]
```

## Module Specification

### Module 1: <Name>
- **Type:** <app + action>
- **Config:**
  - field_a: `{{1.value}}`
  - field_b: static
- **Error handler:** Break + alert

### Module 2: <Name>
...

## Data Mapping
| Source | Transform | Target | Default | Required |
|---|---|---|---|---|
| form.email | lowercase | crm.email | — | yes |
| form.name | split " " | crm.first_name | "" | no |

## Error Handling
- Critical modules: ...
- Alerts: Slack #automations
- Retry logic: 3x with 1min delay

## Test Plan
- [ ] Happy path
- [ ] Missing email
- [ ] Duplicate submission (idempotency)
- [ ] CRM API down
- [ ] Rate limit

## Op Count Estimate
- Per run: X ops
- Daily runs: Y
- Monthly: Y × 30 × X = Z ops
- Budget headroom: (10K - Z) ops = __%

## Deploy Checklist
- [ ] Scenario imported
- [ ] API credentials stored in Make connections (not hardcoded)
- [ ] Webhook URL shared with source app
- [ ] Error alert channel configured
- [ ] Test data sent + validated
- [ ] Live monitoring for 48h

## Handover
- Make URL: https://eu1.make.com/...
- Documentation: link to this file
- Runbook: what to do if it fails
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Make Blueprint - <Scenario>.md`

## Red flags
- Hardcoded credentials (use Make Connections)
- No error handlers (silent failures)
- No idempotency (duplicate processing)
- Iterator without aggregator (op cost explodes)
- No test data in dev before production
- Webhook with no retry logic on source
- Sensitive data in logs (GDPR leak)
- Unbounded loops
- Sending tracking data without RGPD consent

## Interactions
- Check `spec/pt-legal-compliance` for RGPD-sensitive flows
- Save via `dario-obsidian-save`
- Part of `dario-client-onboard` for clients needing automation

## Red Flags
- Never build a scenario without error handlers on every critical module — silent failures in production mean lost data, missed leads, and hours of debugging with no audit trail
- Never skip the test plan (happy path, missing fields, duplicate, API failure) — untested automations break on the first edge case and erode client trust immediately
- Always document webhook URLs and share them in the blueprint handover — undocumented webhook endpoints become orphaned when the original builder is unavailable
- Never hardcode API credentials in module configs — use Make Connections for all auth; hardcoded keys are a security risk and break when rotated
- Always estimate monthly ops budget before going live — an unbounded iterator can burn through an entire Make plan quota in a single run

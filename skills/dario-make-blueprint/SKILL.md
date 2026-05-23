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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Trigger está completamente especificado
- [ ] Tipo de trigger identificado (webhook / polling / schedule / app-native)
- [ ] Source app nomeada com endpoint ou URL real (não genérico)
- [ ] Frequência ou evento exacto descrito (ex: "submissão do Typeform ID abc123", não "quando há formulário")
- [ ] Webhook response configurada (não deixar o source a aguardar)

❌ NOT delivery-ready: `Trigger: webhook — configurar depois`
✅ Delivery-ready: `Trigger: Webhook POST de Typeform (form ID: 8xKz3p) → URL Make eu1.make.com/hook/xyz, responde 200 em < 2s`

---

### Gate 2 — Flow Diagram tem todos os módulos na ordem correcta
- [ ] Cada módulo listado com número, nome e tipo Make real (ex: "HTTP > Make a request", não "chamada API")
- [ ] Routers com ambos os branches documentados (condição A e condição B)
- [ ] Error handler explícito em cada módulo crítico
- [ ] Nenhum módulo vazio ("TBD" ou "configurar depois")

❌ NOT delivery-ready: `Module 3: CRM — inserir contacto`
✅ Delivery-ready: `Module 3: HTTP > Make a request | POST https://api.pipedrive.com/v1/persons | Auth: API Key (Make Connection "Pipedrive-Cuidai-Prod") | Error handler: Break + Slack alert`

---

### Gate 3 — Data Mapping está completo e sem ambiguidade
- [ ] Tabela com todas as colunas: Source, Transform, Target, Default, Required
- [ ] Transformações explícitas (ex: `formatDate(1.submitted_at; "DD/MM/YYYY")`, não "formatar data")
- [ ] Default definido para todos os campos opcionais (nunca em branco na coluna Default)
- [ ] Campos RGPD identificados (email, nome, NIF) com nota de conformidade

❌ NOT delivery-ready: `form.email → crm.email (obrigatório)`
✅ Delivery-ready: `form.email | `toLowerCase(1.email)` | pipedrive.email[0].value | — | yes | ⚠️ RGPD: dados pessoais, só processar com consentimento Cuidai T&C v2`

---

### Gate 4 — Op Count está calculado e cabe no plano Make do cliente
- [ ] Ops por run calculadas com fórmula visível (não estimativa vaga)
- [ ] Runs diárias baseadas em dado real (volume de formulários, clientes, etc.)
- [ ] Total mensal calculado: `runs/dia × 30 × ops/run`
- [ ] Budget headroom declarado em % e em ops absolutas
- [ ] Se > 80% do plano: recomendação de upgrade ou optimização listada

❌ NOT delivery-ready: `Estimativa: ~500 ops/mês — dentro do plano`
✅ Delivery-ready: `7 ops/run × 45 submissões/dia × 30 = 9.450 ops/mês | Plano Core 10K → 5,5% headroom ⚠️ CRÍTICO: recomendar upgrade para Make Pro (40K) antes de go-live`

---

### Gate 5 — Test Plan tem casos concretos e critérios de pass/fail
- [ ] Happy path com payload de teste real (campos preenchidos com dados fictícios mas plausíveis)
- [ ] Duplicate test com método de idempotência documentado (Data Store? campo unique?)
- [ ] API failure test: o que acontece e quem recebe alerta (canal + pessoa nomeada)
- [ ] Todos os testes têm critério explícito de "passou" (não apenas "verificar se funciona")

❌ NOT delivery-ready: `- [ ] Testar happy path`
✅ Delivery-ready: `- [ ] Happy path: submeter email="teste@cuidai.pt", nome="Ana Ferreira" → PASS se registo aparece em Pipedrive < 30s + log em Sheets linha nova com status="success"`

---

### Gate 6 — Output usa CLIENT NAME + dados reais, sem angle-brackets por preencher
- [ ] Nenhum `<client>`, `<app>`, `<name>`, `<config>` visível no output final
- [ ] Make URL real ou placeholder explicitamente marcado como "pendente activação"
- [ ] Credenciais referenciadas pelo nome da Make Connection real (ex: `"Pipedrive-Cuidai-Prod"`)
- [ ] Save location preenchida com cliente, data e nome do cenário reais

❌ NOT delivery-ready: `project: <client> | Slack #<canal-alertas>`
✅ Delivery-ready: `project: Cuidai | date: 2025-06-10 | Slack #automations-cuidai | Make Connection: "ActiveCampaign-Cuidai-Prod"`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: Cuidai
date: 2025-06-10
type: make-blueprint
scenario_name: Nova Candidatura Cuidadora → CRM + Onboarding
trigger: webhook
monthly_ops_estimate: 3.150
---

# Make Blueprint — Nova Candidatura Cuidadora → CRM + Onboarding

## Goal
Quando uma cuidadora submete o formulário Typeform de candidatura, criar perfil no
Pipedrive, enviar email de confirmação via ActiveCampaign e notificar a equipa no Slack
#ops-cuidai — tudo em menos de 30 segundos, sem intervenção manual.

## Trigger
- **Type:** Webhook (real-time)
- **Source:** Typeform — Form ID `8xKz3p` ("Candidatura Cuidadora v3")
- **Detail:** POST → `https://eu1.make.com/hook/abc123xyz` (activar após import)
- **Webhook response:** 200 OK imediato; processamento assíncrono

## Flow Diagram
```
[Trigger: Typeform Webhook — "form_response"]
  ↓
[Filter: email válido + NIF 9 dígitos]
  ↓
[Data Store: check duplicate by NIF]
  ├── (NIF já existe) → [HTTP: PATCH Pipedrive /persons/{id} — add tag "re-candidatura"]
  │                       ↓ [Log Sheets: status="duplicate-updated"]
  └── (NIF novo) → [HTTP: POST Pipedrive /persons — criar pessoa]
                    ↓
                  [HTTP: POST ActiveCampaign /contacts — add to list 14]
                    ↓
                  [ActiveCampaign: add tag "cuidadora-candidata-2025"]
                    ↓
                  [Slack: POST #ops-cuidai — "Nova candidatura: {{nome}}"]
                    ↓
                  [Log Sheets: status="success"]
```

## Module Specification

### Module 1: Typeform — Watch Responses
- **Type:** Typeform > Watch Responses
- **Config:**
  - Form: `8xKz3p — Candidatura Cuidadora v3`
  - Webhook: auto-registado pelo Make
- **Error handler:** n/a (trigger)

### Module 2: Filter — Validação básica
- **Type:** Filter (built-in, 0 ops)
- **Condition A:** `{{1.answers.email}}` contains `@` AND length > 5
- **Condition B:** `{{1.answers.nif}}` matches pattern `[0-9]{9}`
- **Se falhar:** cenário para, log "validation-failed" em Sheets

### Module 3: Data Store — Check Duplicate NIF
- **Type:** Data Store > Search Records
- **Store:** `cuidai-candidaturas-nif` (estrutura: nif:string, pipedrive_id:string, ts:date)
- **Search:** `nif = {{1.answers.nif}}`
- **Error handler:** Break + Slack alert #ops-cuidai

### Module 4a (branch novo): HTTP — POST Pipedrive
- **Type:** HTTP > Make a request
- **Method:** POST `https://api.pipedrive.com/v1/persons`
- **Auth:** Make Connection `"Pipedrive-Cuidai-Prod"` (API Key, nunca hardcoded)
- **Body:**
  ```json
  {
    "name": "{{1.answers.nome}}",
    "email": [{"value": "{{toLowerCase(1.answers.email)}}", "primary": true}],
    "phone": [{"value": "{{1.answers.telemovel}}", "primary": true}],
    "custom_fields": { "nif": "{{1.answers.nif}}", "zona": "{{1.answers.distrito}}" }
  }
  ```
- **Error handler:** Break + Slack alert `"Pipedrive down — candidatura {{1.answers.email}} perdida"`

### Module 5: ActiveCampaign — Add Contact
- **Type:** HTTP > Make a request
- **POST** `https://cuidai.api-us1.com/api/3/contacts`
- **Auth:** Make Connection `"ActiveCampaign-Cuidai-Prod"`
- **Body:** email, firstName, lastName (split de nome), listId: `14`
- **Error handler:** Resume (contacto já existe) — não bloquear flow

### Module 6: Slack — Notificação Equipa
- **Type:** Slack > Create a Message
- **Channel:** `#ops-cuidai`
- **Text:** `✅ Nova candidatura: *{{1.answers.nome}}* ({{1.answers.distrito}}) — Pipedrive ID {{4.id}}`
- **Error handler:** Resume (Slack down não deve parar onboarding)

### Module 7: Google Sheets — Audit Log
- **Type:** Google Sheets > Add a Row
- **Spreadsheet:** `Cuidai — Make Audit Log 2025` | Sheet: `candidaturas`
- **Row:** `run_id={{scenarioId}}, ts={{now}}, email={{1.answers.email}}, nif={{1.answers.nif}}, status="success", pipedrive_id={{4.id}}`
- **Error handler:** Break (log é obrigatório para RGPD audit)

## Data Mapping
| Source | Transform | Target | Default | Required |
|---|---|---|---|---|
| `1.answers.email` | `toLowerCase()` | `pipedrive.email[0].value` | — | yes |
| `1.answers.nome` | `split(" ")[0]` | `ac.firstName` | `"Cuidadora"` | no |
| `1.answers.nome` | `split(" ")[-1]` | `ac.lastName` | `""` | no |
| `1.answers.nif` | nenhuma | `pipedrive.nif` (custom) | — | yes |
| `1.answers.distrito` | `capitalize()` | `pipedrive.zona` (custom) | `"Desconhecido"` | no |
| `1.submitted_at` | `formatDate(;"DD/MM/YYYY HH:mm")` | `sheets.ts` | `now` | yes |

⚠️ **RGPD:** email, nome, NIF e telemóvel são dados pessoais. Processados sob consentimento
expresso (checkbox obrigatória no Typeform campo ID `q_consent`). Retenção: 24 meses.

## Error Handling
- **Módulos críticos:** M3 (Data Store), M4a (Pipedrive), M7 (Log) → Break + alert
- **Módulos tolerantes:** M5 (ActiveCampaign), M6 (Slack) → Resume
- **Canal de alerta:** Slack `#automations-erros-cuidai` com texto:
  `"⚠️ Make Erro — Cenário 'Candidatura Cuidadora' | Módulo: {{moduleName}} | Erro: {{error.message}} | Run: {{scenarioId}}"`
- **Retry:** 3x com 60s delay (configurado em Make > Scenario settings)

## Test Plan
- [ ] **Happy path:** submeter `email="ana.ferreira.teste@cuidai.pt"`, `nif="123456789"`, `nome="Ana Ferreira"`, `distrito="Lisboa"` → PASS se Pipedrive tem nova pessoa + AC lista 14 + Slack mensagem + Sheets linha, tudo < 30s
- [ ] **Email inválido:** submeter `email="naoeumemail"` → PASS se cenário para no Filter, log "validation-failed", SEM registo no CRM
- [ ] **NIF duplicado:** submeter mesmo NIF `123456789` duas vezes → PASS se 2ª run faz PATCH (não POST), sem duplicado no Pipedrive
- [ ] **Pipedrive API down:** mock 500 em Make dev → PASS se Slack #automations-erros-cuidai recebe alerta em < 2min, Sheets log status="error"
- [ ] **Campo distrito vazio:** submeter sem distrito → PASS se `pipedrive.zona = "Desconhecido"` (default aplicado)

## Op Count Estimate
- Por run (branch novo): 7 ops (trigger + filter-free + DS + HTTP×2 + Slack + Sheets)
- Por run (branch duplicado): 5 ops
- Volume: ~15 candidaturas/dia (estimativa Cuidai Q2 2025)
- Mensal: `15 × 30 × 7 = 3.150 ops`
- Plano Make Core (10K): **68,5% headroom** ✅ seguro até ~43 candidaturas/dia

## Deploy Checklist
- [ ] Cenário importado em `eu1.make.com` (conta `ops@cuidai.pt`)
- [ ] Make Connections criadas: `Pipedrive-Cuidai-Prod`, `ActiveCampaign-Cuidai-Prod`, `Google-Cuidai-Prod`
- [ ] Webhook URL enviada a João (Typeform admin): `https://eu1.make.com/hook/abc123xyz`
- [ ] Canal Slack `#automations-erros-cuidai` criado e bot adicionado
- [ ] Data Store `cuidai-candidaturas-nif` criado com estrutura correcta
- [ ] Test data enviado + todos os 5 testes passaram
- [ ] Monitoring activo 48h pós-go-live (Mariana responsável)

## Handover
- **Make URL:** `https://eu1.make.com/org/12345/scenarios/67890` (ativar após testes)
- **Documentação:** `05 - Claude - IA/Outputs/2025-06-10 - Cuidai - Make Blueprint - Candidatura Cuidadora.md`
- **Runbook:** Se cenário falhar → verificar Make History → se Pipedrive down, submissões ficam em fila (retry 3x) → se persistir, contactar Mariana (mariana@cuidai.pt)
```

---

## Output anti-patterns

- **Módulos sem tipo Make real** — escrever "chamada API" em vez de "HTTP > Make a request" ou "Pipedrive > Create a Person" impossibilita implementação directa
- **Data Mapping incompleto** — omitir a coluna "Default" garante erros silenciosos quando campos opcionais chegam vazios
- **Op count sem fórmula** — estimar "poucas ops" sem calcular `runs × ops × 30` deixa cliente sem saber se precisa de upgrade
- **Error handler genérico em todos os módulos como Break** — módulos de notificação (Slack, email) devem ser Resume para não bloquear o flow principal por falha não-crítica
- **Test plan sem critério de pass** — "testar happy path" sem definir o que constitui sucesso não serve de spec para QA
- **Credenciais referenciadas como `<API_KEY>`** — qualquer angle-bracket no output final indica blueprint inacabado; usar sempre o nome da Make Connection
- **Flow diagram sem branches do Router** — mostrar apenas "Router" sem as condições A/B obriga o implementador a adivinhar a lógica de negócio
- **RGPD invisível** — blueprint que flui email/NIF/nome sem nenhuma nota de consentimento ou retenção é risco legal imediato para clientes PT/EU
- **Deploy Checklist sem owner** — itens como "configurar webhook" sem nomear quem faz ficam por fazer no go-live
- **Scenario name genérico** — `scenario_name: automação formulário` em vez de `Nova Candidatura Cuidadora → CRM + Onboarding` dificulta rastreio em contas Make com múltiplos cenários

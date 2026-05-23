---
name: builder-smart-context
description: >
  Seleccao inteligente de contexto para builder skills. Em vez de enviar todo o projecto
  ao LLM, score ficheiros por relevancia e inclui apenas os necessarios. Reduz tokens 60-80%.
  Inspirado em Dyad (8K stars). Use quando: optimizar contexto, reduzir tokens, smart context.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Smart Context Selector (Dyad pattern)

## Proposito
Quando um builder skill precisa de contexto do projecto, NAO enviar tudo.
Score ficheiros por relevancia e incluir apenas os top-N. Savings: 60-80% tokens.

## Como funciona

### 1. Recebe pedido do builder skill
```
Skill: builder-landing-page
Task: "Gerar hero section para SaaS de contabilidade"
```

### 2. Score ficheiros do projecto por relevancia
```
tailwind.config.ts     → 0.95 (design tokens — ESSENTIAL)
package.json           → 0.80 (dependencies — IMPORTANT)
app/layout.tsx         → 0.75 (root layout — IMPORTANT)
components/ui/button.tsx → 0.60 (existing component — RELEVANT)
db/schema.ts           → 0.15 (database — NOT RELEVANT for hero)
lib/auth.ts            → 0.10 (auth — NOT RELEVANT)
```

### 3. Include top-N ate token budget
```
Token budget: 4000 tokens
Include: tailwind.config.ts + package.json + app/layout.tsx + button.tsx
Skip: db/schema.ts, lib/auth.ts (irrelevant to hero section)
Savings: ~70% vs including everything
```

### Scoring Rules
| Factor | Weight | Description |
|---|---|---|
| Filename match | 0.4 | File name contains task keywords |
| Import chain | 0.3 | File is imported by target file |
| Recency | 0.2 | Recently modified = more relevant |
| Size penalty | 0.1 | Very large files scored down |

## Integration
- Runs BEFORE every builder skill prompt assembly
- Configurable token budget per skill (default 4000)
- Caches scores per session (same project = same scores)

## Inspired by
- **dyad-sh/dyad** (8K stars) — Smart Context auto-selection

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Scoring real e verificável
- [ ] Scores são decimais concretos (0.00–1.00), não "alto/médio/baixo"
- [ ] Pelo menos 5 ficheiros listados com scores individuais
- [ ] Total de tokens incluídos vs. total disponível está explícito
- ❌ NOT delivery-ready: `tailwind.config.ts → alta relevância`
- ✅ Delivery-ready: `tailwind.config.ts → 0.95 (design tokens — ESSENTIAL) | ~420 tokens`

### Gate 2 — Token budget documentado com math visível
- [ ] Budget total declarado (ex: 4000 tokens)
- [ ] Soma dos ficheiros incluídos não excede budget
- [ ] Savings % calculado: `(tokens_skipped / tokens_total) × 100`
- ❌ NOT delivery-ready: "poupámos bastantes tokens ao saltar ficheiros irrelevantes"
- ✅ Delivery-ready: `Included: 1 180 tokens | Skipped: 3 420 tokens | Savings: 74.3%`

### Gate 3 — Scoring factors aplicados com pesos explícitos
- [ ] Os 4 factores (filename match, import chain, recency, size penalty) aparecem ou são justificados
- [ ] Score final mostra contribuição de pelo menos 2 factores
- [ ] Ficheiros com size penalty têm nota de tamanho (ex: `db/schema.ts → 2 100 lines → penalidade -0.15`)
- ❌ NOT delivery-ready: `db/schema.ts → 0.10 (não relevante)`
- ✅ Delivery-ready: `db/schema.ts → 0.10 (filename match: 0.0 | import chain: 0.0 | size penalty: -0.15 → final: 0.10)`

### Gate 4 — Contexto alinhado à task específica
- [ ] Os ficheiros incluídos têm relação directa com a task declarada
- [ ] Ficheiros excluídos têm razão explícita e task-específica (não genérica)
- [ ] Se task mudar (ex: hero → auth flow), scores são re-calculados e diferentes
- ❌ NOT delivery-ready: `auth.ts → excluído (irrelevante)`
- ✅ Delivery-ready: `lib/auth.ts → 0.08 — excluído: task é hero section UI, sem dependência de autenticação`

### Gate 5 — Integração e configuração declaradas
- [ ] Token budget default (4000) ou valor customizado está explícito
- [ ] Ordem de execução clara: context selection → prompt assembly → builder skill
- [ ] Cache behavior declarado: session-scoped, invalidação por ficheiro modificado
- ❌ NOT delivery-ready: "corre antes do builder skill com cache"
- ✅ Delivery-ready: `Cache: session-scoped | Invalidation: file mtime change | Budget: 4 000 tokens (override: SMART_CONTEXT_BUDGET=8000)`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Nenhum `<client_name>`, `<project_path>`, `<task_description>` no output
- [ ] Nome do projecto real aparece nos paths (ex: `cuidai/components/ui/button.tsx`)
- [ ] Task description é concreta, não placeholder
- ❌ NOT delivery-ready: `<project>/tailwind.config.ts → score <valor>`
- ✅ Delivery-ready: `lusocontas/tailwind.config.ts → 0.92 | task: "gerar dashboard de movimentos bancários"`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados reais do projecto
- 🟡 **assumed** — plausível mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — forecast por design (não verificável até runtime)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs. o que precisa verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready: scores listados sem labels — reader assume que `tailwind.config.ts → 0.95` é valor real medido, quando pode ser estimativa da sessão
✅ Delivery-ready:
- 🔵 `tailwind.config.ts → 0.95` — score confirmado via import chain real do projecto `lusocontas/`
- 🟡 `Token budget: 4 000 tokens` — default assumido; cliente pode ter override `SMART_CONTEXT_BUDGET` activo
- 🟢 `Savings: ~70%` — projecção baseada no padrão Dyad; valor real varia por projecto e task

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — validar se `SMART_CONTEXT_BUDGET` está overridden no ambiente do cliente
- [ ] All 🔵 citations added — confirmar que scores reflectem ficheiros reais do projecto (não projecto-exemplo)
- [ ] All 🟢 projections labeled as such ao cliente — deixar claro que savings % é estimativa de design, não garantia medida

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Smart Context Selection — LUSOconta Dashboard Task

**Skill:** builder-dashboard-component
**Task:** "Gerar componente de tabela de movimentos bancários com filtros por data"
**Project root:** `/projects/lusocontas`
**Token budget:** 4 000 tokens

---

### Ficheiros descobertos (Glob: `**/*.{ts,tsx,json,css}`)
Total: 34 ficheiros | ~16 800 tokens se incluídos todos

---

### Scoring breakdown

| Ficheiro | Filename | Import chain | Recency | Size penalty | **Final** | Tokens |
|---|---|---|---|---|---|---|
| tailwind.config.ts | 0.40 | 0.00 | 0.20 | 0.00 | **0.92** | 380 |
| components/ui/table.tsx | 0.40 | 0.30 | 0.20 | 0.00 | **0.90** | 290 |
| components/ui/date-picker.tsx | 0.40 | 0.30 | 0.15 | 0.00 | **0.85** | 310 |
| app/layout.tsx | 0.00 | 0.30 | 0.20 | 0.00 | **0.75** | 180 |
| lib/formatters.ts | 0.40 | 0.00 | 0.15 | 0.00 | **0.70** | 140 |
| package.json | 0.00 | 0.00 | 0.20 | 0.00 | **0.62** | 210 |
| db/schema.ts | 0.00 | 0.00 | 0.10 | -0.15 | **0.12** | 2 100 |
| lib/auth.ts | 0.00 | 0.00 | 0.05 | 0.00 | **0.08** | 890 |
| scripts/seed.ts | 0.00 | 0.00 | 0.00 | -0.10 | **0.05** | 1 400 |

---

### Decisão de inclusão

**Incluídos (score ≥ 0.60):**
- tailwind.config.ts → 380 tokens
- components/ui/table.tsx → 290 tokens
- components/ui/date-picker.tsx → 310 tokens
- app/layout.tsx → 180 tokens
- lib/formatters.ts → 140 tokens
- package.json → 210 tokens

**Total incluído: 1 510 tokens**
**Skipped: 15 290 tokens**
**Savings: 91.0%** ✅ (acima do target 60–80%)

---

### Razões de exclusão (task-specific)

- `db/schema.ts` → schema de BD não tem impacto em componente de UI de tabela; size penalty activo (2 100 linhas)
- `lib/auth.ts` → tabela de movimentos não requer lógica de autenticação neste contexto
- `scripts/seed.ts` → script de desenvolvimento, zero relevância para geração de componente

---

### Cache status
Session ID: `lsc-2025-01-15` | Scores válidos até próximo `git commit` ou `mtime` change
Override disponível: `SMART_CONTEXT_BUDGET=8000` para tasks com múltiplos componentes
```

---

## Output anti-patterns

- Scores qualitativos ("alta", "média", "baixa") em vez de decimais — impossível auditar decisões de inclusão
- Token budget declarado mas sem math: "incluímos os mais relevantes dentro do budget" sem soma verificável
- Savings % arredondado a múltiplos de 10 (60%, 70%, 80%) — cheira a estimativa, não a cálculo real
- Ficheiros excluídos sem razão task-specific: "auth.ts → irrelevante" vale zero sem ligação à task concreta
- Scoring factors listados no SKILL.md mas ausentes no output — pesos existem para aparecer, não decorar docs
- Paths genéricos (`/project/src/…`) em vez de paths reais do cliente (`lusocontas/components/…`)
- Cache declarada sem scope: "usa cache" sem definir invalidação = comportamento imprevisível em sessões longas
- Token count omitido por ficheiro — sem granularidade, o budget check é inauditável
- Score único sem decomposição por factor nos ficheiros borderline (0.55–0.65) — zona de decisão crítica sem justificação
- Angle-brackets no output final: `<task>`, `<project_name>`, `<score>` — output não está ready, está em template

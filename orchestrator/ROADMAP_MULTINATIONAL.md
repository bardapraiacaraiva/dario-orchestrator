# DARIO Orchestrator — Roadmap para Nível Multinacional

## Auditoria Pós-Sessão 2026-05-05

### O que funciona E2E (10/10 subsistemas testados):
- DB lifecycle ACID (create→assign→checkout→complete→score, CAS previne double-execute)
- Dispatch engine (130+ workers, keyword routing, workload awareness, fallback)
- State machine (4 estados, triggers reais, autonomy ladder P-A1→P-A4)
- Guardrails (7 checks, DB-first com YAML fallback)
- Executor (pipeline completa: guard→context→rubric→trace→prompt→checkout)
- Chain executor (DAG waves, checkpoints per-step, artifact validation)
- Evolution (journals, mutations, crystallization — dados reais)
- AutoDiag (7 checks executáveis com auto-fix)
- Runtime API (27 endpoints, scheduler interno)
- File locking (OS-level + WAL + atomic write)

### 10 Gaps honestos para nível multinacional:
1. Execução depende de Claude numa sessão (não invoca API directamente)
2. DB e YAML coexistem (dual-write, inconsistência potencial)
3. Zero testes automatizados (pytest, CI/CD)
4. Quality scoring é registro, não cálculo (depende de Claude inline)
5. Token metering é self-report (não captura usage real)
6. Runtime não persiste entre reboots (sem service manager)
7. Sem autenticação na API (qualquer processo pode chamar)
8. Dashboard é server-rendered (não reactive)
9. Sem multi-tenancy (um DB, um company.yaml)
10. Evolution não fecha o loop (weights não influenciam dispatch)

---

## NÍVEL 1 — PRODUÇÃO (Score actual 9/10 → Enterprise-ready)

### 1.1 Claude API Direct Execution
**O maior gap.** O executor monta o prompt perfeito mas não pode executar sem sessão Claude.

Implementar:
- `api_executor.py` — invoca Claude API (Anthropic SDK) directamente
- Modelo routing: Haiku para tasks simples, Sonnet para standard, Opus para critical
- Prompt caching: reutilizar system prompts entre tasks do mesmo skill
- Streaming: output parcial em tempo real para o dashboard
- Cost tracking: tokens reais da API response, não estimativas

```python
from anthropic import Anthropic
client = Anthropic()

def execute_via_api(task, prompt, model="claude-sonnet-4-6"):
    response = client.messages.create(
        model=model,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    return {
        "output": response.content[0].text,
        "tokens_input": response.usage.input_tokens,
        "tokens_output": response.usage.output_tokens,
        "cost": calculate_cost(response.usage),
    }
```

**Impacto:** O runtime passa a executar tasks 24/7 sem sessão Claude aberta. Autonomia REAL.

### 1.2 DB como Única Fonte de Verdade
Eliminar dual-write:
- Todos os engines lêem do DB (não de YAML)
- `db_sync.py` — exporta DB → YAML para human readability (cron, não real-time)
- Guardrails, dispatch, state machine, quality — todos via `from db import DB`
- Migrar tasks/active/*.yaml → SQLite (one-time, com `--migrate-yaml`)
- YAML fica como formato de IMPORT (user cria YAML → import tool → DB)

### 1.3 Test Suite Automatizada
```
tests/
  test_db.py            — 20 tests (CRUD, CAS, concurrent access)
  test_dispatch.py      — 15 tests (routing, fallback, workload)
  test_state_machine.py — 12 tests (transitions, triggers, autonomy)
  test_guardrails.py    — 10 tests (each check, edge cases)
  test_executor.py      — 8 tests (full pipeline, failure paths)
  test_chain.py         — 10 tests (checkpoints, resume, artifacts)
  test_evolution.py     — 8 tests (journals, mutations, bounds)
  test_replanner.py     — 10 tests (each failure type, escalation)
  conftest.py           — fixtures (test DB, mock tasks, mock company)
```

Run: `pytest tests/ -v --cov=. --cov-report=html`
CI: GitHub Actions on every push

### 1.4 Service Management (Persistência entre reboots)
Windows:
```python
# runtime_service.py — NSSM wrapper
# nssm install DarioRuntime "python" "C:\Users\barda\.claude\orchestrator\runtime.py"
# nssm set DarioRuntime AppDirectory "C:\Users\barda\.claude\orchestrator"
# nssm start DarioRuntime
```

Linux: systemd unit file
Docker: `Dockerfile` + `docker-compose.yml` para deploy portátil

### 1.5 API Authentication + RBAC
```python
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = APIKeyHeader(name="X-API-Key")

ROLES = {
    "admin": ["*"],
    "operator": ["tasks.*", "dispatch", "pulse"],
    "viewer": ["tasks.read", "audit", "budget", "dashboard"],
}

# Per-request auth
@app.get("/tasks", dependencies=[Depends(verify_api_key)])
```

---

## NÍVEL 2 — INTELIGÊNCIA AVANÇADA (Enterprise → AI-Native)

### 2.1 Auto-Quality via API (LLM-as-Judge)
Em vez de Claude inline scoring, usar uma API call separada:
```python
def auto_score(task_output, rubric):
    """Use Haiku as judge — cheap, fast, consistent."""
    prompt = f"Score this output against the rubric. Return JSON only.\n\nRubric:\n{rubric}\n\nOutput:\n{task_output}"
    response = client.messages.create(model="claude-haiku-4-5-20251001", ...)
    return json.loads(response.content[0].text)
```

Benefícios:
- Scoring consistente (mesmo modelo, mesmo prompt)
- Barato (Haiku para scoring, Opus para execução)
- Batch scoring possível (re-score histórico)
- A/B testing de rubrics

### 2.2 Evolution Loop Fechado
Os synaptic weights DEVEM influenciar o dispatch. Implementar:

```python
# dispatch_engine.py — usar weights no scoring
def score_worker_with_weights(worker, task, weights):
    base_score = capability_overlap(worker, task)
    
    # Boost se este worker tem alta afinidade com skills co-activados
    for pair, weight_data in weights.items():
        if worker.skill in pair and weight_data['weight'] > 0.7:
            base_score *= 1.0 + (weight_data['weight'] - 0.5)
    
    return base_score
```

Adicionalmente:
- Auto-detect qual modelo (Haiku/Sonnet/Opus) produz melhor score por skill
- Model routing adaptativo: skill X funciona melhor com Sonnet → usa Sonnet
- Feedback loop: score < 60 → flag skill para review → propor prompt improvement

### 2.3 Smart Token Metering (Real)
Hook no PostToolUse para capturar tokens reais:
```json
// settings.json — PostToolUse hook
{
    "matcher": "Agent",
    "hooks": [{
        "type": "command",
        "command": "python ~/.claude/orchestrator/meter.py --task $TASK_ID --input $INPUT_TOKENS --output $OUTPUT_TOKENS"
    }]
}
```

Metering dashboard: custo real por task, por skill, por modelo, por projecto.

### 2.4 Predictive Dispatch
Usar histórico de scores + tokens para predizer ANTES de executar:
- Estimated quality: "este skill neste domínio tipicamente faz 85/100"
- Estimated cost: "tasks deste tipo custam ~2500 tokens"
- Risk score: "esta combinação skill+worker tem 15% revision rate"
- Auto-route para modelo mais custo-eficiente baseado no risco

### 2.5 Context RAG Integration (Deep)
O context_injector.py já busca RAG, mas superficialmente. Implementar:
- Vector search por TASK DESCRIPTION (não só keywords)
- Inject top-3 RAG chunks directamente no prompt
- Track quais chunks levaram a scores altos → reinforce
- Auto-ingest task outputs de alta qualidade como novo conhecimento RAG

---

## NÍVEL 3 — DIFERENCIAÇÃO GLOBAL (AI-Native → Unprecedented)

### 3.1 Multi-Agent Orchestration via Claude Managed Agents
Usar a Claude Managed Agents API (`/v1/agents`) para execução persistente:
```python
# Criar um agent por division (DARIO, DIVA, LUCAS)
dario_agent = client.agents.create(
    model="claude-sonnet-4-6",
    instructions="You are the DARIO digital agency CEO...",
    tools=[{"type": "code_execution"}, {"type": "file_search"}],
)

# Cada task é uma session no agent
session = client.agents.sessions.create(agent_id=dario_agent.id)
response = client.agents.sessions.messages.create(
    agent_id=dario_agent.id,
    session_id=session.id,
    messages=[{"role": "user", "content": prompt}],
)
```

Benefícios:
- Agentes PERSISTENTES com memória de sessão
- File search integrado (RAG nativo)
- Code execution (Opus pode executar Python inline)
- Multi-turn (follow-up questions automáticas)

### 3.2 Multi-Tenancy
```sql
-- Adicionar tenant_id a todas as tabelas
ALTER TABLE tasks ADD COLUMN tenant_id TEXT DEFAULT 'default';
ALTER TABLE audit ADD COLUMN tenant_id TEXT DEFAULT 'default';
ALTER TABLE budget ADD COLUMN tenant_id TEXT DEFAULT 'default';

CREATE INDEX idx_tasks_tenant ON tasks(tenant_id);
```

- Um DB, múltiplos tenants (equipas, clientes, projectos)
- Budget isolado por tenant
- RBAC per-tenant (admin da equipa A não vê tasks da equipa B)
- Company.yaml per-tenant (diferentes hierarquias)

### 3.3 Reactive Dashboard (SPA)
Substituir o HTML server-rendered por:
- Next.js SPA com Tailwind + shadcn/ui
- SSE subscription para updates em tempo real
- Interactive DAG (D3.js force-directed graph, drag to reorder)
- Task detail panel (trace, rubric, artifacts, history)
- Budget gauge animado
- Timeline view (Gantt-like para chains)
- Mobile responsive

### 3.4 Plugin Marketplace
Permitir que terceiros criem e instalem skills no DARIO:
```yaml
# skill manifest
name: "seo-youtube"
version: "1.0.0"
author: "community"
schema:
  required: ["video_title", "description", "tags"]
  optional: ["thumbnail_prompt"]
triggers: ["youtube seo", "video optimization"]
```

- `dario install seo-youtube` — instala skill + worker + schema
- Marketplace HTML com ratings, downloads, compatibility
- Sandbox execution (skill não pode aceder a outros projectos)

### 3.5 Workflow Designer (Visual)
Interface drag-and-drop para compor workflows:
- Arrastar skills para um canvas
- Conectar com setas (dependências)
- Configurar conditions (if score > X → path A)
- Preview mode (dry-run visual)
- Export como skill_chain YAML ou chain_executor run

### 3.6 Cross-Instance Federation
Múltiplas instâncias DARIO a comunicar:
- Instance A (Lisboa office) ↔ Instance B (NYC office)
- Tasks podem ser delegadas entre instances
- Shared audit trail (append-only, CRDTs para merge)
- Budget consolidado cross-instance
- Ideal para a "multinacional" com offices distribuídos

### 3.7 Compliance & Governance Layer
- RGPD: data retention policies, right-to-forget per task
- SOC2: immutable audit log, access controls, encryption at rest
- ISO 27001: risk assessment automático, control mapping
- Audit export: CSV/PDF para auditores externos
- Data residency: tenant data stays in specified region

### 3.8 Observability Stack
Substituir audit_logger.py + tracer.py por stack profissional:
- OpenTelemetry integration (traces, metrics, logs)
- Prometheus metrics endpoint (/metrics)
- Grafana dashboards (latency, throughput, error rate, cost)
- Alerting: PagerDuty/OpsGenie integration
- SLO tracking: 99.9% task completion rate target

### 3.9 Natural Language Interface
Em vez de commands, conversar com o orchestrator:
- "Quais tasks estão atrasadas?" → query DB, format response
- "Cria um brand audit para a Vivenda" → template instantiation
- "Porque é que o MNB-003 falhou?" → trace lookup + root cause analysis
- "Replaneia o projecto mar-brasa" → chain re-execution
- Powered by: runtime API + Claude with tool_use

### 3.10 Cost Optimization Engine
Análise e optimização automática de custos:
- Identify: quais skills são over-specified (Opus quando Haiku bastava)
- Suggest: model downgrade para tasks com revision_rate < 5%
- Auto-route: tasks simples → Haiku ($0.25/M), complexas → Opus ($15/M)
- Caching: prompts similares → reutilizar system prompt cached
- Batching: agrupar tasks não-urgentes para batch API (50% desconto)
- Monthly report: "Optimizámos $X este mês vs last month"

---

## Priorização para Implementação Imediata

### Sprint 1 (esta semana): FECHAR OS LOOPS
1. **Claude API execution** — executor.py invoca API directamente → AUTONOMIA REAL
2. **Evolution weights → dispatch** — fechar o learning loop
3. **DB-only mode** — eliminar dual-write

### Sprint 2 (próxima semana): PRODUÇÃO
4. **Test suite** — pytest completo
5. **Service manager** — runtime persiste entre reboots
6. **Real token metering** — PostToolUse hook

### Sprint 3 (semana 3): INTELIGÊNCIA
7. **LLM-as-Judge** — auto-scoring via Haiku
8. **Predictive dispatch** — quality/cost estimates antes de executar
9. **Deep RAG integration** — vector search no context injection

### Sprint 4 (semana 4): DIFERENCIAÇÃO
10. **API auth + RBAC**
11. **Reactive dashboard (Next.js)**
12. **Managed Agents integration**

---

## Métricas de Sucesso (KPIs para a Multinacional)

| KPI | Target | Como medir |
|---|---|---|
| Task completion rate | 95%+ | done / (done + blocked + failed) |
| First-pass quality | 80%+ avg score | avg(quality_score) across all tasks |
| Revision rate | < 10% | tasks_revised / tasks_completed |
| Cost per task | < $0.50 avg | total_cost / tasks_completed |
| Time to completion | < 5 min avg | completed_at - created_at |
| System health | > 0.90 | state_machine.py health metric |
| Uptime | 99.9% | runtime availability |
| Evolution velocity | +2 rules/week | crystallized_rules / weeks |
| Dispatch accuracy | > 95% | correct_first_dispatch / total_dispatches |
| Budget adherence | < 80% monthly | actual_spend / budget_limit |

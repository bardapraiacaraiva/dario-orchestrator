---
name: dario-ai-engineering
description: AI Engineering squad — build production LLM products from POC to production. RAG systems, multi-agent architectures, tool-use workflows, structured outputs, evals, cost optimization, observability, fine-tuning, and model selection. Triggers on "ai engineering", "rag production", "multi-agent", "llm production", "evals", "ai pipeline", "model selection", "ai cost", "fine-tuning", "function calling", "tool use", "structured output".
version: 1.0.0
license: MIT
---

# DARIO Skill — AI Engineering

From POC to production: the engineering discipline of building reliable, observable, cost-efficient products with LLMs. This is not prompt engineering — this is the systems thinking that turns a working demo into a product that handles 10,000 requests/day without breaking or bankrupting you.

## When to activate

- Building a RAG system beyond the tutorial stage
- Designing multi-agent architectures (orchestrator, router, specialist agents)
- Implementing tool-use / function calling in production
- Setting up LLM evaluations (offline evals, regression tests, online monitoring)
- Optimizing LLM costs (caching, batching, model routing, prompt compression)
- Adding observability to LLM pipelines (tracing, debugging, latency tracking)
- Deciding whether to fine-tune vs prompt engineer vs RAG
- Choosing between models (Claude vs GPT vs Gemini vs Llama vs Mistral)
- Structured output design (JSON mode, function calling, schema validation)
- Migrating from prototype to production-grade AI system
- Debugging non-deterministic LLM behavior
- User asks "how do I make this AI thing actually work reliably?"

## Workflow

### 1. Assess current state

- **What exists:** POC? Prototype? Production system?
- **Traffic:** Expected requests/day, peak load, latency requirements
- **Budget:** Monthly LLM API spend ceiling
- **Data:** What data is available for RAG/fine-tuning? Volume, quality, format?
- **Team:** Who maintains this? ML engineers? Full-stack devs? Solo founder?
- **Requirements:** Accuracy target, latency SLA, compliance needs

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "RAG production retrieval augmented generation chunking embedding", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "multi-agent architecture orchestration tool use function calling", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "LLM evaluation evals regression testing accuracy", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "LLM cost optimization caching batching model routing", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "LLM observability tracing debugging monitoring production", collection: "dario", limit: 5)
```

### 3. Architecture decision

Choose the right pattern for the problem:

#### Pattern A: Simple Chain
```
User → Prompt Template → LLM → Parse → Output
```
**When:** Single-turn, well-defined tasks with predictable input/output. Example: email classification, text extraction.

#### Pattern B: RAG Pipeline
```
User Query → Embed → Retrieve (vector DB) → Rerank → Augment Prompt → LLM → Output
```
**When:** Need factual accuracy from a specific knowledge base. Example: customer support bot, internal docs Q&A.

#### Pattern C: Agentic Loop
```
User → Planner LLM → [Tool Call → Result]* → Synthesizer LLM → Output
```
**When:** Multi-step tasks requiring external actions. Example: research assistant, code generation with execution.

#### Pattern D: Multi-Agent Orchestration
```
User → Router → Agent A / Agent B / Agent C → Synthesizer → Output
```
**When:** Different domains or expertise needed per query. Example: DARIO itself, customer service with specialist routing.

#### Pattern E: Human-in-the-Loop
```
User → LLM Draft → Human Review → Approve/Edit → Execute
```
**When:** High-stakes decisions, regulated industries, early-stage trust building.

### 4. Component deep-dives

#### RAG Production Systems

**Chunking strategy:**
- Fixed-size chunks (512-1024 tokens) for general text
- Semantic chunking (by paragraph/section boundaries) for structured docs
- Recursive character splitting as fallback
- Overlap: 10-20% between chunks to preserve context at boundaries
- Metadata: always attach source, page, section, date to every chunk

**Embedding selection:**
- `text-embedding-3-small` (OpenAI): good balance of cost and quality
- `text-embedding-3-large` (OpenAI): best quality, higher cost
- `voyage-3` (Voyage AI): strong for code and technical content
- Local models (e5-large, bge-large): zero API cost, self-hosted
- Rule: benchmark on YOUR data with YOUR queries — leaderboard rankings lie

**Retrieval optimization:**
- Hybrid search: vector similarity + BM25 keyword search
- Reranking: Cohere Rerank or cross-encoder after initial retrieval
- HyDE (Hypothetical Document Embeddings): generate ideal answer, embed that, search
- Query expansion: rephrase user query into 2-3 variants, retrieve for each
- Metadata filtering: pre-filter by date, source, category before vector search

**Failure modes to watch:**
- Retrieval returns irrelevant chunks → embedding/chunking mismatch
- Correct chunks retrieved but LLM ignores them → prompt structure issue
- LLM hallucinates despite good retrieval → need stronger grounding instructions
- Latency too high → reduce chunk count, use smaller reranker, cache frequent queries

#### Multi-Agent Architectures

**Router pattern:**
- Classifier LLM (small, fast) routes to specialist agents
- Each agent has its own system prompt, tools, and context
- Router must handle "none of the above" — fallback agent or human escalation
- Keep router prompt simple: list of agents + descriptions + example queries

**Orchestrator pattern:**
- Planner LLM decomposes task into subtasks
- Dispatcher assigns subtasks to agents
- Aggregator collects results and synthesizes
- Error handler catches agent failures and retries or escalates

**Agent communication:**
- Shared memory (context window, external store) vs message passing
- Structured handoff format: `{task, context, constraints, expected_output}`
- Never pass raw LLM output between agents — always parse/validate first

#### Structured Outputs

**JSON mode:** Force LLM to output valid JSON. Use when:
- Downstream code needs to parse the output
- Multiple fields need extraction from unstructured text
- API response must conform to a schema

**Function calling:** Define tools the LLM can invoke. Use when:
- LLM needs to take actions (API calls, DB queries, calculations)
- Multi-step workflows with decision points
- Grounding responses in real-time data

**Schema validation:** Always validate LLM outputs against a schema:
- Zod (TypeScript), Pydantic (Python) for type-safe parsing
- Retry with error feedback if validation fails (max 3 retries)
- Fallback to human review if retries exhausted

#### Evaluations

**Offline evals (before deploy):**
- Golden dataset: 50-200 input/expected-output pairs
- Metrics: accuracy, F1, BLEU/ROUGE (text), exact match (structured)
- LLM-as-judge: use a stronger model to grade a weaker model's output
- A/B prompt comparison: run same inputs through prompt variants, compare scores
- Run on every prompt change, model change, or system update

**Regression tests:**
- Critical examples that must always pass (the "never break these" set)
- Run in CI/CD pipeline before deploying prompt changes
- Minimum 20 cases covering edge cases, not just happy path

**Online monitoring:**
- Track: latency, token usage, error rate, user feedback (thumbs up/down)
- Alert on: latency p95 > threshold, error rate > 5%, feedback score drop
- Log every request/response pair (anonymized) for debugging
- Weekly review: sample 20 random responses, manually grade quality

#### Cost Optimization

**Caching:**
- Prompt caching (Anthropic, OpenAI): cache system prompt + common prefixes
- Semantic caching: hash similar queries, return cached responses
- Exact-match caching: identical queries get cached response (Redis/Memcached)
- Cache invalidation: time-based (TTL) or content-based (source data changed)

**Batching:**
- Batch API (Anthropic, OpenAI): 50% cost reduction for non-real-time tasks
- Queue non-urgent requests, process in batch windows
- Good for: bulk classification, content generation, data extraction

**Model routing:**
- Easy queries → small/cheap model (Haiku, GPT-4o-mini)
- Hard queries → large/expensive model (Opus, GPT-4o, Gemini Pro)
- Router: classifier that scores query complexity, routes accordingly
- Savings: 40-70% with minimal quality loss on routed queries

**Prompt optimization:**
- Shorter prompts = fewer tokens = lower cost
- Remove redundant instructions, examples that don't improve output
- Use structured few-shot (3-5 examples) instead of verbose instructions
- Measure: cost per request, cost per successful request

#### Observability

**Tracing:**
- Trace every LLM call: input, output, latency, tokens, model, temperature
- Trace tool calls: which tools invoked, inputs, outputs, errors
- Trace retrieval: queries, retrieved chunks, reranking scores
- Tools: LangSmith, Langfuse, Arize Phoenix, Helicone, custom logging

**Debugging non-deterministic behavior:**
- Temperature 0 reduces but doesn't eliminate variation
- Log the exact prompt (after template rendering) for every request
- Compare outputs across runs with same input — track consistency
- When debugging: fix seed (if available), reduce temperature, add constraints

#### Fine-tuning Decision Framework

**Don't fine-tune if:**
- Prompt engineering hasn't been exhausted
- RAG can provide the knowledge needed
- Dataset is < 500 high-quality examples
- The task changes frequently (fine-tuned model = frozen behavior)
- Budget is limited (fine-tuning + hosting costs add up)

**Do fine-tune if:**
- Consistent style/format needed that prompting can't achieve
- Latency critical (fine-tuned small model faster than prompted large model)
- Cost critical at scale (fine-tuned small model cheaper per request)
- Proprietary knowledge that can't be in prompts (security)
- Dataset is > 1000 high-quality examples with clear input/output pairs

#### Model Selection (Real Tradeoffs)

| Model | Strengths | Weaknesses | Best For |
|-------|-----------|------------|----------|
| **Claude Opus** | Deep reasoning, long context, code, safety | Cost, latency | Complex analysis, code gen, research |
| **Claude Sonnet** | Balance of quality and speed | Not as deep as Opus | Production workloads, general use |
| **Claude Haiku** | Speed, cost, good enough quality | Less nuanced reasoning | Classification, extraction, routing |
| **GPT-4o** | Multimodal, wide knowledge, fast | Cost at scale, less consistent on complex tasks | Multimodal apps, general purpose |
| **GPT-4o-mini** | Very cheap, fast | Quality ceiling for complex tasks | High-volume simple tasks |
| **Gemini Pro** | Long context (1M+), multimodal | API stability, less coding strength | Large document processing |
| **Llama 3.1 70B** | Self-hosted, no API cost, customizable | Hosting cost, ops burden, quality gap | Privacy-sensitive, high-volume |
| **Mistral Large** | European, GDPR-friendly, capable | Smaller ecosystem | EU compliance-sensitive apps |

**Rule:** Never choose a model based on benchmarks alone. Test with YOUR data, YOUR prompts, YOUR use cases. Benchmark scores are marketing.

### 5. Production checklist

Before going live, verify:

- [ ] **Evals pass:** Golden dataset accuracy above threshold
- [ ] **Regression tests pass:** All critical cases green
- [ ] **Error handling:** Graceful degradation when LLM fails, times out, or returns garbage
- [ ] **Rate limiting:** Respect API rate limits, implement backoff
- [ ] **Cost controls:** Per-user and per-day spend caps, alerts at 80% of budget
- [ ] **Observability:** Tracing, logging, metrics dashboards operational
- [ ] **Caching:** Prompt caching and/or semantic caching enabled
- [ ] **Fallback:** Human escalation path for low-confidence responses
- [ ] **Content safety:** Input/output filtering for harmful content
- [ ] **Data privacy:** PII handling, data retention policy, GDPR compliance
- [ ] **Latency:** p50 and p95 within SLA
- [ ] **Load testing:** Tested at 2x expected peak traffic

## Commands

| Command | Description |
|---------|-------------|
| `/rag-design` | Design a RAG system — chunking strategy, embedding model, retrieval pipeline, reranking |
| `/agent-arch` | Design multi-agent architecture — router, specialists, orchestrator, error handling |
| `/eval-setup` | Create evaluation framework — golden dataset, metrics, LLM-as-judge prompts, CI integration |
| `/cost-audit` | Audit current LLM spend — identify savings via caching, batching, model routing |
| `/observe` | Design observability stack — tracing, logging, metrics, alerts, debugging workflow |
| `/model-select` | Model selection analysis — compare options for specific use case with cost/quality/latency tradeoffs |
| `/fine-tune-decision` | Structured decision: should you fine-tune? Data audit, alternative analysis, ROI projection |
| `/structured-output` | Design structured output schema — JSON mode, function calling, validation, retry logic |
| `/prod-checklist` | Production readiness checklist — comprehensive go/no-go for deploying LLM system |
| `/ai-debug` | Debug non-deterministic LLM behavior — trace analysis, prompt inspection, consistency testing |

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: ai-engineering
pattern: <simple-chain|rag|agentic|multi-agent|human-in-loop>
primary-model: <model name>
---

# AI Engineering — <System Name>

## Requirements
- **Use case:** ...
- **Traffic:** ...requests/day
- **Latency SLA:** p95 < ...ms
- **Accuracy target:** ...%
- **Monthly budget:** $...
- **Compliance:** ...

## Architecture
<Pattern selected + rationale>

### System Diagram
```
<ASCII diagram of components and data flow>
```

## Component Specifications

### Retrieval (if RAG)
- **Embedding model:** ...
- **Vector DB:** ...
- **Chunk strategy:** ...
- **Reranking:** ...

### LLM Configuration
- **Model:** ...
- **Temperature:** ...
- **Max tokens:** ...
- **System prompt:** <summary, full prompt in appendix>

### Tools / Function Calling (if agentic)
| Tool | Description | Input Schema | Output Schema |
|------|-------------|-------------|---------------|
| ... | ... | ... | ... |

### Structured Output Schema
```json
{ ... }
```

## Evaluation Plan
### Golden Dataset
- **Size:** ... examples
- **Source:** ...
- **Metrics:** ...

### Regression Tests
- **Critical cases:** ... examples
- **CI integration:** ...

### Online Monitoring
- **Metrics tracked:** ...
- **Alert thresholds:** ...

## Cost Model
| Component | Cost/request | Monthly (at volume) |
|-----------|-------------|-------------------|
| LLM calls | ... | ... |
| Embeddings | ... | ... |
| Vector DB | ... | ... |
| Reranking | ... | ... |
| **Total** | ... | **$...** |

### Optimization Applied
- Caching: ...
- Batching: ...
- Model routing: ...
- **Savings:** ...%

## Observability
- **Tracing tool:** ...
- **Key dashboards:** ...
- **Alert channels:** ...

## Production Readiness
- [ ] Evals pass
- [ ] Regression tests pass
- [ ] Error handling tested
- [ ] Cost controls active
- [ ] Observability operational
- [ ] Load tested

## Next Steps
- [ ] ...
```

## Save location

- Architecture designs → `05 - Claude - IA/Outputs/YYYY-MM-DD - AI Engineering - <System Name>.md`
- Eval frameworks → `05 - Claude - IA/Outputs/YYYY-MM-DD - AI Evals - <System Name>.md`
- Cost audits → `05 - Claude - IA/Outputs/YYYY-MM-DD - AI Cost Audit - <System Name>.md`

## Integration points

| Skill | Relationship |
|-------|-------------|
| `dario-c-level` | CAIO delegates implementation details here; this skill reports ROI back to CAIO |
| `dario-product` | Product defines what to build; this skill defines how to build it with AI |
| `dario-data` | Data squad provides analytics/metrics; this skill consumes data for RAG and evals |
| `dario-rag-ingest` | This skill designs the RAG architecture; `dario-rag-ingest` handles the actual ingestion |
| `dario-saas-metrics` | SaaS metrics inform cost optimization and usage-based pricing decisions |
| `dario-diagnose` | Diagnose identifies AI opportunities; this skill designs the implementation |
| `dario-sop` | SOPs generated for AI system operations, monitoring, and incident response |
| `dario-pentest-checklist` | Security review of AI systems — prompt injection, data leakage, adversarial inputs |
| `dario-obsidian-save` | All outputs saved to vault |

## Red flags / anti-patterns

- **Demo-driven development** — building a product around a cool demo without validating the use case. A demo that works on 5 examples will fail on 5,000. Always start with evals, not demos.
- **No evals before production** — deploying an LLM system without a golden dataset and regression tests is deploying a system you cannot verify. You will not know when it breaks.
- **Ignoring cost until the bill arrives** — LLM costs scale linearly with usage. A system that costs $50/month in development can cost $5,000/month in production. Model the cost at target volume before building.
- **Fine-tuning as first resort** — fine-tuning is expensive, slow, and creates maintenance burden. Exhaust prompt engineering, RAG, and few-shot before considering fine-tuning.
- **Choosing models by benchmark** — benchmark scores measure performance on benchmark tasks, not your tasks. Always evaluate on your own data with your own prompts.
- **RAG without reranking** — vector similarity search alone returns "similar" documents, not "relevant" documents. Reranking is the difference between a system that mostly works and one that reliably works.
- **No fallback for LLM failures** — LLMs timeout, return errors, hallucinate, and produce malformed output. Every production system needs graceful degradation: retry, fallback model, human escalation.
- **Logging nothing** — if you don't log prompts, responses, latency, and token usage, you cannot debug, optimize, or improve. Observability is not optional.
- **Prompt injection ignorance** — every user-facing LLM system is vulnerable to prompt injection. Validate inputs, separate system/user prompts, and test adversarial inputs before launch.
- **Building multi-agent when single-agent suffices** — complexity is cost. Only add agents when a single agent demonstrably cannot handle the task. Start simple, add complexity only when measured need arises.

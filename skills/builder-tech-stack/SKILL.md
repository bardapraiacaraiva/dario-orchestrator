---
name: builder-tech-stack
description: >
  Seleccao de tech stack baseada em requisitos: framework, DB, hosting, scaling, custo.
  Analisa trade-offs. Recomenda com justificacao. Evita over-engineering.
  Use quando: que tecnologia usar, tech stack, framework, base de dados, hosting, stack.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Tech Stack Selection

## Proposito
Escolher a stack CERTA para o projecto — nao a mais cool, a mais adequada.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-tech-stack [tipo-app]` | Recomendacao de stack |
| `/builder-tech-stack compare [a] [b]` | Comparar duas opcoes |

## Decision Matrix

| Tipo de App | Frontend | Backend | DB | Deploy | Custo/mes |
|---|---|---|---|---|---|
| **Landing page** | Next.js | — | — | Vercel | EUR 0 |
| **SaaS simples** | Next.js | Next.js API | PostgreSQL | Vercel + Neon | EUR 0-25 |
| **SaaS complexo** | Next.js | Node/FastAPI | PostgreSQL | VPS Docker | EUR 15-50 |
| **E-commerce** | Next.js | WooCommerce | MySQL | VPS | EUR 15-30 |
| **Mobile-first** | React Native | Node/FastAPI | PostgreSQL | Vercel + VPS | EUR 15-50 |
| **AI product** | Next.js | Python FastAPI | PostgreSQL + pgvector | VPS | EUR 30-100 |
| **Blog/Content** | Next.js + MDX | — | — | Vercel | EUR 0 |

## Princípios
1. **Start simple** — Next.js resolve 80% dos casos
2. **PostgreSQL always** — nunca erras com Postgres
3. **Vercel first** — zero-config deploy, scale gratis ate 100K visits
4. **VPS when needed** — backends custom, AI, websockets
5. **No microservices** — monolito ate provar que precisa de mais

## Output
1. Stack recommendation (justified)
2. Trade-offs matrix
3. Cost estimate (monthly)
4. Scaling path (what changes at 10x, 100x)
5. Alternatives considered (and why rejected)

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Stack recommendation é justificada com critérios do projecto real
- [ ] Recomendação referencia tipo de app concreto (SaaS, AI product, landing, etc.)
- [ ] Justificação menciona pelo menos 2 requisitos do cliente (ex: budget, escala esperada, equipa)
- [ ] Não recomenda tech "porque é popular" — argumento é adequação ao caso
- [ ] Stack encaixa no Decision Matrix ou explica desvio explicitamente
- ❌ NOT delivery-ready: "Recomendo Next.js porque é muito usado atualmente"
- ✅ Delivery-ready: "Recomendo Next.js + Neon PostgreSQL porque a Cuidai precisa de deploy imediato sem equipa DevOps, budget EUR 0-25/mês, e o volume inicial é <10K visitas/mês — Vercel free tier cobre."

### Gate 2 — Trade-offs matrix tem dados, não opinião
- [ ] Cada opção comparada tem pelo menos: custo real (EUR/mês), complexidade (Low/Med/High), e um caso de uso onde falha
- [ ] Alternativas rejeitadas estão listadas com motivo específico (não "é complexo demais")
- [ ] Se compara dois frameworks, os critérios são os mesmos para ambos
- [ ] Números de custo têm fonte ou são do Decision Matrix documentado
- ❌ NOT delivery-ready: "Django é mais pesado que FastAPI mas tem mais features"
- ✅ Delivery-ready: "Django rejeitado: overhead EUR 20+/mês em VPS 2GB vs FastAPI em VPS 1GB EUR 6/mês (Hetzner CX11); para a Tributario.AI com 3 endpoints AI, FastAPI é suficiente e reduz custos 60%."

### Gate 3 — Cost estimate é mensal, itemizado, com provider real
- [ ] Custo total mensal em EUR com breakdown por componente (hosting, DB, CDN, etc.)
- [ ] Provider nomeado explicitamente (Vercel, Hetzner, Neon, Railway, Supabase, etc.)
- [ ] Tier de pricing especificado (free, pro, etc.) com link ou referência verificável
- [ ] Custo no ano 1 calculado (mensal × 12 ou com nota de ramp-up)
- ❌ NOT delivery-ready: "Custo baixo, ronda os 20-30 euros por mês"
- ✅ Delivery-ready: "Vercel Pro EUR 20/mês + Neon free tier EUR 0 + domínio EUR 12/ano = EUR 252/ano. Para ARRECADA.GOV com tráfego estimado 5K req/dia, Vercel free tier é suficiente nos primeiros 6 meses."

### Gate 4 — Scaling path é concreto (10x e 100x definidos)
- [ ] "10x tráfego" tem acção específica (ex: upgrade Neon paid, mover para VPS)
- [ ] "100x tráfego" tem arquitectura diferente descrita (não "vai precisar de mais")
- [ ] Custo estimado em cada patamar de escala
- [ ] Identifica o bottleneck mais provável (DB, compute, bandwidth)
- ❌ NOT delivery-ready: "A 100x vais precisar de uma infraestrutura mais robusta e talvez microservices"
- ✅ Delivery-ready: "10x (100K visits/mês): manter Vercel + upgrade Neon para EUR 19/mês. Bottleneck: DB connections — adicionar PgBouncer. 100x (1M visits/mês): migrar para Hetzner VPS EUR 20/mês + managed Postgres EUR 50/mês; Vercel edge functions continuam a servir frontend."

### Gate 5 — Stack é adequada ao perfil técnico da equipa do cliente
- [ ] Menciona quem vai manter (founder solo, dev júnior, equipa, sem dev)
- [ ] Não recomenda stack que a equipa não consegue operar (ex: Kubernetes para founder solo)
- [ ] Se stack exige conhecimento específico, flag está presente ("requer familiaridade com Docker")
- [ ] "No microservices até provar necessidade" está aplicado — monolito é default
- ❌ NOT delivery-ready: "Para o Atrium, recomendo arquitectura de microservices com Kubernetes e service mesh"
- ✅ Delivery-ready: "Para a Vivenda com 1 dev part-time: Next.js monorepo no Vercel — zero DevOps, deploy via git push. Docker e VPS só quando precisarem de websockets para notificações em tempo real (fase 2)."

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem placeholders entre angle-brackets
- [ ] Nenhum `<client-name>`, `<app-type>`, `<budget>`, `<team-size>` no output final
- [ ] Nome do projecto/cliente aparece pelo menos 2× na recomendação
- [ ] Todos os URLs, providers e versões são reais e actuais (não "framework X versão Y")
- [ ] Stack recommendation é assinada para ESTE projecto, não genérica
- ❌ NOT delivery-ready: "Para `<client>`, recomendo `<frontend-framework>` com `<database>`"
- ✅ Delivery-ready: "Stack final para SAQUEI v1.0: Next.js 14 + FastAPI 0.111 + PostgreSQL 16 (Neon) + Vercel. Custo mês 1: EUR 0."

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Stack Recommendation — Tributario.AI

**Tipo de app:** AI product (chat fiscal + document parsing)
**Equipa:** 1 dev fullstack (founder), sem DevOps
**Budget:** EUR 50-100/mês fase 1
**Escala esperada:** 500 utilizadores pagos no ano 1

---

### Stack Recomendada

| Camada | Tecnologia | Provider | Custo/mês |
|--------|-----------|----------|-----------|
| Frontend | Next.js 14 (App Router) | Vercel Pro | EUR 20 |
| Backend / API | Python FastAPI 0.111 | Hetzner CX21 (4GB) | EUR 6 |
| Base de dados | PostgreSQL 16 + pgvector | Neon Pro | EUR 19 |
| Auth | NextAuth.js v5 | — (incluído) | EUR 0 |
| AI / LLM | OpenAI API (gpt-4o) | OpenAI | ~EUR 30 (uso) |
| Storage docs | Cloudflare R2 | Cloudflare | EUR 0-5 |
| **Total** | | | **EUR 75-80/mês** |

---

### Justificação

- **Next.js + FastAPI separados** porque o parsing de documentos fiscais (PDFs,
  XMLs SAFT) precisa de Python nativo — bibliotecas como `pdfplumber` e
  `python-saft` não têm equivalente Node robusto.
- **pgvector no Neon** em vez de Pinecone: poupa EUR 70/mês em fase 1,
  PostgreSQL já está no stack, e <1M embeddings cabe confortavelmente.
- **Vercel para frontend** mantém zero-config deploy e preview environments
  por PR — crítico para founder solo iterar rápido.
- **Hetzner CX21 EUR 6/mês** suficiente para FastAPI + Celery worker para
  parsing assíncrono de documentos até 500 utilizadores.

---

### Alternativas Rejeitadas

| Opção | Razão de rejeição |
|-------|------------------|
| Supabase (tudo-em-um) | pgvector no Supabase Pro = EUR 25/mês + lock-in em edge functions; Neon mais flexível |
| Django REST Framework | Overhead desnecessário para 3 endpoints AI; FastAPI 3× mais rápido a implementar para este caso |
| Railway (backend) | EUR 20/mês vs Hetzner EUR 6 para mesmo compute; savings EUR 168/ano |
| Pinecone | EUR 70/mês no starter vs pgvector EUR 0 adicional no Neon já pago |

---

### Scaling Path

**Agora → 500 utilizadores (fase 1):**
Stack actual. Neon Pro aguenta 10GB + 1000 conexões. FastAPI single instance.

**10x → 5.000 utilizadores:**
- Adicionar PgBouncer no Hetzner (connection pooling, EUR 0 adicional)
- Upgrade Hetzner CX21→CX31 (8GB RAM, EUR 11/mês)
- Redis (Upstash free tier) para cache de respostas fiscais repetidas
- Custo estimado: EUR 110-120/mês

**100x → 50.000 utilizadores:**
- Separar FastAPI em 2 serviços: API principal + worker parsing (Hetzner × 2)
- PostgreSQL migrar para Neon Business ou managed RDS EUR 80/mês
- CDN Cloudflare pro para assets estáticos
- Custo estimado: EUR 200-250/mês
- **Bottleneck provável:** OpenAI API latency + custo — avaliar fine-tuned
  modelo open-source (Mistral) em GPU spot instance nessa fase

---

### Decisão Final

> Para a Tributario.AI em fase 1: **Next.js + FastAPI + PostgreSQL/pgvector**.
> Monolito lógico, dois processos físicos. Sem Docker Compose em produção até
> precisar de orquestrar 3+ serviços. Revisão de stack em Março 2026 se
> ultrapassar 2.000 utilizadores activos.
```

---

## Output anti-patterns

- Recomendar stack sem mencionar o nome do cliente ou projecto — output genérico não é consultoria
- Custos sem provider real: "hosting barato" ou "uns 20 euros" em vez de "Hetzner CX21 EUR 6/mês"
- Scaling path com "vais precisar de mais recursos" sem definir o que muda, quando e a que custo
- Comparar tecnologias com critérios assimétricos (listar 5 vantagens de A e 1 de B)
- Recomendar microservices, Kubernetes ou service mesh para projectos fase 0-1 com equipa <3 devs
- Trade-offs matrix vazia de números — "FastAPI é mais rápido" sem benchmark ou contexto de uso
- Ignorar perfil técnico da equipa: recomendar stack que o cliente não consegue operar sozinho
- Placeholders não substituídos: `<framework>`, `<database>`, `<team-size>` no output final
- Rejeitar alternativas com "é mais complexo" sem quantificar o custo dessa complexidade
- Stack recommendation que muda o tipo de app original sem flag explícita ao cliente

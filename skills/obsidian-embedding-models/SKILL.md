---
name: obsidian-embedding-models
description: Embedding model selection, fine-tuning, evaluation. OpenAI, Cohere, BGE, nomic, sentence-transformers. Triggers em "embedding model", "fine-tune embedding", "OpenAI embeddings", "Cohere embed", "BGE", "nomic-embed".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification]
---

# OBSIDIAN-EMBEDDING-MODELS

## Quando usar
- Escolher embedding model (greenfield)
- A/B test models on YOUR data
- Fine-tune model em domain
- Multilingual setup
- Cost vs quality trade-off (managed vs self-host)

## Landscape (2026)
**Managed:**
- OpenAI text-embedding-3-large (3072 dims, $0.13/M tokens)
- Cohere embed-multilingual-v3 (1024 dims, $0.10/M)
- Voyage AI (multimodal, +finance-tuned)

**Open-source SOTA:**
- BGE-m3 (BAAI, multilingual, 1024 dims)
- mxbai-embed-large (1024 dims, English líder)
- nomic-embed-text-v1.5 (768 dims, Matryoshka)
- gte-large (Alibaba, 1024 dims)
- jina-embeddings-v3 (long-context 8K)

## Critérios de seleção
- **MTEB benchmark:** standard reference
- **Domain match:** finance/medical/legal precisam tuned
- **Language coverage:** PT-BR é tricky
- **Dimensions:** 384/768/1024/3072 (storage trade-off)
- **Long-context:** >2K tokens precisa late chunking
- **Cost:** managed vs self-host TCO

## Fine-tuning
- **MTEB benchmark:** standard reference para SOTA
- **MultipleNegativesRankingLoss:** contrastive standard
- **Train data:** anchor-positive pairs (5K-50K) suficiente
- **Hardware:** A100 ~4-8h
- **Eval:** holdout test set + production A/B

## Templates
1. Embedding model selection scorecard
2. Fine-tuning pipeline (sentence-transformers)
3. MTEB evaluation runner
4. Production A/B test setup
5. Embedding version migration plan

## Cross-references
- [[obsidian-semantic-search]] · [[obsidian-rag-corpus-engineering]] · [[demeter-ml-pipelines]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-embedding-models** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-embedding-models:**

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

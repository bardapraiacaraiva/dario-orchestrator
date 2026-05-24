---
name: obsidian-knowledge-compaction
description: Knowledge compaction — summarization, distillation, progressive summarization, abstract generation. Triggers em "summarization", "compaction", "progressive summarization", "distill", "abstract generation".
license: MIT
parent_agent: obsidian-director
compliance: [data_classification, audit_trail]
---

# OBSIDIAN-KNOWLEDGE-COMPACTION

## Quando usar
- Long-form → executive summary
- RAG context window optimization (compactar antes de retrieve)
- Newsletter / digest generation
- Meeting notes → action items
- Research synthesis (N papers → 1 summary)

## Técnicas
- **Progressive summarization (Forte):** highlight → bold → 1-liner
- **Extractive:** top sentences (TextRank, BERT)
- **Abstractive:** LLM-generated novel sentences
- **Hierarchical:** summary of summaries (recursive)
- **Query-focused:** sumariza apenas o relevante para pergunta X
- **Map-reduce:** chunks paralelos → merge final

## Stack
- **LangChain summarization chains** (stuff / map_reduce / refine)
- **LlamaIndex** (response synthesis modes)
- **Anthropic Contextual retrieval:** chunk + situated summary
- **OpenAI GPT-4o** + Claude Opus para abstractive
- **BART / Pegasus** para extractive/abstractive open-source

## Templates
1. Progressive summarization markup convention
2. Map-reduce summarization pipeline
3. Query-focused summarization prompt
4. Meeting notes → action items extractor
5. Research synthesis workflow (N papers → matrix → narrative)

## Métricas
- **ROUGE-1/2/L:** automatic vs reference (limitations)
- **Faithfulness:** factual em relação ao source (LLM-judge)
- **Compression ratio:** input/output token ratio
- **Information retention:** can answer same Qs from summary?

## Cross-references
- [[obsidian-rag-corpus-engineering]] · [[orion-product-discovery]] · [[demeter-data-storytelling]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **obsidian-knowledge-compaction** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in obsidian-knowledge-compaction:**

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

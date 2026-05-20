---
name: prometheus-paper-tracker
description: Sweep arXiv + Anthropic blog + key ML conferences para papers relevantes para LLM agents, memory, dispatch, evaluation. Triggers em "scan papers", "novos papers", "arxiv weekly", "novidades anthropic blog".
license: SEE-LICENSE
parent_agent: prometheus-director
compliance: [audit_immutable, research_integrity]
category: "Sensor — Research & Papers"
version: "1.0"
autonomy_tier: 0
---

# PROMETHEUS-PAPER-TRACKER

**Output only.** Não implementa papers. Flagga os accionáveis.

**Diferenciação vs `oraculo-paper-reading-extraction`:**
- `oraculo` = deep extraction quando user já identificou paper
- **PROMETHEUS** = sweep BREADTH semanal, flag o que merece atenção do ORACULO

## Sources

### Primary (Anthropic)
- `anthropic.com/news` — blog official (filter: research papers)
- `anthropic.com/research` — research output
- `anthropic.com/engineering` — engineering blog
- `youtube.com/@AnthropicAI` — talks & demos

### arXiv — categorias relevantes
- `cs.AI` — AI general
- `cs.CL` — computational linguistics / NLP
- `cs.LG` — machine learning
- `cs.MA` — multi-agent systems

Query filters (RSS):
- "language agents"
- "agentic workflows"
- "LLM memory"
- "tool use"
- "model context protocol"
- "retrieval augmented generation"
- "agent evaluation"
- "constitutional AI"
- "RLHF"
- "Sonnet" OR "Opus" OR "Claude" OR "GPT-5" OR "Gemini 3"

### Conferences (proceedings & accept lists)
- ICLR (annually, ~3000 papers — only attend list dump)
- NeurIPS (annually, ~4000 papers)
- ICML
- ACL
- COLM (Conference on Language Models — newer, very relevant)

### Industry research blogs
- `openai.com/research`
- `deepmind.google/research`
- `microsoft.com/en-us/research/blog/`
- `huggingface.co/blog` (engineering + research mix)
- `lilianweng.github.io/` (Lilian Weng's curated takes)
- `simonwillison.net` (Simon Willison — daily LLM tracking)

## Workflow

```
1. arXiv RSS digest:
   curl -s "https://export.arxiv.org/api/query?search_query=cat:cs.CL+AND+abs:agent&max_results=20&sortBy=submittedDate&sortOrder=descending"
   → extract titles, abstracts, authors

2. Anthropic blog scrape (HTML parse):
   curl -s "https://www.anthropic.com/news" | grep -oE 'href="/news/[^"]+"' | head -10

3. Diff vs state/seen_papers.yaml

4. Para cada paper NEW:
   a. Filter by abstract relevance (keyword match): agent / memory / dispatch / eval / RAG / chain / tool use
   b. Auto-summarize abstract (1-line)
   c. Score relevance to DARIO modules:
      - Memory & Dreaming subsystem
      - Skill dispatch / routing
      - Quality scoring / evaluation
      - Multi-agent orchestration
      - RAG / retrieval

5. Output: digests/YYYY-WW-papers.md
6. Update state/seen_papers.yaml
```

## Signal filter — DARIO relevance

| Tópico | Aplicabilidade DARIO | Tag default |
|---|---|---|
| Agent memory architectures | 🔥 directo — dream subsystem v2 |
| Q-value learning / RL for dispatch | 🔥 directo — qvalue_memory_wire |
| Constitutional AI / governance | ⚠️ ethical_gate evolution |
| Tool use / function calling | ⚠️ skill chains evolution |
| Multi-agent coordination | ⚠️ orchestrator core |
| Long-context / 1M+ context | 💤 nice-to-know, sem acção |
| Fine-tuning techniques | 💤 não fine-tunamos models |
| New benchmark releases (GAIA, AgentBench, etc.) | 🔥 golden_eval new test cases |
| Anthropic model release (Sonnet 5, Opus 5, etc.) | 🔥 model migration playbook |

## Commands

```bash
# arXiv recent papers (cs.CL com "agent" no abstract, últimas 7 dias)
curl -s "https://export.arxiv.org/api/query?search_query=cat:cs.CL+AND+abs:agent&max_results=30&sortBy=submittedDate&sortOrder=descending" \
  | xmlstarlet sel -t -m "//entry" -v "title" -o "|" -v "summary" -n

# Anthropic blog latest
curl -s "https://www.anthropic.com/news" \
  | grep -oE 'href="/news/[^"]+"' \
  | sort -u | head -20

# Simon Willison's blog feed
curl -s "https://simonwillison.net/atom/everything/" \
  | xmlstarlet sel -t -m "//entry" -v "title" -n
```

## State file

`~/.claude/orchestrator/prometheus/state/seen_papers.yaml`:

```yaml
last_scan: "YYYY-MM-DDTHH:MM:SS+00:00"
sources_scanned: [arxiv, anthropic-news, simonw-blog]
papers_seen:
  - arxiv_id: "2405.12345"
    title: "Memory-Augmented Language Agents"
    seen_at: "2026-05-20"
    relevance: high
    tag: 🔥
  # ... etc
total_seen: N
```

## Output exemplo

```markdown
## prometheus-paper-tracker — 2026-W21

Scanned: 5 sources · 47 papers · 4 flagged after filter

### 🔥 HIGH
- **"Sleep-Time Compute for Language Agents"** (Anthropic, 2026-05-18)
  - Abstract: extends memory consolidation during agent idle time...
  - DARIO module: extends dream subsystem (já temos 4-fase consolidation diária)
  - Action: ler full paper, comparar com nossa implementação

- **"Q-Learning over Sparse Skill Graphs"** (Google DeepMind, 2026-05-15)
  - Abstract: improves dispatch in multi-skill environments...
  - DARIO module: qvalue_memory_wire (já implementado mas pode ser melhor)
  - Action: review vs current Q-table

### ⚠️ MEDIUM
- 2 papers sobre new benchmarks

### 💤 LOW
- 41 papers (counted, not detailed) — most fine-tuning / niche
```

## Cross-references

[[prometheus-director]] · [[oraculo-paper-reading-extraction]] · [[memory-dream-subsystem]]

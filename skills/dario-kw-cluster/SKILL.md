---
name: dario-kw-cluster
description: Semantic keyword clustering — groups keywords by intent and topic into content clusters for site architecture and content planning. Pairs with seo-dataforseo for live volume data. Triggers on "keyword cluster", "topic cluster", "keyword map", "content cluster", "keyword grouping", "pillar page".
license: MIT
---

# DARIO Skill — Keyword Clustering

Takes a list of keywords (or a seed topic) and groups them into semantic clusters for content architecture. Each cluster becomes a pillar page + supporting articles + internal linking map.

## When to activate
- Content strategy from scratch
- Site architecture planning
- After keyword research (from seo-dataforseo or manual)
- Blog editorial calendar design
- URL structure redesign

## Workflow

### 1. Gather keywords
Sources:
- User-provided list
- `/seo-dataforseo` keyword suggestions for seed terms
- GSC queries export
- Competitor keyword analysis
- "People also ask" / related searches

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "semantic keyword clustering content architecture pillar", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "search intent informational transactional navigational", collection: "dario", limit: 5)
```

### 3. Classify intent per keyword
- **Informational** → "how to", "what is", "guide", "tutorial"
- **Navigational** → brand names, specific pages
- **Commercial investigation** → "best", "vs", "review", "top 10"
- **Transactional** → "buy", "price", "coupon", "hire", "contratar"

### 4. Cluster by semantic topic
Group keywords that target the same search intent + topic. Rules:
- Same SERP overlap (>3 shared URLs in top 10) = same cluster
- One cluster = one page (avoid cannibalization)
- Name each cluster by its primary keyword (highest volume)

### 5. Build cluster map

```
Pillar: "design de interiores lisboa" (800/mo)
├── Supporting: "design interiores moderno apartamento" (210/mo)
├── Supporting: "quanto custa design interiores" (170/mo)
├── Supporting: "designer interiores preços portugal" (140/mo)
├── Supporting: "remodelação apartamento lisboa" (390/mo)
└── Supporting: "home staging lisboa" (90/mo)
```

### 6. Content brief per cluster
For each cluster page:
- **Primary KW** + volume + difficulty
- **Secondary KWs** (2-5)
- **Intent** match
- **URL** proposed
- **H1** suggested
- **Content type** (guide, comparison, service page, blog)
- **Word count** target (based on SERP average)
- **Internal links** to/from pillar and siblings

## Output template
```markdown
# Keyword Cluster Map — <Client / Topic>

## Cluster 1: <Primary KW> (vol/mo)
| Keyword | Volume | Difficulty | Intent | Target URL |
|---|---|---|---|---|
| ... | | | | |

**Content brief:** ...
**Internal linking:** pillar ↔ support articles

## Cluster 2: ...
```

## Cannibalization Check

Before finalizing clusters, check for keyword cannibalization:
1. Search each primary keyword on the client's site: `site:domain.com "keyword"`
2. If 2+ pages rank for the same keyword → merge into one or 301 redirect the weaker
3. If zero pages rank → new content opportunity
4. Document in the cluster map: "Existing URL" column with current ranking page if any

## Integration

- Pairs with `seo-dataforseo` for live volume/difficulty data
- Feeds into `seo-plan` for site architecture
- Content briefs feed into `dario-content` for production
- Pillar page structure feeds into `seo-sitemap`

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Keyword Cluster Map.md`

## Red Flags

- Never create a cluster with only 1 keyword — that's a page, not a cluster
- Never assign two clusters to the same URL — one URL, one cluster
- Never skip intent classification — informational and transactional keywords need different pages
- Always validate SERP overlap before merging keywords into a cluster
- Always check existing content first to avoid creating duplicates
- Minimum 3 supporting articles per pillar page for internal linking effectiveness

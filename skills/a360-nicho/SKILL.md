---
name: "A360 Niche Research & Validation"
description: "Deep niche research and market validation — TAM/SAM/SOM sizing, competition mapping, demand signals, viability scoring. Takes a business idea and determines if the market is worth entering."
version: "1.0"
agent: "A360 — Accelera 360"
category: "Phase 1 — Discovery"
---

# A360 Niche Research & Validation

## Triggers

Activate this skill when the user says any of:
- "niche research", "pesquisa de nicho", "market research"
- "TAM SAM SOM", "market size", "tamanho de mercado"
- "competition analysis", "analise concorrencia"
- "demand signals", "sinais de procura"
- "is this niche viable?", "este nicho vale a pena?"
- "validate this market", "validar mercado"
- Any request to evaluate whether a business idea has market potential

## Frameworks & References

- **Eric Ries** (Lean Startup) — validated learning, build-measure-learn
- **Alex Hormozi** ($100M Offers) — market selection criteria: growing, has pain, can afford to pay, easy to target
- **Russell Brunson** (DotCom Secrets) — dream customer identification, market sophistication levels (Eugene Schwartz)
- **Sean Ellis** (Hacking Growth) — growth experiments, North Star Metric
- **Peter Thiel** (Zero to One) — monopoly vs competition, 10x better test

## Workflow

### Step 1: Niche Definition
Capture from the user:
- Business idea / product concept (1-2 sentences)
- Target geography (local, national, global)
- Initial target audience hypothesis
- Budget range for validation (if any)
- Timeline pressure (how fast to revenue?)

### Step 2: Market Sizing (TAM/SAM/SOM)
Calculate using top-down AND bottom-up approaches:

**Top-Down:**
- TAM (Total Addressable Market): entire global market for the category
- SAM (Serviceable Addressable Market): segment you CAN reach with your business model
- SOM (Serviceable Obtainable Market): realistic capture in 12-24 months

**Bottom-Up:**
- Number of potential customers in target segment
- Average revenue per customer (ARPC)
- Purchase frequency per year
- SOM = customers x ARPC x frequency x realistic penetration rate (1-5%)

### Step 3: Demand Signal Analysis
Research and document each signal:

| Signal | Source | Method |
|--------|--------|--------|
| Search volume | Google Trends | Trend direction (rising/stable/declining), seasonality |
| Keyword volume | SEO tools | Monthly searches for core terms, CPC as proxy for commercial intent |
| Forum activity | Reddit, Quora, Facebook Groups | Number of posts, engagement, sentiment |
| Social mentions | Twitter/X, Instagram, TikTok | Hashtag volume, creator activity |
| Competitor funding | Crunchbase, AngelList | Recent raises in the space = investor validation |
| Job postings | LinkedIn, Indeed | Companies hiring in this niche = growth signal |
| Amazon/marketplace | Amazon BSR, Etsy trends | Product demand, review volume, pricing |
| Paid ads | Facebook Ad Library, SpyFu | Active advertisers = proven monetization |

### Step 4: Competition Mapping
Create a competitive landscape matrix:

**Direct Competitors** (same product, same market):
- Name, URL, estimated revenue/traffic
- Positioning statement
- Pricing model and price points
- Key differentiators
- Weaknesses / gaps / complaints (review mining)

**Indirect Competitors** (different product, same problem):
- Alternative solutions the customer uses today
- DIY / status quo alternatives

**Market Sophistication Level** (Eugene Schwartz scale):
1. Unaware — nobody knows the problem exists
2. Problem-aware — know the problem, no solutions yet
3. Solution-aware — solutions exist, yours must differentiate
4. Product-aware — market is crowded, need unique mechanism
5. Most-aware — market is saturated, need identity/brand play

### Step 5: Hormozi Market Selection Criteria
Score the niche on Alex Hormozi's 4 criteria (1-10 each):

| Criterion | Score | Evidence |
|-----------|-------|----------|
| **Growing market** (tailwind) | /10 | Google Trends direction, industry reports |
| **Has massive pain** (desperate buyers) | /10 | Forum posts, complaint volume, urgency signals |
| **Can afford to pay** (purchasing power) | /10 | Average income, B2B budget, existing spend |
| **Easy to target** (reachable audience) | /10 | Congregations, media, associations, lists |

**Minimum viable score: 28/40**. Below this, recommend pivoting.

### Step 6: Blue Ocean Opportunity Scan
Identify potential differentiation angles:
- Underserved sub-segments within the niche
- Feature gaps in competitor offerings
- Pricing model innovation opportunities
- Distribution channel gaps
- Geographic whitespace
- Audience segments competitors ignore

### Step 7: Viability Scorecard

Score each dimension 1-10:

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Market size (SOM > $1M) | 15% | /10 | |
| Growth trajectory | 15% | /10 | |
| Pain intensity | 15% | /10 | |
| Willingness to pay | 15% | /10 | |
| Competition gap | 10% | /10 | |
| Reachability | 10% | /10 | |
| Personal fit / expertise | 10% | /10 | |
| Speed to revenue | 10% | /10 | |
| **TOTAL** | 100% | | **/100** |

**Decision Thresholds:**
- 80-100: GREEN — Strong niche, proceed to Avatar (a360-avatar)
- 60-79: YELLOW — Viable with adjustments, refine positioning
- 40-59: ORANGE — High risk, consider pivot or sub-niche
- 0-39: RED — Do not proceed, find a different niche

## Commands

```bash
# Research Google Trends for niche terms
rtk curl "https://trends.google.com/trends/explore?q=TERM"

# Check keyword volume (if DataForSEO available)
# Use seo-dataforseo skill for live keyword data

# Search Reddit for pain points
rtk curl "https://www.reddit.com/search.json?q=TOPIC&sort=relevance&limit=25"
```

## Output Template

```markdown
# A360 Niche Research Report
## Niche: [NICHE NAME]
## Date: YYYY-MM-DD

### 1. Market Sizing
- **TAM**: $X (global category)
- **SAM**: $X (reachable segment)
- **SOM**: $X (12-month realistic capture)
- **Method**: [top-down / bottom-up / hybrid]

### 2. Demand Signals
| Signal | Finding | Strength |
|--------|---------|----------|
| Google Trends | [direction] | Strong/Medium/Weak |
| Keyword Volume | [X/mo] | Strong/Medium/Weak |
| Forum Activity | [description] | Strong/Medium/Weak |
| Competitor Activity | [description] | Strong/Medium/Weak |
| Paid Ads | [description] | Strong/Medium/Weak |

### 3. Competition Landscape
| Competitor | Revenue Est. | Positioning | Weakness |
|------------|-------------|-------------|----------|
| [Name] | $X | [statement] | [gap] |

**Market Sophistication**: Level X — [description]

### 4. Hormozi Criteria: X/40
| Criterion | Score | Evidence |
|-----------|-------|----------|
| Growing | /10 | [evidence] |
| Pain | /10 | [evidence] |
| Purchasing Power | /10 | [evidence] |
| Targetability | /10 | [evidence] |

### 5. Blue Ocean Opportunities
1. [Opportunity 1]
2. [Opportunity 2]
3. [Opportunity 3]

### 6. Viability Score: X/100
**Verdict**: [GREEN/YELLOW/ORANGE/RED]
**Recommendation**: [proceed / refine / pivot / abandon]

### 7. Next Steps
- [ ] Proceed to a360-avatar for customer profiling
- [ ] Proceed to a360-validacao for smoke testing
- [ ] [Other specific actions]
```

## Red Flags

Stop and warn the user if:
- SOM is below $100K (too small to build a business)
- Google Trends shows consistent decline over 5 years
- Zero active paid advertisers in the space (nobody can monetize)
- All competitors are VC-funded with deep moats (Thiel's competition trap)
- Market sophistication is Level 5 with no differentiation angle
- Hormozi score below 20/40
- User has zero expertise AND zero passion for the niche (personal fit = 0)
- The niche requires regulatory licenses the user does not have
- Customer acquisition cost appears higher than lifetime value at first glance

## Handoff

After completing niche research:
- **If GREEN**: Route to `a360-avatar` to build ideal customer profile
- **If YELLOW**: Refine niche parameters and re-run, or route to `a360-avatar` with caveats
- **If ORANGE/RED**: Brainstorm alternative niches and re-run this skill
- Save output to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - A360 - Niche Research - [NicheName].md`

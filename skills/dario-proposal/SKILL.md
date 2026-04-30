---
name: dario-proposal
description: Commercial proposal generator — 3-option pricing (Blair Enns), scope, timeline, deliverables, value framing. Uses Sales Squad + Agency Model spec + proposal PDF template. Triggers on "proposta", "proposal", "orçamento", "quanto cobrar para", "proposta comercial".
license: MIT
---

# DARIO Skill — Commercial Proposal

## Workflow
1. RAG: `search_kb("proposal pricing three options agency value-based", collection: "dario")`
2. Gather: client need, scope, timeline, budget range
3. Structure 3 options (Blair Enns framework):
   - **Option 1 (Good):** minimum viable, lowest price, DIY elements
   - **Option 2 (Better):** recommended, covers most needs
   - **Option 3 (Best):** premium, done-for-you, includes strategy
4. Value framing: anchor Option 3 high, make Option 2 the obvious choice
5. Include: deliverables table, timeline, payment terms, what's excluded
6. Generate PDF via `generate_pdf.py --template proposal`
7. Save to Obsidian

## Pricing rules (Agency Model spec)
- Calculate real cost first (hours × internal rate)
- Apply 1.5-2.0x markup for margin
- Option 3 = 2.5-5x Option 1 (anchoring)
- Always show value delivered, not hours
- Never present single price (no anchor)

## Proposal Structure

Every proposal follows this exact section order:

1. **Cover Page** — Client name, project title, date, your agency logo and contact. Clean, professional, no clutter.
2. **Executive Summary** — 3-4 sentences: what the client needs, why it matters, what you propose. Written for the decision-maker who won't read the rest.
3. **Understanding** — Demonstrate you understand the client's situation, pain points, goals, and market context. Mirror their language from the briefing call.
4. **Approach** — Your methodology: discovery → strategy → design → development → launch → support. Explain *why* your process delivers results, not just *what* you do.
5. **3 Options Table** — Good / Better / Best pricing (see template below). Each option is self-contained with clear scope.
6. **Timeline** — Milestone-based: kickoff, wireframes, design, development, review rounds, launch. Include calendar dates, not just "Week 1-2".
7. **Investment** — The pricing section. Lead with value, present the 3 options, highlight Option 2 as recommended.
8. **Terms** — Payment schedule, revision rounds included, IP transfer, cancellation policy.
9. **About Us** — Brief agency intro, relevant case studies (2-3), team members assigned to this project, client logos.
10. **Next Steps** — Exactly what happens when they say yes: sign proposal, pay deposit, kickoff call scheduled within 48h.

## 3-Option Pricing Template

| Feature | Option 1 — Essencial | Option 2 — Recomendado | Option 3 — Premium |
|---|---|---|---|
| Pages | 5 pages | 10 pages | 15+ pages |
| Design | Template-based, brand colours | Custom design, 2 revision rounds | Fully bespoke, unlimited revisions |
| Copywriting | Client provides all content | Headlines + CTAs written by us | Full professional copywriting |
| SEO | Basic on-page (meta tags, alt text) | Full on-page SEO + keyword research | On-page + off-page strategy 3 months |
| Mobile | Responsive | Responsive + speed optimisation | Responsive + PWA + AMP |
| Analytics | Google Analytics setup | GA4 + Search Console + dashboards | GA4 + Tag Manager + conversion tracking |
| Blog | Not included | Blog setup + 3 sample posts | Blog + 12 SEO articles (quarterly plan) |
| Support post-launch | 30 days bug fixes | 60 days support + 1 training session | 90 days support + monthly retainer option |
| Hosting setup | Guidance only | We configure hosting | Managed hosting 12 months included |
| **Investment** | **2.500€ – 3.500€** | **5.000€ – 7.500€** | **12.000€ – 18.000€** |
| **Timeline** | **3-4 weeks** | **5-7 weeks** | **8-12 weeks** |

> **Note:** Option 2 is always the recommended option. It delivers the best value-to-investment ratio and is designed to be the natural choice for 70% of clients.

## Value Framing Script

Use these phrases when presenting pricing. Never say "the cost is" or "the price is":

1. **"The investment for Option 2, which we recommend, is..."** — Frames as investment, not cost. Positions Option 2 as the default.
2. **"Based on the value this delivers to your business — more leads, higher conversion, stronger brand presence — this represents..."** — Anchors to business outcomes before revealing the number.
3. **"Clients in your sector typically see a return within 3-6 months, which means this investment pays for itself..."** — Introduces ROI framing to make the price feel smaller relative to expected gains.
4. **"Option 3 is our full-service solution at [price]. Many of our most successful clients choose this because... That said, Option 2 at [price] covers everything most businesses need."** — Present Option 3 first as the anchor, then make Option 2 feel like a bargain by comparison.
5. **"We structured these options so you can choose the level of involvement that's right for you right now — and you can always upgrade later."** — Reduces commitment anxiety and opens the door to future upsells.

## Payment Terms

### Model A: 50/50 Split
- 50% upon proposal acceptance (before any work begins)
- 50% upon project delivery / go-live
- **Pros:** Simple, easy to understand, good cash flow for small projects
- **Cons:** Risk if client delays approvals; large final payment can cause hesitation
- **Best for:** Projects under 5.000€, short timelines (< 4 weeks)

### Model B: 40/30/30 Milestones
- 40% upon proposal acceptance
- 30% upon design approval (midpoint milestone)
- 30% upon project delivery / go-live
- **Pros:** Cash flow aligned with work delivered, reduces client risk perception, creates natural review checkpoints
- **Cons:** Slightly more admin to manage billing
- **Best for:** Projects 5.000€ – 15.000€, standard 6-8 week timelines

### Model C: Monthly Retainer
- Fixed monthly fee for ongoing work (e.g., SEO, content, maintenance)
- Minimum 3-month commitment, billed on the 1st, due within 5 days
- **Pros:** Predictable recurring revenue, deeper client relationship, better resource planning
- **Cons:** Requires clear scope definition to avoid scope creep, client may want to cancel early
- **Best for:** Ongoing services (SEO, social media, maintenance), post-launch support packages

## Exclusions Checklist

Always explicitly state what is **NOT** included to prevent scope creep and disputes:

1. **Web hosting and domain** — Client responsible for hosting fees and domain renewal unless specified in Option 3
2. **Stock photography and video** — Licensed images/footage billed separately at cost or client provides
3. **Content writing** — Unless copywriting is included in the chosen option, client provides all text
4. **Translations** — Multi-language content requires separate quote per language
5. **Ongoing maintenance** — Post-support-period updates, security patches, plugin updates are separate
6. **Email marketing setup** — Newsletter platform, templates, automation sequences quoted separately
7. **Third-party integrations** — CRM, ERP, booking systems, payment gateways beyond standard scope
8. **Print design** — Business cards, brochures, signage — separate deliverable
9. **Social media management** — Content creation, scheduling, community management is a separate retainer
10. **Paid advertising** — Ad spend, campaign management, creative production for ads not included

> **Tip:** Include the exclusions list in the Terms section of every proposal. Clients appreciate transparency and it protects both parties.

## Proposal Delivery Tips

1. **Never send a proposal by email without a call.** Always schedule a 20-30 minute video call to walk through the proposal. Proposals sent cold have < 20% close rate; presented proposals close at 50-70%.
2. **Walk through Option 2 first.** Start with the recommended option, explain why it's the best fit, then briefly mention Option 1 (stripped down) and Option 3 (premium). This anchoring sequence makes Option 2 feel like the natural choice.
3. **Present within 48 hours of the discovery call.** Momentum matters. The longer you wait, the colder the lead gets.
4. **Use screen sharing, not just PDF.** Walk through each section live. Pause at the pricing table and let silence do the work — don't rush to justify.
5. **End with a clear next step and deadline.** "This proposal is valid for 15 days. If you'd like to proceed, I'll send the agreement today and we can kick off next Monday."
6. **Follow up exactly 3 times:** Day 3 (light check-in), Day 7 (add a case study or testimonial), Day 12 (final reminder before expiry). After 3 follow-ups, move on.

## Save Location

Save generated proposals to Obsidian:
- **Path:** `05 - Claude - IA/Outputs/YYYY-MM-DD - Proposta - [ClientName] - [ProjectTitle].md`
- Include frontmatter: `type: proposal`, `client:`, `project:`, `total_value:`, `status: draft`

## Red Flags

Stop and flag to the user if any of these are detected:
- Client wants a proposal before a discovery call (no understanding of scope)
- Budget expectation is less than 50% of your calculated minimum cost
- Client asks for "just a quick quote" with no defined scope or deliverables
- Project scope keeps changing during the proposal phase (scope creep before signing)
- Client wants to pay 100% on delivery (zero upfront commitment)
- Client requests unlimited revisions without additional cost
- Timeline is unrealistic for the scope (e.g., full website in 1 week)
- Client mentions they are "getting quotes from 5+ agencies" (price shopping, not value buying)

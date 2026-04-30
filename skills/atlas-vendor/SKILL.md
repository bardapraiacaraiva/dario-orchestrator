---
name: atlas-vendor
description: Vendor Management & Procurement for events -- vendor database, RFP templates, evaluation matrix, contract essentials, preferred vendor lists, multi-vendor coordination, payment tracking. Portuguese specifics including insurance, IVA, Alvara, HACCP. Triggers on "vendor", "fornecedor", "procurement", "RFP", "proposta fornecedor", "contratar servico", "avaliar fornecedor", "vendor management".
license: MIT
---

# ATLAS Skill -- Vendor Management & Procurement

End-to-end vendor lifecycle management for events: sourcing, evaluating, contracting, coordinating, and reviewing suppliers. Builds and maintains a preferred vendor ecosystem that delivers consistent quality across all event categories. Covers Portuguese regulatory requirements (Alvara, insurance, HACCP) and IVA implications for event services.

## When to activate

Invoke `/atlas-vendor` (or trigger automatically) when:
- User needs to source vendors for an event (AV, catering, decor, transport, security, etc.)
- User wants to create or send an RFP to suppliers
- User needs to evaluate competing vendor proposals
- User wants to build or update a preferred vendor list
- User needs vendor contract templates or review
- Multi-vendor coordination is required for an event
- User asks about Portuguese vendor compliance (insurance, Alvara, HACCP)

Do NOT use when:
- Catering-specific deep planning (use `atlas-catering`)
- Transport-specific logistics (use `atlas-transport`)
- Staff hiring/management (use `atlas-staff`)
- Venue selection (use `atlas-venue`)

## Workflow

### 1. Gather vendor requirements
From event brief or user input:
- **Event type and scale** -- corporate, social, wedding, conference, festival
- **Service categories needed** -- AV, catering, decor, lighting, transport, security, photography, entertainment, floristry, furniture rental
- **Budget envelope** -- total and per-category allocation
- **Event date and timeline** -- including load-in, event, load-out
- **Venue constraints** -- approved vendor lists, insurance requirements, access restrictions
- **Quality tier** -- standard, premium, luxury
- **Special requirements** -- sustainability, cultural sensitivity, language capabilities

If key inputs are missing, request them before proceeding.

### 2. Vendor database structure
Maintain structured vendor records:

| Field | Description | Example |
|---|---|---|
| Vendor ID | Unique identifier | VND-AV-001 |
| Company name | Legal name | SomTech Audiovisual Lda |
| Trading name | Brand name | SomTech Events |
| Category | Primary service | AV & Sound |
| Sub-categories | Additional services | Lighting, LED walls, streaming |
| Contact person | Primary contact | Joao Silva |
| Phone / Email | Direct line | +351 91X XXX XXX |
| NIF | Tax identification | 51XXXXXXX |
| Portfolio URL | Website/portfolio | somtech.pt/portfolio |
| Pricing tier | Budget/Mid/Premium | Premium |
| Day rate range | Typical pricing | 2,500-8,000 EUR |
| Rating (1-5) | Internal score | 4.5 |
| Insurance status | Valid/expired/none | Valid until 2027-03 |
| Insurance type | RC, acidentes trabalho | RC 500k + AT |
| Alvara | License number if required | Alvara 12345-IMPIC |
| HACCP | Certification if F&B | HACCP cert. valid 2026-12 |
| Certifications | ISO, sustainability | ISO 9001, Green Events |
| Capacity | Max simultaneous events | 3 events/weekend |
| Lead time | Minimum booking notice | 4 weeks |
| Payment terms | Standard terms | 50% advance, 50% post-event |
| Last event | Most recent collaboration | Gala XYZ, 2026-03 |
| Notes | Internal observations | Excellent LED walls, slow on quotes |

### 3. RFP template

```markdown
# Request for Proposal -- [Service Category]

## Event Overview
- **Event:** [Name]
- **Client:** [Organization]
- **Date:** [DD/MM/YYYY]
- **Venue:** [Name + Address]
- **Expected attendance:** [Number]
- **Event type:** [Conference / Gala / Wedding / Festival / Corporate]

## Scope of Work
[Detailed description of services required, including:]
- Specific deliverables
- Technical specifications
- Quantity requirements
- Quality standards expected

## Timeline
| Milestone | Date |
|---|---|
| RFP issued | DD/MM/YYYY |
| Site visit (optional) | DD/MM/YYYY |
| Questions deadline | DD/MM/YYYY |
| Proposal submission deadline | DD/MM/YYYY |
| Vendor selection announced | DD/MM/YYYY |
| Contract signed | DD/MM/YYYY |
| Load-in | DD/MM/YYYY |
| Event day(s) | DD/MM/YYYY |
| Load-out | DD/MM/YYYY |

## Budget Range
- Budget envelope: EUR [X] - [Y] (excluding IVA)
- Please provide itemized pricing

## Submission Requirements
1. Company profile and relevant experience (3 similar events)
2. Itemized pricing breakdown
3. Team proposed (names, roles, experience)
4. Equipment list with specifications
5. Insurance certificates (RC + Acidentes de Trabalho)
6. Alvara / certifications (if applicable)
7. References (minimum 3, contactable)
8. Cancellation and force majeure terms
9. Sustainability practices (if applicable)

## Evaluation Criteria
| Criterion | Weight |
|---|---|
| Quality & experience | 30% |
| Price competitiveness | 25% |
| Relevant experience | 20% |
| Reliability & references | 15% |
| Innovation & added value | 10% |

## Terms
- All prices in EUR, excluding IVA
- Proposals valid for minimum 30 days
- [Organization] reserves the right to reject all proposals
```

### 4. Evaluation matrix
Score each vendor (0-10 per criterion, weighted):

| Criterion | Weight | Vendor A | Vendor B | Vendor C |
|---|---|---|---|---|
| Quality of proposal | 30% | X | X | X |
| Price competitiveness | 25% | X | X | X |
| Relevant experience | 20% | X | X | X |
| Reliability (references) | 15% | X | X | X |
| Innovation / added value | 10% | X | X | X |
| **Weighted total** | **100%** | **X.X** | **X.X** | **X.X** |

Scoring guide:
- 9-10: Exceptional, exceeds requirements
- 7-8: Strong, meets all requirements
- 5-6: Adequate, meets minimum requirements
- 3-4: Weak, gaps in key areas
- 1-2: Unacceptable, does not meet requirements

### 5. Contract essentials checklist
Every vendor contract must include:

| Section | Key Elements |
|---|---|
| Parties | Full legal names, NIF, addresses |
| Scope | Detailed deliverables, specifications, quantities |
| Timeline | Load-in, event, load-out, rehearsal times |
| Pricing | Itemized costs, IVA treatment, what is/is not included |
| Payment terms | Schedule (typically 30-50% advance, balance post-event) |
| Cancellation | By client (sliding scale), by vendor (replacement + penalty) |
| Force majeure | Definition, notification period, remedies |
| Insurance | Minimum RC coverage, proof before event |
| Liability | Damage caps, indemnification, property damage |
| IP rights | Content created during event, photo/video usage rights |
| Confidentiality | Client data, event details, guest information |
| Subcontracting | Approval required, liability remains with vendor |
| Dispute resolution | Jurisdiction (Portuguese courts), mediation first |
| Signatures | Both parties, date, two copies minimum |

### 6. Preferred vendor list management
- **Building:** 3 vendors minimum per category, scored after each event
- **Annual review:** Performance review in January, remove vendors below 3.0/5.0 average
- **Performance tracking:** score after every event (quality, punctuality, communication, value)
- **Categories to maintain:** AV/Sound, Lighting, Catering, Decor/Floristry, Photography/Video, Transport, Security, Furniture Rental, Printing/Signage, Entertainment, Staffing Agencies, Cleaning

### 7. Multi-vendor coordination protocol

| Phase | Action |
|---|---|
| 8 weeks before | Shared production timeline distributed to all vendors |
| 4 weeks before | All-vendor coordination call (or Teams/Zoom) |
| 2 weeks before | Final timeline with load-in slots confirmed |
| 1 week before | Contact sheet distributed (all vendor leads + phones) |
| Day before | Load-in according to schedule, production manager on-site |
| Event day | Morning briefing, radio/WhatsApp channel active |
| Post-event | Load-out schedule, damage check, feedback forms |

Load-in priority order (typical):
1. Staging / structure
2. AV / sound / lighting
3. Furniture / decor
4. Catering setup
5. Floristry / final touches

### 8. Portuguese vendor compliance

| Requirement | When Mandatory | Verification |
|---|---|---|
| Seguro de Responsabilidade Civil (RC) | All vendors on-site | Request certificate, verify dates |
| Seguro de Acidentes de Trabalho | All vendors with staff on-site | Mandatory by law, verify coverage |
| Alvara IMPIC | Construction, staging, structures | Verify at impic.pt |
| HACCP certification | All F&B vendors | Certificate + inspection records |
| IVA registration | All vendors | Verify NIF on Portal das Financas |
| Licenca de atividade | Security companies (MAI) | Verify MAI license number |
| Certificado PME | Optional, preference in public events | IAPMEI certification |

**IVA considerations for events:**
- Standard rate: 23% (most services)
- Reduced rate: 13% (catering/restaurant services in some contexts)
- Reverse charge: applicable for some international vendors
- Always confirm if vendor quotes include or exclude IVA

### 9. Payment tracking

| PO Number | Vendor | Service | Amount (ex-IVA) | IVA | Total | Invoice Received | Payment Due | Paid | Notes |
|---|---|---|---|---|---|---|---|---|---|
| PO-001 | SomTech | AV package | 5,000 | 1,150 | 6,150 | Yes | DD/MM | Yes | 50% advance paid |

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-vendor
event_date: <YYYY-MM-DD>
total_vendor_budget: <EUR>
vendor_count: <number>
---

# Vendor Management Plan -- <Event Name>

## Vendor Requirements Summary
| Category | Required | Budget (EUR) | Status |
|---|---|---|---|
| AV & Sound | Yes | X,XXX | RFP sent |
| Catering | Yes | X,XXX | Contracted |
| Decor & Floristry | Yes | X,XXX | Evaluating |
| Photography | Yes | X,XXX | Pending |
| Transport | Yes | X,XXX | Not started |
| Security | Yes | X,XXX | Not started |

## RFPs Issued
[RFP details per category]

## Vendor Evaluation Results
[Evaluation matrix per category]

## Contracted Vendors
| Vendor | Category | Contract Value | Payment Terms | Insurance | Status |
|---|---|---|---|---|---|
| [Name] | [Cat] | EUR X,XXX | 50/50 | RC + AT valid | Signed |

## Multi-Vendor Timeline
[Shared production timeline]

## Payment Schedule
[Payment tracking table]

## Compliance Checklist
- [ ] All vendor insurance certificates collected
- [ ] Alvara verified for staging/structure vendors
- [ ] HACCP certificates for all F&B vendors
- [ ] Contact sheet distributed to all vendors
- [ ] Load-in schedule confirmed with venue
- [ ] All contracts signed and countersigned

## Risk Register
| Risk | Impact | Mitigation |
|---|---|---|
| Vendor no-show | Critical | Backup vendor identified per category |
| Equipment failure | High | Vendor provides backup equipment clause |
| Over-budget | Medium | 10% contingency in each category |

## Next Steps
- [ ] Finalize pending RFPs
- [ ] Schedule all-vendor coordination call
- [ ] Confirm load-in schedule with `atlas-timeline`
- [ ] Brief vendors using `atlas-briefing` template
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Vendor Management Plan.md`

## Red Flags
- Never contract a vendor without valid Seguro de Responsabilidade Civil and Seguro de Acidentes de Trabalho -- if an accident occurs on-site the event organizer becomes personally liable
- Never accept verbal-only agreements -- every vendor must have a signed contract with scope, price, cancellation terms, and insurance before the event date
- Never skip reference checks -- contact at least 2 previous clients before contracting any vendor over 2,000 EUR
- Never accept 100% prepayment -- standard is 30-50% advance maximum, balance on delivery or post-event; full prepayment removes all leverage for quality enforcement
- Never assume a vendor is available -- always confirm capacity for the specific event date, especially for peak season (May-October in Portugal) and holiday weekends
- Never allow a vendor to subcontract without prior written approval -- the team that showed up to the tasting or demo must be the team that shows up on event day
- Never skip the load-in schedule coordination -- two vendors arriving simultaneously at a narrow venue entrance creates cascading delays that compress setup time for everyone

## Interactions
- Feeds vendor briefs to `atlas-briefing` for event-day preparation
- Coordinates with `atlas-timeline` for production schedule and load-in slots
- Works with `atlas-budget` for vendor cost allocation and payment tracking
- Catering vendors hand off to `atlas-catering` for menu and service details
- Transport vendors hand off to `atlas-transport` for fleet logistics
- Staff agency vendors hand off to `atlas-staff` for crew management
- Warehouse/rental vendors coordinate with `atlas-warehouse` for equipment tracking
- Compliance checks feed into `atlas-compliance` for regulatory verification
- Save via `dario-obsidian-save` to vault

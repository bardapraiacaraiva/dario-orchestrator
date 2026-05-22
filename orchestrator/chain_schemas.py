"""Chain artifact schemas — required/optional fields per skill.

Extracted from chain_executor.py (Onda 5 #2). This is the JSON-shape
schema dict (distinct from artifact_schemas.SCHEMAS which targets markdown
section presence). Used by chain_validator + chain_graph.
"""

DEFAULT_SCHEMAS: dict[str, dict[str, list[str]]] = {
    "dario-brand": {
        "required": [
            "archetype",
            "positioning_statement",
            "tone_of_voice",
            "differentiators"
        ],
        "optional": [
            "tagline",
            "brand_values",
            "messaging_hierarchy",
            "competitor_gaps"
        ]
    },
    "dario-naming": {
        "required": [
            "recommended_name",
            "alternatives",
            "domain_available"
        ],
        "optional": [
            "linguistic_analysis",
            "inpi_notes",
            "social_handles"
        ]
    },
    "dario-offer": {
        "required": [
            "offer_title",
            "value_equation",
            "pricing",
            "guarantee"
        ],
        "optional": [
            "bonuses",
            "urgency_mechanism",
            "risk_reversal"
        ]
    },
    "dario-sales-letter": {
        "required": [
            "headline",
            "lead",
            "body",
            "cta"
        ],
        "optional": [
            "ps_lines",
            "testimonial_slots",
            "word_count"
        ]
    },
    "dario-email-seq": {
        "required": [
            "sequence_type",
            "email_count",
            "emails"
        ],
        "optional": [
            "send_schedule",
            "segment_rules"
        ]
    },
    "dario-diagnose": {
        "required": [
            "critico",
            "importante",
            "otimizacao",
            "overall_score"
        ],
        "optional": [
            "quick_wins",
            "url_analyzed",
            "tech_stack"
        ]
    },
    "seo-audit": {
        "required": [
            "score",
            "critical_issues",
            "recommendations"
        ],
        "optional": [
            "pages_crawled",
            "schema_gaps",
            "competitor_comparison"
        ]
    },
    "seo-local": {
        "required": [
            "gbp_optimized",
            "nap_format",
            "citations_list",
            "review_strategy"
        ],
        "optional": [
            "schema_jsonld",
            "competitor_local",
            "categories"
        ]
    },
    "seo-plan": {
        "required": [
            "site_architecture",
            "keyword_map",
            "content_calendar"
        ],
        "optional": [
            "link_strategy",
            "hreflang_plan",
            "schema_plan"
        ]
    },
    "dario-story-circle": {
        "required": [
            "origin_story",
            "about_page_copy",
            "short_bio"
        ],
        "optional": [
            "8_beats",
            "brand_narrative_arc"
        ]
    },
    "diva-briefing": {
        "required": [
            "requirements",
            "style_preferences",
            "budget_range",
            "timeline"
        ],
        "optional": [
            "restrictions",
            "inspiration_refs",
            "priority_rooms"
        ]
    },
    "diva-budget": {
        "required": [
            "total_estimate",
            "phases",
            "cost_per_m2"
        ],
        "optional": [
            "contingency",
            "payment_schedule",
            "alternatives"
        ]
    },
    "diva-floor-plan": {
        "required": [
            "layout_description",
            "areas_m2",
            "circulation_score"
        ],
        "optional": [
            "zoning",
            "natural_light_analysis",
            "rgeu_compliance"
        ]
    }
}

__all__ = ["DEFAULT_SCHEMAS"]

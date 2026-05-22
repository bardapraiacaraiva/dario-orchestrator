#!/usr/bin/env python3
"""
DARIO License Manager — Trial enforcement + VIP key activation.
================================================================
Public install (pip/npx) gets 7-day trial with limited features.
VIP key unlocks full access permanently.

Tiers:
    TRIAL   — 7 days, 3 engines, 1 parallel, no API execution, no evolution
    PRO     — unlimited, all engines, 3 parallel, API execution, evolution
    ENTERPRISE — unlimited, all engines, 5 parallel, multi-tenant, federation

Usage:
    python license_manager.py --status          # Show current license
    python license_manager.py --activate KEY    # Activate VIP key
    python license_manager.py --init-trial      # Initialize 7-day trial
    python license_manager.py --check           # Check if license valid (exit 0=ok, 1=expired)
    python license_manager.py --generate-key TIER EMAIL  # Generate VIP key (admin only)
    python license_manager.py --json

Key format: DARIO-XXXX-XXXX-XXXX-TIER
    DARIO-A1B2-C3D4-E5F6-PRO
    DARIO-G7H8-I9J0-K1L2-ENT
"""

import argparse
import hashlib
import json
import logging
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
LICENSE_FILE = ORCH_DIR / "license.json"

# MASTER_SECRET source priority:
#   1. Env var DARIO_MASTER_SECRET (recommended for production)
#   2. ~/.claude/orchestrator/.master_secret file (admin local)
#   3. Placeholder fallback (signs nothing useful — repo-safe)
#
# Whoever holds the real MASTER_SECRET can mint keys. Keep it private.
# Repo distributions ship the placeholder — keys minted with placeholder
# won't validate on installs that have the real secret, and vice versa.
def _load_master_secret() -> bytes:
    env = os.environ.get("DARIO_MASTER_SECRET")
    if env:
        return env.encode("utf-8")
    secret_file = ORCH_DIR / ".master_secret"
    if secret_file.exists():
        try:
            return secret_file.read_text(encoding="utf-8").strip().encode("utf-8")
        except Exception:
            pass
    return b"DARIO-PLACEHOLDER-NOT-FOR-PRODUCTION-REPLACE-IN-ENV"


MASTER_SECRET = _load_master_secret()

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("license")

TIERS = {
    "trial": {
        "name": "Trial (7 dias — acesso completo DARIO + DIVA + LEX-BR)",
        "duration_days": 7,
        "max_parallel": 3,
        "engines_allowed": "all",
        # LEX-BR — trial dá acesso aos 15 skills + 3 MCP servers + 50 peças
        # Após 7 dias: tudo bloqueado até VIP key ou expira definitivamente
        "lex_br_skills_count": 15,
        "lex_br_mcp_servers": ["jusbrasil", "cnj_datajud", "stf"],
        "lex_br_pieces_month": 50,
        "features": {
            "api_execution": True,
            "evolution_engine": True,
            "llm_judge": True,
            "predictive_dispatch": True,
            "chain_executor": True,
            "multi_tenancy": True,
            "federation": True,
            "plugins": True,
            "adaptive_rubrics": True,
            "dashboard": True,
            "task_templates": True,
            # LEX-BR features acessíveis durante trial (acesso completo)
            "lex_br_agent": True,
            "oab_205_gate": True,
            "lgpd_marker": True,
            "audit_oab": True,
            "lex_memory_multi_client": True,
            "dms_integration": True,
        },
    },
    "pro": {
        "name": "Professional",
        "duration_days": None,  # Permanent
        "max_parallel": 3,
        "engines_allowed": "all",
        "features": {
            "api_execution": True,
            "evolution_engine": True,
            "llm_judge": True,
            "predictive_dispatch": True,
            "chain_executor": True,
            "multi_tenancy": False,
            "federation": False,
            "plugins": True,
            "adaptive_rubrics": True,
            "dashboard": True,
            "task_templates": True,
        },
    },
    "enterprise": {
        "name": "Enterprise",
        "duration_days": None,
        "max_parallel": 5,
        "engines_allowed": "all",
        "features": {
            "api_execution": True,
            "evolution_engine": True,
            "llm_judge": True,
            "predictive_dispatch": True,
            "chain_executor": True,
            "multi_tenancy": True,
            "federation": True,
            "plugins": True,
            "adaptive_rubrics": True,
            "dashboard": True,
            "task_templates": True,
        },
    },
    # LEX-BR tiers (v11.2.0+ — agente Direito BR)
    "lex_solo": {
        "name": "LEX-BR Solo (Advogado individual)",
        "price_brl_month": 297,
        "duration_days": None,
        "max_parallel": 2,
        "engines_allowed": "lex_br_subset",
        "lex_br_skills_count": 15,
        "lex_br_mcp_servers": ["jusbrasil", "cnj_datajud", "stf"],
        "lex_br_pieces_month": 50,
        "features": {
            "api_execution": True, "llm_judge": True, "chain_executor": True,
            "plugins": True, "adaptive_rubrics": True, "dashboard": True,
            "task_templates": True, "lex_br_agent": True,
            "oab_205_gate": True, "lgpd_marker": True, "audit_oab": True,
            "evolution_engine": False, "predictive_dispatch": False,
            "multi_tenancy": False, "federation": False,
        },
    },
    "lex_office": {
        "name": "LEX-BR Office (Escritório < 10 advogados)",
        "price_brl_month": 997,
        "duration_days": None,
        "max_parallel": 3,
        "engines_allowed": "lex_br_full",
        "lex_br_skills_count": 15,
        "lex_br_mcp_servers": ["jusbrasil", "cnj_datajud", "stf", "anpd", "receita_federal"],
        "lex_br_pieces_month": 200,
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "predictive_dispatch": True, "chain_executor": True,
            "plugins": True, "adaptive_rubrics": True, "dashboard": True,
            "task_templates": True, "lex_br_agent": True,
            "oab_205_gate": True, "lgpd_marker": True, "audit_oab": True,
            "lex_memory_multi_client": True, "dms_integration": True,
            "multi_tenancy": False, "federation": False,
        },
    },
    "lex_enterprise": {
        "name": "LEX-BR Enterprise (Escritório/Dept. jurídico)",
        "price_brl_month_from": 4000,
        "duration_days": None,
        "max_parallel": 5,
        "engines_allowed": "all",
        "lex_br_skills_count": 15,
        "lex_br_mcp_servers": ["jusbrasil", "cnj_datajud", "stf", "diario_oficial",
                               "anpd", "receita_federal", "advbox", "projuris"],
        "lex_br_pieces_month": "unlimited",
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "predictive_dispatch": True, "chain_executor": True,
            "multi_tenancy": True, "federation": True,
            "plugins": True, "adaptive_rubrics": True, "dashboard": True,
            "task_templates": True, "lex_br_agent": True,
            "oab_205_gate": True, "lgpd_marker": True, "audit_oab": True,
            "lex_memory_multi_client": True, "dms_integration": True,
            "dpa_anthropic": True, "sla_4h_support": True,
        },
    },
    # =========================================================================
    # DEMETER tiers (v11.3.0+) — Data Engineering & Analytics
    # =========================================================================
    "demeter_solo": {
        "name": "DEMETER Solo (Data analyst / growth solo)",
        "price_brl_month": 297,
        "duration_days": None,
        "max_parallel": 1,
        "engines_allowed": ["analytics", "etl_basic"],
        "demeter_skills_count": 8,
        "demeter_dashboards_month": 5,
        "demeter_warehouses": ["postgres", "duckdb", "bigquery_sandbox"],
        "features": {
            "api_execution": True, "demeter_agent": True,
            "data_quality_basic": True, "dbt_core": True,
            "ab_testing_basic": True, "single_warehouse": True,
            "metrics_layer_lite": True, "support_email": True,
        },
    },
    "demeter_team": {
        "name": "DEMETER Team (Data team / startup)",
        "price_brl_month": 997,
        "duration_days": None,
        "max_parallel": 3,
        "engines_allowed": "all",
        "demeter_skills_count": 15,
        "demeter_dashboards_month": 25,
        "demeter_warehouses": ["postgres", "duckdb", "bigquery", "snowflake", "redshift"],
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "demeter_agent": True, "data_quality_full": True,
            "dbt_cloud": True, "ml_pipelines": True,
            "ab_testing_full": True, "realtime_streaming": True,
            "metrics_layer_full": True, "data_catalog": True,
            "predictive_models": True, "support_chat": True,
        },
    },
    "demeter_enterprise": {
        "name": "DEMETER Enterprise (Data org / multi-warehouse)",
        "price_brl_month_from": 4000,
        "duration_days": None,
        "max_parallel": 5,
        "engines_allowed": "all",
        "demeter_skills_count": 15,
        "demeter_dashboards_month": "unlimited",
        "demeter_warehouses": "all",
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "predictive_dispatch": True, "chain_executor": True,
            "multi_tenancy": True, "federation": True,
            "plugins": True, "adaptive_rubrics": True, "dashboard": True,
            "task_templates": True, "demeter_agent": True,
            "data_quality_full": True, "dbt_cloud": True,
            "ml_pipelines_production": True, "ab_testing_full": True,
            "realtime_streaming": True, "metrics_layer_full": True,
            "data_catalog_enterprise": True, "data_lineage": True,
            "model_explainability": True, "drift_detection": True,
            "dpa_anthropic": True, "sla_4h_support": True,
        },
    },
    # =========================================================================
    # ORION tiers (v11.4.0+) — Product Excellence
    # =========================================================================
    "orion_solo": {"name": "ORION Solo (PM solo / founder produto)",
        "price_brl_month": 297, "duration_days": None, "max_parallel": 1,
        "engines_allowed": ["product_core"], "orion_skills_count": 8,
        "features": {"orion_agent": True, "prd_writing": True, "prioritization_basic": True,
            "discovery_lite": True, "single_product": True, "support_email": True}},
    "orion_team": {"name": "ORION Team (Product team / startup)",
        "price_brl_month": 997, "duration_days": None, "max_parallel": 3,
        "engines_allowed": "all", "orion_skills_count": 15,
        "features": {"orion_agent": True, "all_skills": True, "feature_flags_integration": True,
            "beta_program_mgmt": True, "growth_loops": True, "retention_playbooks": True,
            "pricing_strategy": True, "multi_product": True, "support_chat": True}},
    "orion_enterprise": {"name": "ORION Enterprise (Product org)",
        "price_brl_month_from": 4000, "duration_days": None, "max_parallel": 5,
        "engines_allowed": "all", "orion_skills_count": 15,
        "features": {"orion_agent": True, "all_skills": True, "product_ops": True,
            "portfolio_management": True, "executive_dashboard": True,
            "dedicated_strategist": True, "sla_4h_support": True, "dpa_anthropic": True}},
    # =========================================================================
    # OBSIDIAN-CORP tiers (v11.4.0+) — Knowledge Graph & Second Brain
    # =========================================================================
    "obsidian_solo": {"name": "OBSIDIAN-CORP Solo (Knowledge worker individual)",
        "price_brl_month": 297, "duration_days": None, "max_parallel": 1,
        "engines_allowed": ["knowledge_core"], "obsidian_skills_count": 8,
        "features": {"obsidian_agent": True, "second_brain_setup": True, "PARA_method": True,
            "atomic_notes": True, "single_vault": True, "support_email": True}},
    "obsidian_team": {"name": "OBSIDIAN-CORP Team (Knowledge team)",
        "price_brl_month": 997, "duration_days": None, "max_parallel": 3,
        "engines_allowed": "all", "obsidian_skills_count": 15,
        "features": {"obsidian_agent": True, "all_skills": True, "knowledge_graph": True,
            "rag_corpus_mgmt": True, "semantic_search": True, "embedding_models": True,
            "multi_vault_sync": True, "ontology_design": True, "support_chat": True}},
    "obsidian_enterprise": {"name": "OBSIDIAN-CORP Enterprise (Knowledge org)",
        "price_brl_month_from": 4000, "duration_days": None, "max_parallel": 5,
        "engines_allowed": "all", "obsidian_skills_count": 15,
        "features": {"obsidian_agent": True, "all_skills": True, "enterprise_search": True,
            "knowledge_graph_federation": True, "compliance_audit": True,
            "sla_4h_support": True, "dpa_anthropic": True}},
    # =========================================================================
    # MEDIK tiers (v11.4.0+) — Healthcare BR (LGPD-saúde, ANS, ANVISA, CFM)
    # =========================================================================
    "medik_solo": {"name": "MEDIK Solo (Médico/dentista solo)",
        "price_brl_month": 497, "duration_days": None, "max_parallel": 1,
        "engines_allowed": ["healthcare_core"], "medik_skills_count": 8,
        "features": {"medik_agent": True, "lgpd_healthcare_marker": True,
            "cfm_205_gate": True, "tuss_codes": True, "single_clinic": True,
            "support_email": True}},
    "medik_team": {"name": "MEDIK Team (Clínica / corpo clínico)",
        "price_brl_month": 1497, "duration_days": None, "max_parallel": 3,
        "engines_allowed": "all", "medik_skills_count": 15,
        "features": {"medik_agent": True, "all_skills": True, "ans_compliance": True,
            "anvisa_regulatory": True, "telemedicine_protocols": True,
            "emr_integration": True, "clinical_protocols": True, "multi_clinic": True,
            "support_chat": True}},
    "medik_enterprise": {"name": "MEDIK Enterprise (Hospital/Operadora)",
        "price_brl_month_from": 6000, "duration_days": None, "max_parallel": 5,
        "engines_allowed": "all", "medik_skills_count": 15,
        "features": {"medik_agent": True, "all_skills": True, "hospital_management": True,
            "claim_management": True, "rcm_revenue_cycle": True,
            "audit_compliance_full": True, "dpo_dedicated": True,
            "sla_4h_support": True, "dpa_anthropic": True}},
    # =========================================================================
    # CAMPUS tiers (v11.4.0+) — Education BR (MEC, LDB, BNCC, EAD)
    # =========================================================================
    "campus_solo": {"name": "CAMPUS Solo (Educador / curso solo)",
        "price_brl_month": 297, "duration_days": None, "max_parallel": 1,
        "engines_allowed": ["education_core"], "campus_skills_count": 8,
        "features": {"campus_agent": True, "instructional_design": True,
            "assessment_basic": True, "single_course": True, "support_email": True}},
    "campus_team": {"name": "CAMPUS Team (EAD provider)",
        "price_brl_month": 1497, "duration_days": None, "max_parallel": 3,
        "engines_allowed": "all", "campus_skills_count": 15,
        "features": {"campus_agent": True, "all_skills": True, "lms_architecture": True,
            "mec_compliance": True, "bncc_alignment": True, "enade_prep": True,
            "gamification": True, "multi_course": True, "support_chat": True}},
    "campus_enterprise": {"name": "CAMPUS Enterprise (Universidade/Sistema EAD)",
        "price_brl_month_from": 5000, "duration_days": None, "max_parallel": 5,
        "engines_allowed": "all", "campus_skills_count": 15,
        "features": {"campus_agent": True, "all_skills": True, "ead_credenciamento": True,
            "education_analytics_full": True, "certification_engine": True,
            "sla_4h_support": True, "dpa_anthropic": True}},
    # =========================================================================
    # AEGIS tiers (v11.4.0+) — Cybersecurity
    # =========================================================================
    "aegis_solo": {"name": "AEGIS Solo (Solo CISO / pentest professional)",
        "price_brl_month": 1497, "duration_days": None, "max_parallel": 1,
        "engines_allowed": ["security_core"], "aegis_skills_count": 10,
        "features": {"aegis_agent": True, "threat_modeling": True,
            "pentest_methodology": True, "vuln_scan_basic": True,
            "iam_basic": True, "secure_sdlc_lite": True,
            "single_org": True, "support_email": True}},
    "aegis_team": {"name": "AEGIS Team (Security team / SOC / Compliance officers)",
        "price_brl_month": 2997, "duration_days": None, "max_parallel": 3,
        "engines_allowed": "all", "aegis_skills_count": 18,
        "features": {"aegis_agent": True, "all_18_skills": True, "soc_operations": True,
            "siem_integration": True, "edr_xdr_management": True, "iam_zero_trust": True,
            "incident_response_full": True, "iso27001_soc2_prep": True,
            "third_party_risk": True, "supply_chain_slsa": True,
            "breach_simulation_bas": True, "support_chat": True}},
    "aegis_enterprise": {"name": "AEGIS Enterprise (Fortune 500 CISO org / SOC 24×7)",
        "price_brl_month_from": 4997, "duration_days": None, "max_parallel": 5,
        "engines_allowed": "all", "aegis_skills_count": 18,
        "features": {"aegis_agent": True, "all_18_skills": True, "forensics_advanced": True,
            "threat_intel": True, "purple_team_continuous": True, "compliance_full": True,
            "tprm_continuous": True, "sbom_attestation_l4": True,
            "bas_continuous_validation": True, "incident_24x7": True,
            "sla_2h_support": True, "dpa_anthropic": True}},
    # =========================================================================
    # ZENITH tiers (v11.4.0+) — Executive Decision Support
    # =========================================================================
    "zenith_solo": {"name": "ZENITH Solo (Founder / solo executive)",
        "price_brl_month": 997, "duration_days": None, "max_parallel": 1,
        "engines_allowed": ["executive_core"], "zenith_skills_count": 8,
        "features": {"zenith_agent": True, "okr_design": True, "scenario_planning_basic": True,
            "executive_brief": True, "single_org": True, "support_email": True}},
    "zenith_team": {"name": "ZENITH Team (C-level / management team)",
        "price_brl_month": 2997, "duration_days": None, "max_parallel": 3,
        "engines_allowed": "all", "zenith_skills_count": 15,
        "features": {"zenith_agent": True, "all_skills": True, "strategic_planning": True,
            "board_pack_gen": True, "ma_evaluation": True, "war_gaming": True,
            "monte_carlo": True, "competitive_intel": True, "support_chat": True}},
    "zenith_enterprise": {"name": "ZENITH Enterprise (Board / PE / Holding)",
        "price_brl_month_from": 12000, "duration_days": None, "max_parallel": 5,
        "engines_allowed": "all", "zenith_skills_count": 15,
        "features": {"zenith_agent": True, "all_skills": True, "portfolio_decision": True,
            "capital_allocation": True, "succession_planning": True,
            "dedicated_strategist": True, "sla_4h_support": True, "dpa_anthropic": True}},
    # =========================================================================
    # GAIA tiers (v11.5.0+) — Sustainability & ESG
    # =========================================================================
    "gaia_solo": {"name": "GAIA Solo (ESG consultant freelance)",
        "price_brl_month": 1497, "duration_days": None, "max_parallel": 1,
        "engines_allowed": ["esg_core"], "gaia_skills_count": 8,
        "features": {"gaia_agent": True, "carbon_accounting": True,
            "csrd_basic": True, "esg_rating_lite": True,
            "single_org": True, "support_email": True}},
    "gaia_team": {"name": "GAIA Team (Consultorias mid-size, family offices)",
        "price_brl_month": 3997, "duration_days": None, "max_parallel": 3,
        "engines_allowed": "all", "gaia_skills_count": 15,
        "features": {"gaia_agent": True, "all_15_skills": True,
            "csrd_full_esrs": True, "tcfd_scenario_analysis": True,
            "sbti_validation": True, "b_corp_prep": True,
            "esg_due_diligence": True, "transition_planning": True,
            "support_chat": True}},
    "gaia_enterprise": {"name": "GAIA Enterprise (Listed companies B3/Euronext, F500)",
        "price_brl_month_from": 12997, "duration_days": None, "max_parallel": 5,
        "engines_allowed": "all", "gaia_skills_count": 15,
        "features": {"gaia_agent": True, "all_15_skills": True,
            "csrd_reasonable_assurance": True, "double_materiality_advanced": True,
            "audit_trail_assurance_ready": True, "multi_jurisdiction_reporting": True,
            "dedicated_sustainability_lead": True, "sla_4h_support": True,
            "dpa_anthropic": True}},
    # =========================================================================
    # NOMOS tiers (v11.5.0+) — Compliance Regulatório PT
    # =========================================================================
    "nomos_solo": {"name": "NOMOS Solo (Compliance officer, advogado PT)",
        "price_brl_month": 997, "duration_days": None, "max_parallel": 1,
        "engines_allowed": ["regulatory_core"], "nomos_skills_count": 8,
        "features": {"nomos_agent": True, "rgpd_pt_marker": True,
            "ai_act_classification": True, "kyc_aml_basic": True,
            "single_org": True, "support_email": True}},
    "nomos_team": {"name": "NOMOS Team (Departments compliance, mid-market PT)",
        "price_brl_month": 2997, "duration_days": None, "max_parallel": 3,
        "engines_allowed": "all", "nomos_skills_count": 15,
        "features": {"nomos_agent": True, "all_15_skills": True,
            "cmvm_disclosure": True, "bdp_reporting": True,
            "dora_full_compliance": True, "mifid_ii_suitability": True,
            "psd2_open_banking": True, "support_chat": True}},
    # =========================================================================
    # v12.0 — MERCURIUS, ATLAS-FIN, HELIOS, KIRION, SPHINX, EUTERPE, ORACULO
    # =========================================================================
    "mercurius_solo": {"name": "MERCURIUS Solo (Founder/AE solo)", "price_brl_month": 297, "max_parallel": 1, "engines_allowed": ["sales_core"], "duration_days": None},
    "mercurius_team": {"name": "MERCURIUS Team (Sales team 5-50 reps)", "price_brl_month": 997, "max_parallel": 3, "engines_allowed": "all", "duration_days": None},
    "mercurius_enterprise": {"name": "MERCURIUS Enterprise (Sales org 50+ reps)", "price_brl_month_from": 4997, "max_parallel": 5, "engines_allowed": "all", "duration_days": None},
    "atlas_fin_solo": {"name": "ATLAS-FIN Solo (Fintech founder)", "price_brl_month": 997, "max_parallel": 1, "engines_allowed": ["fintech_core"], "duration_days": None},
    "atlas_fin_team": {"name": "ATLAS-FIN Team (Fintechs small-medium)", "price_brl_month": 2997, "max_parallel": 3, "engines_allowed": "all", "duration_days": None},
    "atlas_fin_enterprise": {"name": "ATLAS-FIN Enterprise (Digital banks, BaaS)", "price_brl_month_from": 9997, "max_parallel": 5, "engines_allowed": "all", "duration_days": None},
    "helios_solo": {"name": "HELIOS Solo (Energy consultant, ESCO solo)", "price_brl_month": 1997, "max_parallel": 1, "engines_allowed": ["energy_core"], "duration_days": None},
    "helios_team": {"name": "HELIOS Team (Consultorias energia)", "price_brl_month": 4997, "max_parallel": 3, "engines_allowed": "all", "duration_days": None},
    "helios_enterprise": {"name": "HELIOS Enterprise (Indústrias, utilities, oil&gas)", "price_brl_month_from": 14997, "max_parallel": 5, "engines_allowed": "all", "duration_days": None},
    "kirion_solo": {"name": "KIRION Solo (RE broker, analyst)", "price_brl_month": 997, "max_parallel": 1, "engines_allowed": ["realestate_core"], "duration_days": None},
    "kirion_team": {"name": "KIRION Team (Consultancies, family offices)", "price_brl_month": 2997, "max_parallel": 3, "engines_allowed": "all", "duration_days": None},
    "kirion_enterprise": {"name": "KIRION Enterprise (REITs, developers, banks RE)", "price_brl_month_from": 7997, "max_parallel": 5, "engines_allowed": "all", "duration_days": None},
    "sphinx_solo": {"name": "SPHINX Solo (Senior pentest)", "price_brl_month": 4997, "max_parallel": 1, "engines_allowed": ["cyber_advanced_core"], "duration_days": None},
    "sphinx_team": {"name": "SPHINX Team (Red team / advanced SOC)", "price_brl_month": 12997, "max_parallel": 3, "engines_allowed": "all", "duration_days": None},
    "sphinx_enterprise": {"name": "SPHINX Enterprise (Defense, gov, F500 CISO)", "price_brl_month_from": 29997, "max_parallel": 5, "engines_allowed": "all", "duration_days": None},
    "euterpe_solo": {"name": "EUTERPE Solo (Growth marketer freelance)", "price_brl_month": 297, "max_parallel": 1, "engines_allowed": ["marketing_core"], "duration_days": None},
    "euterpe_team": {"name": "EUTERPE Team (Growth agencies, in-house)", "price_brl_month": 997, "max_parallel": 3, "engines_allowed": "all", "duration_days": None},
    "euterpe_enterprise": {"name": "EUTERPE Enterprise (E-commerce, mass advertisers)", "price_brl_month_from": 3997, "max_parallel": 5, "engines_allowed": "all", "duration_days": None},
    "oraculo_solo": {"name": "ORACULO Solo (Independent researcher, PhD)", "price_brl_month": 997, "max_parallel": 1, "engines_allowed": ["ai_research_core"], "duration_days": None},
    "oraculo_team": {"name": "ORACULO Team (Research labs, R&D)", "price_brl_month": 2997, "max_parallel": 3, "engines_allowed": "all", "duration_days": None},
    "oraculo_enterprise": {"name": "ORACULO Enterprise (AI companies, universities)", "price_brl_month_from": 9997, "max_parallel": 5, "engines_allowed": "all", "duration_days": None},
    "nomos_enterprise": {"name": "NOMOS Enterprise (Bancos PT, seguradoras, fintechs)",
        "price_brl_month_from": 9997, "duration_days": None, "max_parallel": 5,
        "engines_allowed": "all", "nomos_skills_count": 15,
        "features": {"nomos_agent": True, "all_15_skills": True,
            "regulator_simulator": True, "audit_trail_immutable": True,
            "multi_regulator_coordination": True, "dedicated_compliance_advisor": True,
            "sla_2h_support": True, "dpa_anthropic": True}},
}


# =============================================================================
# KEY GENERATION + VALIDATION
# =============================================================================

import hmac
import secrets

TIER_SUFFIXES = {
    "starter": "STR", "pro": "PRO", "enterprise": "ENT",
    # LEX-BR tiers (v11.2.0+)
    "lex_solo": "LXS", "lex_office": "LXO", "lex_enterprise": "LXE",
    # DEMETER tiers (v11.3.0+)
    "demeter_solo": "DMS", "demeter_team": "DMT", "demeter_enterprise": "DME",
    # ORION tiers (v11.4.0+) — Product Excellence
    "orion_solo": "ORS", "orion_team": "ORT", "orion_enterprise": "ORE",
    # OBSIDIAN-CORP tiers (v11.4.0+) — Knowledge Graph
    "obsidian_solo": "OBS", "obsidian_team": "OBT", "obsidian_enterprise": "OBE",
    # MEDIK tiers (v11.4.0+) — Healthcare BR
    "medik_solo": "MDS", "medik_team": "MDT", "medik_enterprise": "MDE",
    # CAMPUS tiers (v11.4.0+) — Education BR
    "campus_solo": "CPS", "campus_team": "CPT", "campus_enterprise": "CPE",
    # AEGIS tiers (v11.4.0+) — Cybersecurity
    "aegis_solo": "AGS", "aegis_team": "AGT", "aegis_enterprise": "AGE",
    # ZENITH tiers (v11.4.0+) — Executive Decision Support
    "zenith_solo": "ZNS", "zenith_team": "ZNT", "zenith_enterprise": "ZNE",
    # GAIA tiers (v11.5.0+) — Sustainability & ESG
    "gaia_solo": "GAS", "gaia_team": "GAT", "gaia_enterprise": "GAE",
    # NOMOS tiers (v11.5.0+) — Compliance PT
    "nomos_solo": "NMS", "nomos_team": "NMT", "nomos_enterprise": "NME",
    # v12.0 squads
    "mercurius_solo": "MES", "mercurius_team": "MET", "mercurius_enterprise": "MEE",
    "atlas_fin_solo": "AFS", "atlas_fin_team": "AFT", "atlas_fin_enterprise": "AFE",
    "helios_solo": "HES", "helios_team": "HET", "helios_enterprise": "HEE",
    "kirion_solo": "KIS", "kirion_team": "KIT", "kirion_enterprise": "KIE",
    "sphinx_solo": "SPS", "sphinx_team": "SPT", "sphinx_enterprise": "SPE",
    "euterpe_solo": "EUS", "euterpe_team": "EUT", "euterpe_enterprise": "EUE",
    "oraculo_solo": "OCS", "oraculo_team": "OCT", "oraculo_enterprise": "OCE",
}
TIER_MAP = {v: k for k, v in TIER_SUFFIXES.items()}


def _hmac_signature(payload: str) -> str:
    """HMAC-SHA256 of payload with MASTER_SECRET. Returns uppercase hex."""
    return hmac.new(MASTER_SECRET, payload.encode("utf-8"),
                    hashlib.sha256).hexdigest().upper()


def generate_key(tier: str, email: str = "") -> str:
    """Generate a license key. Admin only — needs real MASTER_SECRET in env.

    Key format: DARIO-{nonce4}-{sig4}-{sig4}-TIER

    The nonce is random; the signature is HMAC-SHA256(tier:nonce, secret).
    Keys minted with the placeholder secret won't validate on machines that
    set DARIO_MASTER_SECRET — and vice versa. So leave the placeholder in
    public repos and only generate real keys in environments with the env
    var set.

    `email` is stored alongside the key for audit but NOT part of the
    signature payload (so users don't need to remember which email at
    activation time).
    """
    if tier not in TIER_SUFFIXES:
        return None
    suffix = TIER_SUFFIXES[tier]
    nonce = secrets.token_hex(2).upper()  # 4 hex chars
    payload = f"{tier}:{nonce}"
    sig = _hmac_signature(payload)
    return f"DARIO-{nonce}-{sig[0:4]}-{sig[4:8]}-{suffix}"


def validate_key(key: str) -> dict:
    """Validate a license key by recomputing HMAC against MASTER_SECRET.

    Returns {"valid": True, "tier": ...} if signature matches.
    Returns {"valid": False, "reason": ...} otherwise.
    """
    if not key or not key.startswith("DARIO-"):
        return {"valid": False, "reason": "Invalid key format"}

    parts = key.split("-")
    if len(parts) != 5:
        return {"valid": False,
                "reason": "Key must have 5 segments (DARIO-NONCE-SIG-SIG-TIER)"}

    nonce, sig1, sig2, suffix = parts[1], parts[2], parts[3], parts[4].upper()
    if suffix not in TIER_MAP:
        return {"valid": False, "reason": f"Unknown tier suffix: {suffix}"}

    tier = TIER_MAP[suffix]
    payload = f"{tier}:{nonce}"
    expected = _hmac_signature(payload)

    # Constant-time compare to avoid timing leaks
    presented_sig = sig1.upper() + sig2.upper()
    expected_sig = expected[0:8]
    if not hmac.compare_digest(presented_sig, expected_sig):
        return {
            "valid": False,
            "reason": "Signature mismatch (forged key or wrong MASTER_SECRET)",
        }
    return {"valid": True, "tier": tier}


# =============================================================================
# LICENSE FILE
# =============================================================================

def load_license() -> dict:
    """Load current license."""
    if LICENSE_FILE.exists():
        try:
            return json.loads(LICENSE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def save_license(lic: dict):
    """Save license to file."""
    LICENSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    LICENSE_FILE.write_text(json.dumps(lic, indent=2), encoding="utf-8")


TRIAL_FINGERPRINT = ORCH_DIR / ".trial_fingerprint"


def _machine_id() -> str:
    """Return a stable machine identifier for cross-validation.
    Tries Windows MachineGUID, then mac address, then hostname as last resort."""
    try:
        if os.name == "nt":
            import subprocess
            r = subprocess.run(
                ["reg", "query", r"HKLM\SOFTWARE\Microsoft\Cryptography",
                 "/v", "MachineGuid"],
                capture_output=True, text=True, timeout=3,
            )
            for line in (r.stdout or "").splitlines():
                if "MachineGuid" in line:
                    return line.split()[-1]
    except Exception:
        pass
    try:
        import uuid
        return f"mac-{uuid.getnode():012x}"
    except Exception:
        pass
    try:
        import socket
        return f"host-{socket.gethostname()}"
    except Exception:
        return "unknown"


# ─── Onda 7 anti-bypass hardening ────────────────────────────────────────────
# 3-layer trial fingerprint:
#   1. `~/.claude/orchestrator/.trial_fingerprint` (original, visible)
#   2. `~/.dario-trial-{obfuscated-hash}.bin` (home dir, hidden, obfuscated)
#   3. Windows registry `HKCU\Software\DARIO\TrialState` (Windows only)
#
# `_check_fingerprint()` returns `used=True` if ANY of the three is present
# and valid. To bypass, a user has to discover and remove all three —
# substantially harder than just `rm .trial_fingerprint`.


def _home_marker_path() -> Path:
    """Hidden home-dir marker. Filename obfuscated by SHA256(machine_id+SECRET).

    The user cannot guess this filename without `MASTER_SECRET`. Even if they
    inspect ~/, the file looks like a generic dotfile blob.
    """
    machine = _machine_id()
    digest = hashlib.sha256(f"{MASTER_SECRET}:home:{machine}".encode()).hexdigest()
    return Path.home() / f".dario-trial-{digest[:16]}.bin"


def _registry_state() -> dict | None:
    """Read trial state from Windows registry HKCU\\Software\\DARIO\\TrialState.

    Returns the stored dict if present, None otherwise. Always returns None
    on non-Windows.
    """
    if os.name != "nt":
        return None
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\DARIO\TrialState",
                             0, winreg.KEY_READ)
        try:
            raw, _ = winreg.QueryValueEx(key, "fingerprint")
            return json.loads(raw)
        finally:
            winreg.CloseKey(key)
    except FileNotFoundError:
        return None
    except Exception:
        return None


def _registry_write(fp_data: dict) -> bool:
    """Write trial state to Windows registry. Returns True on success."""
    if os.name != "nt":
        return False
    try:
        import winreg
        key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,
                                  r"Software\DARIO\TrialState", 0, winreg.KEY_WRITE)
        try:
            winreg.SetValueEx(key, "fingerprint", 0, winreg.REG_SZ,
                              json.dumps(fp_data))
            return True
        finally:
            winreg.CloseKey(key)
    except Exception:
        return False


def _validate_fingerprint(fp: dict) -> dict:
    """Check signature of a fingerprint dict. Returns dict with `valid` + `tampered`."""
    if not isinstance(fp, dict):
        return {"valid": False, "tampered": True}
    sig_payload = f"{MASTER_SECRET}:{fp.get('machine_id')}:{fp.get('first_init_at')}"
    expected_sig = hashlib.sha256(sig_payload.encode()).hexdigest()
    if fp.get("signature") != expected_sig:
        return {"valid": False, "tampered": True,
                "first_init_at": fp.get("first_init_at")}
    return {"valid": True, "tampered": False,
            "first_init_at": fp.get("first_init_at"),
            "machine_id": fp.get("machine_id")}


def _write_fingerprint() -> dict:
    """Persistent trial-used marker. Survives license.json deletion.

    Onda 7 hardening — writes to 3 locations:
        1. `.trial_fingerprint` in orchestrator dir (legacy compat)
        2. `~/.dario-trial-{hash}.bin` in home dir (obfuscated)
        3. Windows Registry `HKCU\\Software\\DARIO\\TrialState` (Windows only)

    Contains: machine_id + first_init_timestamp + signature.
    """
    now = datetime.now(UTC).isoformat()
    machine = _machine_id()
    sig_payload = f"{MASTER_SECRET}:{machine}:{now}"
    signature = hashlib.sha256(sig_payload.encode()).hexdigest()
    fp = {
        "machine_id": machine,
        "first_init_at": now,
        "signature": signature,
        "note": "Trial activation marker. Do not edit — deletion does NOT grant a new trial.",
    }
    payload = json.dumps(fp, indent=2)

    # Layer 1: orchestrator dir
    ORCH_DIR.mkdir(parents=True, exist_ok=True)
    try:
        TRIAL_FINGERPRINT.write_text(payload, encoding="utf-8")
    except Exception:
        pass

    # Layer 2: home dir (obfuscated)
    try:
        _home_marker_path().write_text(payload, encoding="utf-8")
    except Exception:
        pass

    # Layer 3: Windows registry
    _registry_write(fp)

    return fp


def _check_fingerprint() -> dict:
    """Detect if a trial was already initialized on this machine.

    Onda 7 hardening — checks 3 locations. Returns `used=True` if ANY of
    them has a valid (or tampered) fingerprint. To regain a fresh trial,
    a user would need to delete all three AND not be on a fingerprinted
    machine the registry remembers.
    """
    found_in: list[str] = []
    candidates: list[dict] = []

    # Layer 1: orchestrator dir
    if TRIAL_FINGERPRINT.exists():
        try:
            fp = json.loads(TRIAL_FINGERPRINT.read_text(encoding="utf-8"))
            candidates.append({"source": "orchestrator_dir", "fp": fp})
            found_in.append("orchestrator_dir")
        except Exception:
            # Corrupted — fail-closed (count as used)
            return {"used": True, "corrupted": True, "found_in": ["orchestrator_dir"]}

    # Layer 2: home dir (obfuscated)
    home_marker = _home_marker_path()
    if home_marker.exists():
        try:
            fp = json.loads(home_marker.read_text(encoding="utf-8"))
            candidates.append({"source": "home_dir", "fp": fp})
            found_in.append("home_dir")
        except Exception:
            return {"used": True, "corrupted": True, "found_in": ["home_dir"]}

    # Layer 3: Windows registry
    reg_fp = _registry_state()
    if reg_fp is not None:
        candidates.append({"source": "registry", "fp": reg_fp})
        found_in.append("registry")

    if not candidates:
        return {"used": False}

    # Validate signatures across all found copies. Any tamper flags the whole.
    tampered = False
    first_init = None
    machine_id = None
    for c in candidates:
        v = _validate_fingerprint(c["fp"])
        if v.get("tampered"):
            tampered = True
        if first_init is None:
            first_init = v.get("first_init_at")
            machine_id = v.get("machine_id")

    # Self-heal: if one layer is missing but another has a valid fp,
    # rewrite missing layers so future bypasses are harder.
    if not tampered and len(found_in) < 3:
        valid_fp = next(
            (c["fp"] for c in candidates
             if _validate_fingerprint(c["fp"]).get("valid")),
            None,
        )
        if valid_fp is not None:
            payload = json.dumps(valid_fp, indent=2)
            if "orchestrator_dir" not in found_in:
                try:
                    ORCH_DIR.mkdir(parents=True, exist_ok=True)
                    TRIAL_FINGERPRINT.write_text(payload, encoding="utf-8")
                except Exception:
                    pass
            if "home_dir" not in found_in:
                try:
                    home_marker.write_text(payload, encoding="utf-8")
                except Exception:
                    pass
            if "registry" not in found_in:
                _registry_write(valid_fp)

    return {
        "used": True,
        "tampered": tampered,
        "first_init_at": first_init,
        "machine_id": machine_id,
        "found_in": found_in,
    }


def init_trial(force: bool = False) -> dict:
    """Initialize a 7-day trial license.

    Defence layers (in order):
        1. Local 3-layer fingerprint (Onda 7) — refuses if any layer present.
        2. License server (Onda 8) — when `DARIO_LICENSE_SERVER` is set,
           server is the source of truth. Server says "machine_id already
           activated 5 days ago" → refused even if all local layers were
           wiped (e.g. fresh OS install on the same hardware).

    Use `force=True` only with the dev bypass active.
    """
    # Layer 1: local fingerprint check (Onda 7)
    fp_check = _check_fingerprint()
    if fp_check.get("used") and not force:
        try:
            sys.path.insert(0, str(ORCH_DIR))
            from license_guard import _bypass_active
            if _bypass_active():
                force = True
        except Exception:
            pass

    if fp_check.get("used") and not force:
        return {
            "status": "refused",
            "reason": "trial_already_used",
            "first_init_at": fp_check.get("first_init_at"),
            "tampered": fp_check.get("tampered", False),
            "found_in": fp_check.get("found_in", []),
            "message": (
                "A trial was already used on this machine. "
                "Trials are one-time per machine. "
                "Activate a VIP key: python license_manager.py --activate DARIO-XXXX-XXXX-XXXX-PRO"
            ),
        }

    # Layer 2: license server check (Onda 8)
    server_record: dict | None = None
    try:
        import license_client
        if license_client.is_enabled():
            machine = _machine_id()
            server_record = license_client.activate_trial(machine)
            if server_record and not force:
                # Server may say this machine_id was already activated
                # in the past. Server is the source of truth.
                if server_record.get("status") == "expired":
                    return {
                        "status": "refused",
                        "reason": "server_trial_expired",
                        "first_init_at": server_record.get("first_init_at"),
                        "expires_at": server_record.get("expires_at"),
                        "message": (
                            "The license server records a previous trial on "
                            "this machine that has expired. Activate a VIP key."
                        ),
                    }
                if (server_record.get("status") == "active"
                        and server_record.get("days_remaining", 0) < 7
                        and server_record.get("heartbeat_count", 0) > 1):
                    # Server records an existing trial in progress — return it
                    # rather than restarting the clock.
                    pass  # fall through; we'll persist server values below
    except Exception as e:
        # Server unreachable / misconfigured — fall back to local-only.
        try:
            log.warning(f"[license-server] activation failed, offline mode: {e}")
        except Exception:
            pass
        server_record = None

    # Construct the local license — prefer server values when present.
    now = datetime.now(UTC)
    if server_record:
        activated_at = server_record.get("first_init_at", now.isoformat())
        expires_at = server_record.get("expires_at") or \
            (now + timedelta(days=7)).isoformat()
        server_token = server_record.get("token")
    else:
        activated_at = now.isoformat()
        expires_at = (now + timedelta(days=7)).isoformat()
        server_token = None

    lic = {
        "tier": "trial",
        "name": TIERS["trial"]["name"],
        "key": None,
        "email": None,
        "activated_at": activated_at,
        "expires_at": expires_at,
        "max_parallel": TIERS["trial"]["max_parallel"],
        "features": TIERS["trial"]["features"],
        "engines_allowed": TIERS["trial"]["engines_allowed"],
        "status": "active",
        "server_token": server_token,
        "server_bound": server_token is not None,
    }
    save_license(lic)

    # Write all 3 local fingerprint layers (Onda 7)
    if not TRIAL_FINGERPRINT.exists():
        _write_fingerprint()
    return lic


def activate_key(key: str) -> dict:
    """Activate a VIP license key."""
    validation = validate_key(key)
    if not validation["valid"]:
        return {"success": False, "error": validation["reason"]}

    tier = validation["tier"]
    tier_config = TIERS[tier]
    now = datetime.now(UTC)

    lic = {
        "tier": tier,
        "name": tier_config["name"],
        "key": key,
        "email": None,
        "activated_at": now.isoformat(),
        "expires_at": None,  # Permanent
        "max_parallel": tier_config["max_parallel"],
        "features": tier_config["features"],
        "engines_allowed": tier_config["engines_allowed"],
        "status": "active",
    }
    save_license(lic)
    return {"success": True, "tier": tier, "name": tier_config["name"]}


def _server_revalidate(lic: dict) -> dict | None:
    """If the license server is configured AND this license has a server
    token, revalidate against the server (source of truth). Returns the
    server's validation response, or None when offline / unconfigured.

    Side effect: stamps `last_server_check_at` on the local license so
    callers can rate-limit revalidations.
    """
    try:
        import license_client
        if not license_client.is_enabled():
            return None
        token = lic.get("server_token")
        if not token:
            return None
        machine = _machine_id()
        result = license_client.validate_trial(
            machine_id=machine,
            token=token,
            client_first_init_at=lic.get("activated_at"),
        )
        if result is None:
            # Unreachable — degrade gracefully to offline.
            return None
        # Record check timestamp + server-reported status
        lic["last_server_check_at"] = datetime.now(UTC).isoformat()
        lic["last_server_status"] = result.get("status")
        if result.get("rollback_detected"):
            lic["status"] = "tampered"
        elif result.get("status") == "expired":
            lic["status"] = "expired"
        save_license(lic)
        return result
    except Exception:
        return None


def check_license() -> dict:
    """Check if current license is valid. Returns status.

    Order of operations:
        1. Load local license.json
        2. If license is trial AND has server_token AND env DARIO_LICENSE_SERVER
           is set → revalidate against server (truth source). Rate-limited
           to once per hour to avoid hammering the server.
        3. Apply local expiration check (works offline too).

    Anti-snapshot rollback: the server response includes
    `rollback_detected=True` when the client-reported `client_first_init_at`
    diverges from the server's record by more than tolerance. We honour it.
    """
    lic = load_license()

    if not lic:
        return {"valid": False, "reason": "No license found. Run: python license_manager.py --init-trial",
                "tier": "none", "action": "init_trial"}

    # Server revalidation (Onda 8): once per hour, if configured + trial + bound
    if (lic.get("tier") == "trial" and lic.get("server_bound")):
        last_check = lic.get("last_server_check_at")
        do_check = True
        if last_check:
            try:
                last = datetime.fromisoformat(last_check)
                if (datetime.now(UTC) - last).total_seconds() < 3600:
                    do_check = False
            except Exception:
                pass
        if do_check:
            server_result = _server_revalidate(lic)
            if server_result and server_result.get("rollback_detected"):
                return {
                    "valid": False,
                    "tier": "trial",
                    "reason": "snapshot_rollback_detected",
                    "message": (
                        "License server detected a clock or install rollback "
                        "on this machine (VM snapshot or local time tamper). "
                        "Trial revoked. Activate a VIP key to continue."
                    ),
                    "action": "activate_key",
                }
            if server_result and server_result.get("status") == "expired":
                return {
                    "valid": False,
                    "tier": "trial",
                    "reason": "server_says_expired",
                    "expired_at": server_result.get("expires_at"),
                    "message": (
                        "License server records this trial as expired. "
                        "Activate a VIP key: python license_manager.py "
                        "--activate DARIO-XXXX-XXXX-XXXX-PRO"
                    ),
                    "action": "activate_key",
                }

    tier = lic.get("tier", "trial")
    status = lic.get("status", "unknown")

    # Check expiration for trial
    if tier == "trial" and lic.get("expires_at"):
        try:
            expires = datetime.fromisoformat(lic["expires_at"])
            now = datetime.now(UTC)
            if now > expires:
                lic["status"] = "expired"
                save_license(lic)
                remaining = 0
                return {
                    "valid": False,
                    "tier": "trial",
                    "reason": "Trial expired",
                    "expired_at": lic["expires_at"],
                    "action": "activate_key",
                    "message": "Your 7-day trial has expired. Activate a VIP key: python license_manager.py --activate DARIO-XXXX-XXXX-XXXX-PRO",
                }
            remaining = (expires - now).days
            return {
                "valid": True,
                "tier": "trial",
                "days_remaining": remaining,
                "expires_at": lic["expires_at"],
                "max_parallel": lic.get("max_parallel", 1),
                "features": lic.get("features", {}),
            }
        except Exception:
            pass

    # Pro/Enterprise = permanent
    if tier in ("pro", "enterprise"):
        return {
            "valid": True,
            "tier": tier,
            "name": lic.get("name"),
            "key": lic.get("key", "")[:15] + "...",
            "max_parallel": lic.get("max_parallel", 3),
            "features": lic.get("features", {}),
            "permanent": True,
        }

    return {"valid": False, "tier": tier, "reason": "Unknown license state"}


def is_feature_allowed(feature: str) -> bool:
    """Quick check if a specific feature is allowed."""
    lic = check_license()
    if not lic.get("valid"):
        return False
    features = lic.get("features", {})
    return features.get(feature, False)


def get_max_parallel() -> int:
    """Get allowed max parallel from license."""
    lic = check_license()
    if not lic.get("valid"):
        return 0
    return lic.get("max_parallel", 1)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="DARIO License Manager")
    parser.add_argument("--status", "-s", action="store_true", help="Show license status")
    parser.add_argument("--activate", "-a", help="Activate VIP key")
    parser.add_argument("--init-trial", action="store_true", help="Start 7-day trial")
    parser.add_argument("--check", "-c", action="store_true", help="Check if valid (exit code)")
    parser.add_argument("--generate-key", nargs=2, metavar=("TIER", "EMAIL"), help="Generate key (admin)")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.json:
        logging.getLogger().setLevel(logging.ERROR)

    if args.init_trial:
        lic = init_trial()
        if args.json:
            print(json.dumps(lic, indent=2))
        else:
            # v11.1.1+ — handle anti-bypass refusal
            if lic.get("status") == "refused":
                first = (lic.get("first_init_at") or "?")[:10]
                tampered = lic.get("tampered", False)
                print(f"""
╔══════════════════════════════════════════════╗
║  DARIO ORCHESTRATOR — TRIAL REFUSED          ║
║                                              ║
║  Status:    REFUSED (one trial per machine)  ║
║  Used on:   {first}                          ║
║  Tampered:  {'YES — fingerprint modified' if tampered else 'NO':<33s}║
║                                              ║
║  Activate VIP key:                           ║
║  python license_manager.py --activate \\      ║
║    DARIO-XXXX-XXXX-XXXX-PRO                  ║
║                                              ║
║  Or purchase: barda@automationsolutionai.com ║
╚══════════════════════════════════════════════╝
""")
                return 2

            expires = lic["expires_at"][:10]
            print(f"""
╔══════════════════════════════════════════╗
║  DARIO ORCHESTRATOR — 7-DAY TRIAL       ║
║                                          ║
║  Status:   ACTIVE                        ║
║  Expires:  {expires}                    ║
║  Parallel: 1 (max)                       ║
║  Engines:  6 of 26                       ║
║                                          ║
║  To unlock full access:                  ║
║  python license_manager.py --activate    ║
║    DARIO-XXXX-XXXX-XXXX-PRO             ║
╚══════════════════════════════════════════╝
""")
        return 0

    elif args.activate:
        result = activate_key(args.activate)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                print(f"""
╔══════════════════════════════════════════╗
║  DARIO ORCHESTRATOR — LICENSE ACTIVATED  ║
║                                          ║
║  Tier:     {result['name']:30s}  ║
║  Status:   PERMANENT                     ║
║  Parallel: {TIERS[result['tier']]['max_parallel']}                              ║
║  Engines:  ALL 26                        ║
║  Features: ALL UNLOCKED                  ║
║                                          ║
║  Thank you for supporting DARIO!         ║
╚══════════════════════════════════════════╝
""")
            else:
                print(f"  ERROR: {result['error']}")
        return 0 if result.get("success") else 1

    elif args.check:
        result = check_license()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["valid"]:
                tier = result["tier"]
                if tier == "trial":
                    print(f"  TRIAL — {result.get('days_remaining', '?')} days remaining")
                else:
                    print(f"  {result.get('name', tier).upper()} — permanent license")
            else:
                print(f"  INVALID — {result.get('reason', '?')}")
                if result.get("message"):
                    print(f"  {result['message']}")
        return 0 if result["valid"] else 1

    elif args.generate_key:
        tier, email = args.generate_key
        valid_tiers = ("starter", "pro", "enterprise",
                       "lex_solo", "lex_office", "lex_enterprise",
                       "demeter_solo", "demeter_team", "demeter_enterprise",
                       "orion_solo", "orion_team", "orion_enterprise",
                       "obsidian_solo", "obsidian_team", "obsidian_enterprise",
                       "medik_solo", "medik_team", "medik_enterprise",
                       "campus_solo", "campus_team", "campus_enterprise",
                       "aegis_solo", "aegis_team", "aegis_enterprise",
                       "zenith_solo", "zenith_team", "zenith_enterprise",
                       "gaia_solo", "gaia_team", "gaia_enterprise",
                       "nomos_solo", "nomos_team", "nomos_enterprise",
                       "mercurius_solo", "mercurius_team", "mercurius_enterprise",
                       "atlas_fin_solo", "atlas_fin_team", "atlas_fin_enterprise",
                       "helios_solo", "helios_team", "helios_enterprise",
                       "kirion_solo", "kirion_team", "kirion_enterprise",
                       "sphinx_solo", "sphinx_team", "sphinx_enterprise",
                       "euterpe_solo", "euterpe_team", "euterpe_enterprise",
                       "oraculo_solo", "oraculo_team", "oraculo_enterprise")
        if tier not in valid_tiers:
            print(f"Tier must be one of: {', '.join(valid_tiers)}")
            return 1
        key = generate_key(tier, email)
        if args.json:
            print(json.dumps({"key": key, "tier": tier, "email": email}))
        else:
            print(f"  Generated key for {email} ({tier}):")
            print(f"  {key}")
            print("\n  Send to customer. They run:")
            print(f"  python license_manager.py --activate {key}")
        return 0

    elif args.status:
        lic = load_license()
        result = check_license()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if not lic:
                print("  No license. Run: python license_manager.py --init-trial")
            else:
                print(f"  Tier:      {lic.get('tier', '?')}")
                print(f"  Name:      {lic.get('name', '?')}")
                print(f"  Status:    {lic.get('status', '?')}")
                print(f"  Parallel:  {lic.get('max_parallel', '?')}")
                if lic.get("expires_at"):
                    print(f"  Expires:   {lic['expires_at'][:10]}")
                    if result.get("days_remaining") is not None:
                        print(f"  Remaining: {result['days_remaining']} days")
                else:
                    print("  Expires:   NEVER (permanent)")
                if lic.get("key"):
                    print(f"  Key:       {lic['key'][:15]}...")
                # Feature summary
                features = lic.get("features", {})
                locked = [k for k, v in features.items() if not v]
                unlocked = [k for k, v in features.items() if v]
                print(f"  Unlocked:  {len(unlocked)} features")
                if locked:
                    print(f"  Locked:    {', '.join(locked[:5])}")
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

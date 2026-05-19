"""
LEX-BR Compliance Layer
========================
6 modules de compliance para Direito Brasileiro:
  - oab_205_gate: enforce OAB Provimento 205/2021 (revisão humana obrigatória)
  - lgpd_marker: rodapé LGPD automático em outputs
  - zdr_check: enforce ZDR para dados sensíveis
  - cite_checker: valida art./lei citados
  - privilege_marker: marca outputs com sigilo cliente-advogado
  - audit_oab: log imutável compatível com fiscalização OAB
"""

from .oab_205_gate import check as oab_205_check
from .lgpd_marker import add_marker as lgpd_add_marker
from .zdr_check import enforce as zdr_enforce
from .cite_checker import validate as cite_validate
from .privilege_marker import mark as privilege_mark
from .audit_oab import log as audit_log

__all__ = [
    "oab_205_check",
    "lgpd_add_marker",
    "zdr_enforce",
    "cite_validate",
    "privilege_mark",
    "audit_log",
]

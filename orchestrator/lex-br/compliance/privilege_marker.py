#!/usr/bin/env python3
"""
Privilege Marker — Sigilo Cliente-Advogado
============================================
Marca outputs LEX-BR com aviso explícito de sigilo profissional.

Base legal:
  - Art. 36 do Estatuto da OAB (Lei 8.906/94): sigilo é dever
  - Art. 154 Código Penal: violação de segredo profissional é crime
  - Art. 207 CPP: testemunhas que sabem segredo profissional são proibidas

Tipos de output marcados:
  - parecer_juridico
  - estrategia_processual
  - comunicacao_cliente
  - analise_contraparte
  - peticao_em_elaboracao
"""

PRIVILEGE_BANNER = """
═══════════════════════════════════════════════════════════════════════
**SIGILOSO — PRIVILÉGIO CLIENTE-ADVOGADO**

Este documento está protegido por sigilo profissional, nos termos do
Art. 36 do Estatuto da OAB (Lei 8.906/94) e Art. 154 do Código Penal.

Distribuição não autorizada a terceiros constitui infração ética e
penal. Apenas o cliente, advogado responsável e equipa interna do
escritório podem acessar este conteúdo.
═══════════════════════════════════════════════════════════════════════

"""

OUTPUT_TYPES_PRIVILEGED = {
    "parecer_juridico",
    "estrategia_processual",
    "comunicacao_cliente",
    "analise_contraparte",
    "peticao_em_elaboracao",
    "memorial_estrategico",
    "due_diligence_report",
    "compliance_audit_internal",
}


def mark(output_text: str, output_type: str = "draft_interno",
         force: bool = False) -> str:
    """Adiciona privilege banner ao output se aplicável.

    Args:
        output_text: texto produzido
        output_type: tipo do output
        force: força marcação independente do tipo

    Returns:
        text com banner privilege no topo (se aplicável)
    """
    if not output_text or not output_text.strip():
        return output_text

    if not force and output_type not in OUTPUT_TYPES_PRIVILEGED:
        return output_text

    # Evitar duplicação se já está marcado
    if "SIGILOSO — PRIVILÉGIO CLIENTE-ADVOGADO" in output_text:
        return output_text

    return PRIVILEGE_BANNER + output_text


def is_privileged_type(output_type: str) -> bool:
    return output_type in OUTPUT_TYPES_PRIVILEGED


if __name__ == "__main__":
    import sys
    sample = "Análise estratégica do caso XYZ: cliente tem 70% de chance de ganhar..."
    print(mark(sample, output_type="estrategia_processual"))

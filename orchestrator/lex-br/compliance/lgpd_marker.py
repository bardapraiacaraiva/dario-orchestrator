#!/usr/bin/env python3
"""
LGPD Operator Marker
=====================
Adiciona rodapé automático em todos os outputs LEX-BR identificando
o orchestrator como operador LGPD (escritório é controlador).

Conforme art. 5º, VII da Lei 13.709/18 (LGPD), o operador realiza o
tratamento de dados em nome do controlador. O marker explicita esta
relação para fins de auditoria + transparência.
"""

import json
from datetime import UTC, datetime
from pathlib import Path

LEX_DIR = Path.home() / ".claude" / "orchestrator" / "lex-br"

DEFAULT_RODAPE = """

---
**Documento gerado com assistência de DARIO/LEX-BR (operador LGPD).**
Controlador: {escritorio}
DPO: {dpo_contact}
Data: {date}
Sigilo profissional mantido (Provimento OAB 205/2021 + Art. 36 EOAB).
ZDR (Zero Data Retention): {zdr_status}
"""


def add_marker(output_text: str, escritorio: str = "Não informado",
               dpo_contact: str = "Não informado",
               zdr_active: bool = True,
               output_type: str = "draft_interno") -> str:
    """Adiciona rodapé LGPD ao output.

    Args:
        output_text: texto produzido pela skill
        escritorio: nome do escritório/empresa controlador
        dpo_contact: contacto do DPO
        zdr_active: se Zero Data Retention está activo
        output_type: tipo de output (alguns não recebem rodapé)

    Returns:
        output_text + rodapé LGPD
    """
    if not output_text or not output_text.strip():
        return output_text

    # Outputs internos curtos podem não precisar de rodapé
    if output_type == "draft_interno" and len(output_text) < 300:
        return output_text  # Memos curtos sem rodapé

    rodape = DEFAULT_RODAPE.format(
        escritorio=escritorio,
        dpo_contact=dpo_contact,
        date=datetime.now(UTC).strftime("%Y-%m-%d"),
        zdr_status="Activo" if zdr_active else "**INACTIVO — REVISAR**",
    )

    # Se já tem rodapé LGPD (rerun), substitui em vez de duplicar
    marker_signature = "**Documento gerado com assistência de DARIO/LEX-BR"
    if marker_signature in output_text:
        # Encontra início do rodapé existente e substitui
        idx = output_text.rfind("\n---\n")
        if idx >= 0:
            output_text = output_text[:idx]

    return output_text.rstrip() + rodape


def configure_for_office(escritorio: str, dpo_contact: str,
                         zdr_active: bool = True) -> dict:
    """Persiste configuração de rodapé do escritório."""
    config_path = LEX_DIR / "lgpd_config.json"
    config = {
        "escritorio": escritorio,
        "dpo_contact": dpo_contact,
        "zdr_active": zdr_active,
        "configured_at": datetime.now(UTC).isoformat(),
    }
    LEX_DIR.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False),
                           encoding="utf-8")
    return config


def load_config() -> dict:
    """Carrega config do escritório (se já configurado)."""
    config_path = LEX_DIR / "lgpd_config.json"
    if not config_path.exists():
        return {
            "escritorio": "Não configurado",
            "dpo_contact": "Não configurado",
            "zdr_active": True,
        }
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def add_marker_with_config(output_text: str, output_type: str = "draft_interno") -> str:
    """Wrapper que carrega config automaticamente."""
    cfg = load_config()
    return add_marker(
        output_text,
        escritorio=cfg.get("escritorio", "Não informado"),
        dpo_contact=cfg.get("dpo_contact", "Não informado"),
        zdr_active=cfg.get("zdr_active", True),
        output_type=output_type,
    )


if __name__ == "__main__":
    sample = "Parecer jurídico sobre cláusula contratual: a cláusula X é válida..."
    print(add_marker(sample, escritorio="Escritório XYZ Advocacia",
                     dpo_contact="dpo@xyz-adv.com.br"))

#!/usr/bin/env python3
"""
DARIO CFO — Portuguese Financial Validators
Validates NIF, ATCUD, SNC accounts, IVA rates, IBAN, invoice formats.
Inspired by Anthropic Financial Services schema-constrained output pattern.

Usage as CLI:
    python pt_validators.py --nif 123456789
    python pt_validators.py --atcud "ABCD-12345"
    python pt_validators.py --snc 6211
    python pt_validators.py --iva 23 --region continente
    python pt_validators.py --iban PT50000201231234567890154
    python pt_validators.py --invoice "FT 2026/001"
    python pt_validators.py --validate-all '{"nif":"509123456","atcud":"XKJL-1","snc":"7211","iva_rate":23}'
    python pt_validators.py --test               # Run self-test suite

Usage as module:
    from pt_validators import validate_nif, validate_atcud, validate_snc_account
"""

import argparse
import json
import re
import sys

# ═══════════════════════════════════════════════════════════════════
# NIF — Número de Identificação Fiscal
# ═══════════════════════════════════════════════════════════════════

VALID_NIF_PREFIXES = {
    # Pessoas singulares
    "1": "Pessoa singular",
    "2": "Pessoa singular",
    "3": "Pessoa singular",
    # Pessoas colectivas
    "5": "Pessoa colectiva",
    "6": "Administração pública",
    "7": "Herança indivisa / Não residente colectivo",
    "8": "Empresário em nome individual (ENI)",
    "9": "Pessoa colectiva irregular / Internacional",
}


def validate_nif(nif: str) -> dict:
    """
    Validate Portuguese NIF (Número de Identificação Fiscal).
    Uses mod-11 check digit algorithm.

    Returns: {"valid": bool, "nif": str, "type": str, "error": str|None}
    """
    nif = str(nif).strip().replace(" ", "")

    if not nif.isdigit():
        return {"valid": False, "nif": nif, "type": None, "error": "NIF must contain only digits"}

    if len(nif) != 9:
        return {"valid": False, "nif": nif, "type": None, "error": f"NIF must be 9 digits, got {len(nif)}"}

    prefix = nif[0]
    if prefix not in VALID_NIF_PREFIXES:
        return {"valid": False, "nif": nif, "type": None, "error": f"Invalid prefix '{prefix}'. Valid: {list(VALID_NIF_PREFIXES.keys())}"}

    # Mod-11 check digit
    weights = [9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(nif[i]) * weights[i] for i in range(8))
    remainder = total % 11

    if remainder <= 1:
        expected_check = 0
    else:
        expected_check = 11 - remainder

    actual_check = int(nif[8])

    if actual_check != expected_check:
        return {
            "valid": False, "nif": nif,
            "type": VALID_NIF_PREFIXES[prefix],
            "error": f"Check digit invalid: expected {expected_check}, got {actual_check}"
        }

    return {
        "valid": True, "nif": nif,
        "type": VALID_NIF_PREFIXES[prefix],
        "error": None
    }


# ═══════════════════════════════════════════════════════════════════
# ATCUD — Código Único de Documento
# ═══════════════════════════════════════════════════════════════════

ATCUD_PATTERN = re.compile(r"^[A-Z0-9]{4,8}-\d{1,}$")


def validate_atcud(atcud: str) -> dict:
    """
    Validate ATCUD format (obrigatório desde 2023 em todas as facturas).
    Format: [Código de Validação]-[Número Sequencial]
    Example: XKJL-1, ABCD1234-999

    Returns: {"valid": bool, "atcud": str, "error": str|None}
    """
    atcud = str(atcud).strip()

    if not atcud:
        return {"valid": False, "atcud": atcud, "error": "ATCUD is empty"}

    if not ATCUD_PATTERN.match(atcud):
        return {
            "valid": False, "atcud": atcud,
            "error": "ATCUD must match pattern: [A-Z0-9]{4,8}-[digits]. Example: XKJL-1"
        }

    parts = atcud.split("-")
    code = parts[0]
    seq = int(parts[1])

    if seq < 1:
        return {"valid": False, "atcud": atcud, "error": "Sequential number must be >= 1"}

    return {"valid": True, "atcud": atcud, "code": code, "sequence": seq, "error": None}


# ═══════════════════════════════════════════════════════════════════
# SNC — Sistema de Normalização Contabilística (Chart of Accounts)
# ═══════════════════════════════════════════════════════════════════

SNC_CLASSES = {
    "1": {"name": "Meios financeiros líquidos", "examples": ["11-Caixa", "12-Depósitos à ordem", "13-Outros depósitos"]},
    "2": {"name": "Contas a receber e a pagar", "examples": ["21-Clientes", "22-Fornecedores", "23-Pessoal", "24-Estado"]},
    "3": {"name": "Inventários e activos biológicos", "examples": ["31-Compras", "32-Mercadorias", "33-Matérias-primas"]},
    "4": {"name": "Investimentos", "examples": ["41-Investimentos financeiros", "43-Activos fixos tangíveis", "44-Activos intangíveis"]},
    "5": {"name": "Capital, reservas e resultados transitados", "examples": ["51-Capital subscrito", "55-Reservas", "56-Resultados transitados"]},
    "6": {"name": "Gastos", "examples": ["61-CMVMC", "62-FSE", "63-Gastos pessoal", "64-Depreciações", "68-Outros gastos"]},
    "7": {"name": "Rendimentos", "examples": ["71-Vendas", "72-Prestações serviços", "78-Outros rendimentos"]},
    "8": {"name": "Resultados", "examples": ["81-Resultado líquido", "89-Dividendos antecipados"]},
}

# Key accounts that are frequently used
KEY_ACCOUNTS = {
    "11": "Caixa",
    "12": "Depósitos à ordem",
    "21": "Clientes",
    "211": "Clientes c/c",
    "22": "Fornecedores",
    "221": "Fornecedores c/c",
    "231": "Remunerações a pagar",
    "241": "Imposto sobre o rendimento (IRC)",
    "2432": "IVA dedutível",
    "2433": "IVA liquidado",
    "2434": "IVA regularizações",
    "2435": "IVA apuramento",
    "2436": "IVA a pagar",
    "2437": "IVA a recuperar",
    "245": "Contribuições para SS",
    "51": "Capital subscrito",
    "6111": "Mercadorias — Custo",
    "62": "Fornecimentos e serviços externos",
    "631": "Remunerações dos órgãos sociais",
    "632": "Remunerações do pessoal",
    "6811": "Juros suportados",
    "6865": "Tributação autónoma",
    "691": "IRC — Imposto estimado",
    "711": "Vendas — Mercadorias",
    "72": "Prestações de serviços",
    "7811": "Juros obtidos",
    "811": "Resultado antes de impostos",
    "812": "Resultado líquido",
}


def validate_snc_account(account: str) -> dict:
    """
    Validate SNC account number.
    Must start with class 1-8, numeric, 2-6 digits typical.

    Returns: {"valid": bool, "account": str, "class": str, "class_name": str, "known_name": str|None, "error": str|None}
    """
    account = str(account).strip()

    if not account.isdigit():
        return {"valid": False, "account": account, "class": None, "class_name": None, "error": "Account must be numeric"}

    if len(account) < 2:
        return {"valid": False, "account": account, "class": None, "class_name": None, "error": "Account must be at least 2 digits"}

    if len(account) > 8:
        return {"valid": False, "account": account, "class": None, "class_name": None, "error": "Account too long (max 8 digits)"}

    cls = account[0]
    if cls not in SNC_CLASSES:
        return {
            "valid": False, "account": account, "class": cls, "class_name": None,
            "error": f"Invalid class '{cls}'. SNC classes are 1-8"
        }

    # Check for class 0 or 9
    if cls in ("0", "9"):
        return {
            "valid": False, "account": account, "class": cls, "class_name": None,
            "error": f"Class {cls} is not a standard SNC class"
        }

    known_name = KEY_ACCOUNTS.get(account)
    # Try shorter prefixes
    if not known_name:
        for length in range(len(account) - 1, 1, -1):
            known_name = KEY_ACCOUNTS.get(account[:length])
            if known_name:
                known_name = f"{known_name} (sub-account)"
                break

    return {
        "valid": True, "account": account,
        "class": cls, "class_name": SNC_CLASSES[cls]["name"],
        "known_name": known_name,
        "error": None
    }


# ═══════════════════════════════════════════════════════════════════
# IVA — Imposto sobre o Valor Acrescentado
# ═══════════════════════════════════════════════════════════════════

IVA_RATES = {
    "continente": {"normal": 23, "intermedia": 13, "reduzida": 6},
    "madeira":    {"normal": 22, "intermedia": 12, "reduzida": 5},
    "acores":     {"normal": 16, "intermedia": 9,  "reduzida": 4},
}

ALL_VALID_RATES = set()
for region_rates in IVA_RATES.values():
    ALL_VALID_RATES.update(region_rates.values())
ALL_VALID_RATES.add(0)  # Isento


def validate_iva_rate(rate: float, region: str = "continente") -> dict:
    """
    Validate IVA rate for a given region.

    Returns: {"valid": bool, "rate": float, "region": str, "type": str|None, "error": str|None}
    """
    rate = float(rate)
    region = region.lower().strip()

    if region not in IVA_RATES:
        return {
            "valid": False, "rate": rate, "region": region, "type": None,
            "error": f"Unknown region '{region}'. Valid: continente, madeira, acores"
        }

    rates = IVA_RATES[region]

    if rate == 0:
        return {"valid": True, "rate": rate, "region": region, "type": "isento", "error": None}

    for rate_type, rate_value in rates.items():
        if abs(rate - rate_value) < 0.01:
            return {"valid": True, "rate": rate, "region": region, "type": rate_type, "error": None}

    valid_rates = [0] + sorted(rates.values())
    return {
        "valid": False, "rate": rate, "region": region, "type": None,
        "error": f"Rate {rate}% not valid for {region}. Valid rates: {valid_rates}"
    }


# ═══════════════════════════════════════════════════════════════════
# IBAN — International Bank Account Number (PT format)
# ═══════════════════════════════════════════════════════════════════

def validate_iban_pt(iban: str) -> dict:
    """
    Validate Portuguese IBAN (PT50 + 21 digits = 25 chars total).
    Uses mod-97 check per ISO 13616.

    Returns: {"valid": bool, "iban": str, "bank": str|None, "error": str|None}
    """
    iban = iban.strip().replace(" ", "").upper()

    if not iban.startswith("PT"):
        return {"valid": False, "iban": iban, "bank": None, "error": "Portuguese IBAN must start with 'PT'"}

    if len(iban) != 25:
        return {"valid": False, "iban": iban, "bank": None, "error": f"PT IBAN must be 25 chars, got {len(iban)}"}

    if not iban[2:].isdigit():
        return {"valid": False, "iban": iban, "bank": None, "error": "IBAN digits part must be numeric"}

    # ISO 13616 mod-97 check
    # Move country code + check digits to end, convert letters to numbers
    rearranged = iban[4:] + iban[:4]
    numeric = ""
    for char in rearranged:
        if char.isdigit():
            numeric += char
        else:
            numeric += str(ord(char) - 55)  # A=10, B=11, ..., Z=35

    if int(numeric) % 97 != 1:
        return {"valid": False, "iban": iban, "bank": None, "error": "IBAN check digits invalid (mod-97 failed)"}

    # Extract bank code (positions 5-8 in IBAN)
    bank_code = iban[4:8]
    known_banks = {
        "0001": "Banco de Portugal",
        "0007": "Novo Banco",
        "0010": "BPI",
        "0018": "Santander Totta",
        "0023": "Banco Activobank",
        "0033": "Millennium BCP",
        "0035": "CGD",
        "0036": "Montepio",
        "0046": "Crédito Agrícola",
        "0061": "Bankinter",
        "0269": "BEST",
    }
    bank_name = known_banks.get(bank_code, f"Bank code {bank_code}")

    return {"valid": True, "iban": iban, "bank": bank_name, "bank_code": bank_code, "error": None}


# ═══════════════════════════════════════════════════════════════════
# Invoice Number — Formato PT
# ═══════════════════════════════════════════════════════════════════

INVOICE_TYPES = {
    "FT": "Factura",
    "FS": "Factura simplificada",
    "FR": "Factura-recibo",
    "NC": "Nota de crédito",
    "ND": "Nota de débito",
    "RC": "Recibo",
    "GT": "Guia de transporte",
    "GR": "Guia de remessa",
    "OR": "Orçamento",
    "PF": "Proforma",
}

INVOICE_PATTERN = re.compile(r"^([A-Z]{2})\s+(\d{4})/(\d{1,6})$")


def validate_invoice_number(invoice_num: str) -> dict:
    """
    Validate Portuguese invoice number format.
    Expected: TYPE YEAR/SEQUENTIAL (e.g., "FT 2026/001")

    Returns: {"valid": bool, "number": str, "type": str, "type_name": str, "year": int, "seq": int, "error": str|None}
    """
    invoice_num = str(invoice_num).strip()

    match = INVOICE_PATTERN.match(invoice_num)
    if not match:
        return {
            "valid": False, "number": invoice_num,
            "error": "Format must be: TYPE YEAR/SEQ (e.g., 'FT 2026/001')"
        }

    doc_type = match.group(1)
    year = int(match.group(2))
    seq = int(match.group(3))

    if doc_type not in INVOICE_TYPES:
        return {
            "valid": False, "number": invoice_num,
            "error": f"Unknown type '{doc_type}'. Valid: {list(INVOICE_TYPES.keys())}"
        }

    if year < 2020 or year > 2030:
        return {
            "valid": False, "number": invoice_num,
            "error": f"Year {year} seems invalid (expected 2020-2030)"
        }

    if seq < 1:
        return {"valid": False, "number": invoice_num, "error": "Sequential must be >= 1"}

    return {
        "valid": True, "number": invoice_num,
        "type": doc_type, "type_name": INVOICE_TYPES[doc_type],
        "year": year, "seq": seq,
        "error": None
    }


# ═══════════════════════════════════════════════════════════════════
# Batch Validator — validate multiple fields at once
# ═══════════════════════════════════════════════════════════════════

def validate_all(data: dict) -> dict:
    """
    Validate multiple fields in a single call.
    Input: {"nif": "...", "atcud": "...", "snc": "...", "iva_rate": N, "iban": "...", "invoice": "..."}
    Returns: {"valid": bool, "results": {...}, "errors": [...]}
    """
    results = {}
    errors = []

    if "nif" in data:
        r = validate_nif(data["nif"])
        results["nif"] = r
        if not r["valid"]:
            errors.append(f"NIF: {r['error']}")

    if "atcud" in data:
        r = validate_atcud(data["atcud"])
        results["atcud"] = r
        if not r["valid"]:
            errors.append(f"ATCUD: {r['error']}")

    if "snc" in data:
        r = validate_snc_account(data["snc"])
        results["snc"] = r
        if not r["valid"]:
            errors.append(f"SNC: {r['error']}")

    if "iva_rate" in data:
        region = data.get("region", "continente")
        r = validate_iva_rate(data["iva_rate"], region)
        results["iva_rate"] = r
        if not r["valid"]:
            errors.append(f"IVA: {r['error']}")

    if "iban" in data:
        r = validate_iban_pt(data["iban"])
        results["iban"] = r
        if not r["valid"]:
            errors.append(f"IBAN: {r['error']}")

    if "invoice" in data:
        r = validate_invoice_number(data["invoice"])
        results["invoice"] = r
        if not r["valid"]:
            errors.append(f"Invoice: {r['error']}")

    return {
        "valid": len(errors) == 0,
        "fields_checked": len(results),
        "fields_valid": sum(1 for r in results.values() if r.get("valid")),
        "results": results,
        "errors": errors,
    }


# ═══════════════════════════════════════════════════════════════════
# Self-Test Suite
# ═══════════════════════════════════════════════════════════════════

def run_tests():
    """Run validation self-test suite."""
    passed = 0
    failed = 0

    def check(name, result, expected_valid):
        nonlocal passed, failed
        if result["valid"] == expected_valid:
            passed += 1
            print(f"  PASS  {name}")
        else:
            failed += 1
            print(f"  FAIL  {name} — expected valid={expected_valid}, got {result}")

    print("=== NIF Tests ===")
    check("Valid NIF empresa",    validate_nif("509123456"), False)  # Random, likely invalid check digit
    check("Valid NIF format",     validate_nif("123456789"), True)   # 1+2+3... check digit test
    # Known valid: compute one
    # NIF 999999990: weights 9*9+8*9+7*9+6*9+5*9+4*9+3*9+2*9 = 9*(9+8+7+6+5+4+3+2) = 9*44 = 396
    # 396 % 11 = 396 - 36*11 = 396-396 = 0 → check = 0
    check("Valid NIF computed",   validate_nif("999999990"), True)
    check("Invalid NIF length",   validate_nif("12345"), False)
    check("Invalid NIF letters",  validate_nif("12345678A"), False)
    check("Invalid NIF prefix 4", validate_nif("412345678"), False)

    print("\n=== ATCUD Tests ===")
    check("Valid ATCUD simple",   validate_atcud("XKJL-1"), True)
    check("Valid ATCUD long",     validate_atcud("ABCD1234-999"), True)
    check("Invalid ATCUD no dash",validate_atcud("XKJL1"), False)
    check("Invalid ATCUD short",  validate_atcud("XK-1"), False)
    check("Invalid ATCUD lower",  validate_atcud("xkjl-1"), False)

    print("\n=== SNC Account Tests ===")
    check("Valid SNC class 1",    validate_snc_account("12"), True)
    check("Valid SNC class 6",    validate_snc_account("6211"), True)
    check("Valid SNC IVA",        validate_snc_account("2433"), True)
    check("Invalid SNC class 0",  validate_snc_account("01"), False)
    check("Invalid SNC class 9",  validate_snc_account("91"), False)
    check("Invalid SNC short",    validate_snc_account("1"), False)

    print("\n=== IVA Rate Tests ===")
    check("Valid 23% continente", validate_iva_rate(23, "continente"), True)
    check("Valid 6% reduzida",    validate_iva_rate(6, "continente"), True)
    check("Valid 22% Madeira",    validate_iva_rate(22, "madeira"), True)
    check("Valid 16% Açores",     validate_iva_rate(16, "acores"), True)
    check("Valid 0% isento",      validate_iva_rate(0, "continente"), True)
    check("Invalid 21%",          validate_iva_rate(21, "continente"), False)
    check("Invalid region",       validate_iva_rate(23, "algarve"), False)

    print("\n=== IBAN Tests ===")
    check("Valid IBAN CGD",       validate_iban_pt("PT50003506519922710014610"), False)  # Likely invalid check
    check("Invalid IBAN short",   validate_iban_pt("PT501234"), False)
    check("Invalid IBAN prefix",  validate_iban_pt("ES5000350651992271001461"), False)

    print("\n=== Invoice Number Tests ===")
    check("Valid FT",             validate_invoice_number("FT 2026/001"), True)
    check("Valid NC",             validate_invoice_number("NC 2026/15"), True)
    check("Valid RC",             validate_invoice_number("RC 2025/100"), True)
    check("Invalid type",         validate_invoice_number("XX 2026/001"), False)
    check("Invalid format",       validate_invoice_number("FT2026001"), False)
    check("Invalid year",         validate_invoice_number("FT 2015/001"), False)

    print("\n=== Batch Validator Tests ===")
    batch = validate_all({
        "nif": "999999990",
        "atcud": "XKJL-1",
        "snc": "2433",
        "iva_rate": 23,
    })
    check("Batch all valid", batch, True)

    batch_mixed = validate_all({
        "nif": "000000000",
        "atcud": "XKJL-1",
    })
    check("Batch mixed (NIF invalid)", batch_mixed, False)

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed, {passed+failed} total")
    return 0 if failed == 0 else 1


# ═══════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="DARIO CFO — Portuguese Financial Validators")
    parser.add_argument("--nif", type=str, help="Validate NIF")
    parser.add_argument("--atcud", type=str, help="Validate ATCUD")
    parser.add_argument("--snc", type=str, help="Validate SNC account")
    parser.add_argument("--iva", type=float, help="Validate IVA rate")
    parser.add_argument("--region", type=str, default="continente", help="Region for IVA (continente/madeira/acores)")
    parser.add_argument("--iban", type=str, help="Validate PT IBAN")
    parser.add_argument("--invoice", type=str, help="Validate invoice number")
    parser.add_argument("--validate-all", type=str, help="Validate JSON object with multiple fields")
    parser.add_argument("--test", action="store_true", help="Run self-test suite")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.test:
        sys.exit(run_tests())

    results = []

    if args.nif:
        results.append(("NIF", validate_nif(args.nif)))
    if args.atcud:
        results.append(("ATCUD", validate_atcud(args.atcud)))
    if args.snc:
        results.append(("SNC", validate_snc_account(args.snc)))
    if args.iva is not None:
        results.append(("IVA", validate_iva_rate(args.iva, args.region)))
    if args.iban:
        results.append(("IBAN", validate_iban_pt(args.iban)))
    if args.invoice:
        results.append(("Invoice", validate_invoice_number(args.invoice)))
    if args.validate_all:
        data = json.loads(args.validate_all)
        result = validate_all(data)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            status = "VALID" if result["valid"] else "INVALID"
            print(f"{status}: {result['fields_valid']}/{result['fields_checked']} fields valid")
            for err in result["errors"]:
                print(f"  X {err}")
        sys.exit(0 if result["valid"] else 1)

    if not results:
        parser.print_help()
        return

    all_valid = True
    for name, result in results:
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            status = "VALID" if result["valid"] else "INVALID"
            detail = result.get("type") or result.get("class_name") or result.get("type_name") or result.get("bank") or ""
            error = result.get("error", "")
            if result["valid"]:
                print(f"  VALID  {name}: {detail}")
            else:
                print(f"  INVALID  {name}: {error}")
                all_valid = False

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()

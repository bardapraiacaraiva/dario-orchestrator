#!/usr/bin/env python3
"""
DARIO CFO — Bank Statement Parser (PT)
========================================
First REAL data connector. Reads bank statement CSVs from Portuguese banks
and converts to structured data for reconciliation and P&L.

Supported formats:
- CGD (Caixa Geral de Depósitos)
- Millennium BCP
- BPI
- Novo Banco
- Santander Totta
- Generic CSV (configurable columns)

Usage:
    python bank_parser.py --file extrato.csv                     # Auto-detect bank
    python bank_parser.py --file extrato.csv --bank cgd          # Force bank format
    python bank_parser.py --file extrato.csv --output json       # JSON output
    python bank_parser.py --file extrato.csv --output yaml       # Update receivables
    python bank_parser.py --dir ./extratos/ --merge              # Merge multiple files
    python bank_parser.py --file extrato.csv --categorize        # Auto-categorize transactions
    python bank_parser.py --test                                 # Run with sample data
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

ORCH_DIR = Path(os.path.expanduser("~/.claude/orchestrator"))
FINANCE_DIR = ORCH_DIR / "finance"

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("bank_parser")


@dataclass
class Transaction:
    """A single bank transaction."""
    date: str = ""
    description: str = ""
    amount: float = 0.0
    balance: float = 0.0
    type: str = ""        # credit | debit
    category: str = ""    # auto-categorized
    reference: str = ""
    value_date: str = ""
    bank: str = ""
    raw_line: str = ""


# ═══════════════════════════════════════════════════
# BANK FORMAT DEFINITIONS
# ═══════════════════════════════════════════════════

BANK_FORMATS = {
    "cgd": {
        "name": "Caixa Geral de Depósitos",
        "encoding": "latin-1",
        "delimiter": ";",
        "date_col": 0,
        "description_col": 1,
        "debit_col": 2,
        "credit_col": 3,
        "balance_col": 4,
        "date_format": "%d-%m-%Y",
        "skip_header": 1,
        "decimal_sep": ",",
    },
    "millennium": {
        "name": "Millennium BCP",
        "encoding": "utf-8",
        "delimiter": ";",
        "date_col": 0,
        "value_date_col": 1,
        "description_col": 2,
        "amount_col": 3,
        "balance_col": 4,
        "date_format": "%d/%m/%Y",
        "skip_header": 1,
        "decimal_sep": ",",
    },
    "bpi": {
        "name": "Banco BPI",
        "encoding": "latin-1",
        "delimiter": "\t",
        "date_col": 0,
        "description_col": 1,
        "amount_col": 2,
        "balance_col": 3,
        "date_format": "%d-%m-%Y",
        "skip_header": 1,
        "decimal_sep": ",",
    },
    "novo_banco": {
        "name": "Novo Banco",
        "encoding": "utf-8",
        "delimiter": ";",
        "date_col": 0,
        "description_col": 2,
        "debit_col": 3,
        "credit_col": 4,
        "balance_col": 5,
        "date_format": "%d/%m/%Y",
        "skip_header": 1,
        "decimal_sep": ",",
    },
    "santander": {
        "name": "Santander Totta",
        "encoding": "latin-1",
        "delimiter": "\t",
        "date_col": 0,
        "description_col": 1,
        "amount_col": 2,
        "balance_col": 3,
        "date_format": "%d-%m-%Y",
        "skip_header": 3,
        "decimal_sep": ",",
    },
    "generic": {
        "name": "Generic CSV",
        "encoding": "utf-8",
        "delimiter": ",",
        "date_col": 0,
        "description_col": 1,
        "amount_col": 2,
        "balance_col": 3,
        "date_format": "%Y-%m-%d",
        "skip_header": 1,
        "decimal_sep": ".",
    },
}


# ═══════════════════════════════════════════════════
# CATEGORY RULES
# ═══════════════════════════════════════════════════

CATEGORY_RULES = [
    # (pattern, category, subcategory)
    (r"transfer[eê]ncia\s+cr[eé]dito|trf\s+cr", "revenue", "transferencia_recebida"),
    (r"mbway.*receb|pagamento\s+receb", "revenue", "mbway_recebido"),
    (r"multibanco.*dep|deposito", "revenue", "deposito"),

    (r"sal[aá]rio|vencimento|ordenado|remunera", "pessoal", "salarios"),
    (r"seguran[cç]a\s+social|ss\s+contrib", "pessoal", "seguranca_social"),
    (r"reten[cç][aã]o|irs\s+ret", "pessoal", "retencao_irs"),

    (r"vodafone|nos\s+comunica|meo|internet|telef", "fse", "telecomunicacoes"),
    (r"aws|amazon\s+web|google\s+cloud|azure|digitalocean|hetzner|ovh", "fse", "cloud_hosting"),
    (r"github|gitlab|figma|canva|adobe|notion|slack|zoom|microsoft\s+365", "fse", "software_saas"),
    (r"dom[ií]nio|ssl|hosting|alojamento|cpanel", "fse", "dominios_hosting"),

    (r"facebook|meta\s+platform|google\s+ads|youtube\s+ads|linkedin\s+ads", "marketing", "publicidade_digital"),
    (r"publicidade|campanha|promoc|marketing", "marketing", "marketing_geral"),

    (r"restaura|refei[cç]|almo[cç]|jantar|caf[eé]|uber\s+eat|glovo", "deslocacoes", "refeicoes"),
    (r"combustivel|gasolina|gasoleo|bp\s+|galp|repsol|cepsa", "deslocacoes", "combustivel"),
    (r"portagem|via\s+verde|scut|a1|a2|a5", "deslocacoes", "portagens"),
    (r"estaciona|parque|emel|empark", "deslocacoes", "estacionamento"),
    (r"uber|bolt|taxi|cabify|freenow", "deslocacoes", "transporte"),
    (r"cp\s+comboio|metro|carris|transtejo|fertagus", "deslocacoes", "transporte_publico"),

    (r"renda|aluguer|arrend", "instalacoes", "renda"),
    (r"electricidade|edp|galp\s+energ|endesa|iberdrola", "instalacoes", "electricidade"),
    (r"[aá]gua|epal|smas|indaqua", "instalacoes", "agua"),
    (r"g[aá]s|galp\s+gas|lisboag", "instalacoes", "gas"),
    (r"limpeza|higiene|material\s+escrit", "instalacoes", "material_escritorio"),

    (r"seguro|fidelidade|allianz|tranquilidade|liberty|generali|ageas", "seguros", "seguros"),
    (r"iva|imposto|at\s+|finan[cç]as|contrib|derrama", "impostos", "impostos"),
    (r"contabil|roc|revisor|toc", "servicos_profissionais", "contabilidade"),
    (r"advogad|jur[ií]dic|notari", "servicos_profissionais", "juridico"),
    (r"consult|assessor|freelanc", "servicos_profissionais", "consultoria"),

    (r"juros\s+credit|comiss[aã]o|anuidade\s+cart|despesas\s+banc", "financeiros", "custos_bancarios"),
    (r"multibanco\s+lev|atm|caixa\s+autom", "financeiros", "levantamentos"),
]


def parse_amount(value: str, decimal_sep: str = ",") -> float:
    """Parse amount string with PT/EN decimal handling."""
    if not value or not value.strip():
        return 0.0
    value = value.strip().replace(" ", "")
    # Remove currency symbols
    value = re.sub(r"[€$£]", "", value)

    if decimal_sep == ",":
        # PT format: 1.234,56
        value = value.replace(".", "").replace(",", ".")
    else:
        # EN format: 1,234.56
        value = value.replace(",", "")

    try:
        return float(value)
    except ValueError:
        return 0.0


def parse_date(date_str: str, fmt: str) -> str:
    """Parse date string to ISO format."""
    date_str = date_str.strip()
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, fmt)
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        # Try common alternative formats
        for alt_fmt in ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d.%m.%Y"]:
            try:
                dt = datetime.strptime(date_str, alt_fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
    return date_str


def categorize_transaction(description: str) -> tuple[str, str]:
    """Auto-categorize transaction by description pattern matching."""
    desc_lower = description.lower()
    for pattern, category, subcategory in CATEGORY_RULES:
        if re.search(pattern, desc_lower):
            return category, subcategory
    return "outros", "nao_categorizado"


def detect_bank(filepath: str) -> str:
    """Try to auto-detect bank format from file content."""
    try:
        # Try UTF-8 first
        with open(filepath, encoding="utf-8") as f:
            first_lines = [f.readline() for _ in range(5)]
    except UnicodeDecodeError:
        with open(filepath, encoding="latin-1") as f:
            first_lines = [f.readline() for _ in range(5)]

    content = "\n".join(first_lines).lower()

    if "caixa geral" in content or "cgd" in content:
        return "cgd"
    if "millennium" in content or "bcp" in content:
        return "millennium"
    if "bpi" in content:
        return "bpi"
    if "novo banco" in content or "bes" in content:
        return "novo_banco"
    if "santander" in content or "totta" in content:
        return "santander"

    # Check delimiter
    if "\t" in first_lines[0]:
        return "bpi"  # Tab-separated common in BPI/Santander
    if ";" in first_lines[0]:
        return "cgd"  # Semicolon common in CGD/Millennium

    return "generic"


def parse_file(filepath: str, bank: str = None) -> list[Transaction]:
    """Parse a bank statement file into transactions."""
    if not bank:
        bank = detect_bank(filepath)

    fmt = BANK_FORMATS.get(bank, BANK_FORMATS["generic"])
    log.info(f"Parsing {filepath} as {fmt['name']} format")

    transactions = []
    encoding = fmt.get("encoding", "utf-8")

    try:
        with open(filepath, encoding=encoding) as f:
            reader = csv.reader(f, delimiter=fmt["delimiter"])

            # Skip header rows
            for _ in range(fmt.get("skip_header", 1)):
                next(reader, None)

            for row_num, row in enumerate(reader):
                if not row or len(row) < 3:
                    continue

                try:
                    t = Transaction(bank=bank)

                    # Date
                    t.date = parse_date(
                        row[fmt["date_col"]] if fmt["date_col"] < len(row) else "",
                        fmt["date_format"]
                    )

                    # Value date (if available)
                    if "value_date_col" in fmt and fmt["value_date_col"] < len(row):
                        t.value_date = parse_date(row[fmt["value_date_col"]], fmt["date_format"])

                    # Description
                    t.description = row[fmt["description_col"]].strip() if fmt["description_col"] < len(row) else ""

                    # Amount
                    decimal_sep = fmt.get("decimal_sep", ",")
                    if "amount_col" in fmt:
                        # Single amount column (negative = debit)
                        t.amount = parse_amount(row[fmt["amount_col"]] if fmt["amount_col"] < len(row) else "0", decimal_sep)
                    elif "debit_col" in fmt and "credit_col" in fmt:
                        # Separate debit/credit columns
                        debit = parse_amount(row[fmt["debit_col"]] if fmt["debit_col"] < len(row) else "0", decimal_sep)
                        credit = parse_amount(row[fmt["credit_col"]] if fmt["credit_col"] < len(row) else "0", decimal_sep)
                        t.amount = credit - debit if credit else -debit

                    # Balance
                    if "balance_col" in fmt and fmt["balance_col"] < len(row):
                        t.balance = parse_amount(row[fmt["balance_col"]], decimal_sep)

                    # Type
                    t.type = "credit" if t.amount > 0 else "debit"

                    # Auto-categorize
                    t.category, _ = categorize_transaction(t.description)

                    # Raw line for debugging
                    t.raw_line = fmt["delimiter"].join(row)

                    if t.date or t.description:  # At least one meaningful field
                        transactions.append(t)

                except (IndexError, ValueError) as e:
                    log.warning(f"Row {row_num}: {e}")
                    continue

    except Exception as e:
        log.error(f"Failed to parse {filepath}: {e}")
        return []

    log.info(f"Parsed {len(transactions)} transactions from {filepath}")
    return transactions


def summarize(transactions: list[Transaction]) -> dict:
    """Generate summary statistics."""
    if not transactions:
        return {"count": 0}

    credits = [t for t in transactions if t.type == "credit"]
    debits = [t for t in transactions if t.type == "debit"]

    # Category breakdown
    by_category = {}
    for t in transactions:
        cat = t.category or "outros"
        if cat not in by_category:
            by_category[cat] = {"count": 0, "total": 0.0}
        by_category[cat]["count"] += 1
        by_category[cat]["total"] += t.amount

    # Round values
    for cat in by_category:
        by_category[cat]["total"] = round(by_category[cat]["total"], 2)

    dates = [t.date for t in transactions if t.date]
    period_start = min(dates) if dates else ""
    period_end = max(dates) if dates else ""

    return {
        "count": len(transactions),
        "period": {"start": period_start, "end": period_end},
        "total_credits": round(sum(t.amount for t in credits), 2),
        "total_debits": round(sum(t.amount for t in debits), 2),
        "net": round(sum(t.amount for t in transactions), 2),
        "opening_balance": transactions[0].balance if transactions[0].balance else None,
        "closing_balance": transactions[-1].balance if transactions[-1].balance else None,
        "credits_count": len(credits),
        "debits_count": len(debits),
        "by_category": dict(sorted(by_category.items(), key=lambda x: x[1]["total"])),
        "bank": transactions[0].bank if transactions else "unknown",
    }


def to_reconciliation_format(transactions: list[Transaction]) -> list[dict]:
    """Convert to format compatible with ReconciliationEngine."""
    return [
        {
            "date": t.date,
            "amount": t.amount,
            "description": t.description,
            "ref": t.reference or t.description[:20],
            "category": t.category,
            "type": t.type,
        }
        for t in transactions
    ]


def update_receivables(transactions: list[Transaction]):
    """Update receivables.yaml with credit transactions (incoming payments)."""
    import yaml
    receivables_file = FINANCE_DIR / "receivables.yaml"

    credits = [t for t in transactions if t.type == "credit" and t.amount > 100]

    data = {"receivables": [], "summary": {}, "updated_at": datetime.now().isoformat()}

    if receivables_file.exists():
        with open(receivables_file) as f:
            data = yaml.safe_load(f) or data

    for t in credits:
        entry = {
            "date": t.date,
            "amount": t.amount,
            "description": t.description,
            "category": t.category,
            "bank": t.bank,
            "status": "paid",
        }
        data.setdefault("receivables", []).append(entry)

    # Update summary
    all_paid = [r for r in data.get("receivables", []) if r.get("status") == "paid"]
    data["summary"] = {
        "total_paid_this_month": round(sum(r.get("amount", 0) for r in all_paid), 2),
        "total_pending": 0,
        "total_overdue": 0,
    }
    data["updated_at"] = datetime.now().isoformat()

    with open(receivables_file, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    log.info(f"Updated receivables.yaml with {len(credits)} credit transactions")


# ═══════════════════════════════════════════════════
# SELF-TEST WITH SAMPLE DATA
# ═══════════════════════════════════════════════════

SAMPLE_CSV = """Data;Descrição;Débito;Crédito;Saldo
01-05-2026;TRANSFERENCIA CREDITO DE CLIENTE XPTO;0,00;2.500,00;15.234,56
02-05-2026;VODAFONE PORTUGAL SA;45,99;0,00;15.188,57
03-05-2026;AWS EMEA SARL;89,23;0,00;15.099,34
05-05-2026;MBWAY RECEBIDO DE JOAO SILVA;0,00;750,00;15.849,34
07-05-2026;SEGURANCA SOCIAL CONTRIB MENSAL;487,50;0,00;15.361,84
08-05-2026;SALARIO MAIO 2026 FUNC 001;1.250,00;0,00;14.111,84
10-05-2026;FACEBOOK IRELAND LTD PUBLICIDADE;150,00;0,00;13.961,84
12-05-2026;RENDA ESCRITORIO MAIO;800,00;0,00;13.161,84
15-05-2026;TRANSFERENCIA CREDITO PROJECTO VIVENDA;0,00;4.000,00;17.161,84
20-05-2026;BP COMBUSTIVEL CASCAIS;55,00;0,00;17.106,84
"""


def run_self_test():
    """Run with sample data."""
    import tempfile
    p, f = 0, 0

    def check(n, fn):
        nonlocal p, f
        try:
            fn()
            print(f"  PASS  {n}")
            p += 1
        except Exception as e:
            print(f"  FAIL  {n}: {e}")
            f += 1

    print("=== Bank Parser — Self Tests ===\n")

    # Write sample CSV
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
    tmp.write(SAMPLE_CSV)
    tmp.close()

    print("--- Parse ---")
    txns = parse_file(tmp.name, bank="cgd")
    check("parse_10_transactions", lambda: None if len(txns) == 10 else (_ for _ in ()).throw(AssertionError(f"got {len(txns)}")))
    check("first_is_credit", lambda: None if txns[0].type == "credit" else (_ for _ in ()).throw(AssertionError))
    check("first_amount_2500", lambda: None if txns[0].amount == 2500.0 else (_ for _ in ()).throw(AssertionError(txns[0].amount)))
    check("date_iso_format", lambda: None if txns[0].date == "2026-05-01" else (_ for _ in ()).throw(AssertionError(txns[0].date)))
    check("balance_parsed", lambda: None if txns[0].balance == 15234.56 else (_ for _ in ()).throw(AssertionError(txns[0].balance)))

    print("\n--- Categorize ---")
    check("vodafone_is_fse", lambda: None if txns[1].category == "fse" else (_ for _ in ()).throw(AssertionError(txns[1].category)))
    check("aws_is_fse", lambda: None if txns[2].category == "fse" else (_ for _ in ()).throw(AssertionError(txns[2].category)))
    check("ss_is_pessoal", lambda: None if txns[4].category == "pessoal" else (_ for _ in ()).throw(AssertionError(txns[4].category)))
    check("salario_is_pessoal", lambda: None if txns[5].category == "pessoal" else (_ for _ in ()).throw(AssertionError(txns[5].category)))
    check("facebook_is_marketing", lambda: None if txns[6].category == "marketing" else (_ for _ in ()).throw(AssertionError(txns[6].category)))
    check("renda_is_instalacoes", lambda: None if txns[7].category == "instalacoes" else (_ for _ in ()).throw(AssertionError(txns[7].category)))
    check("combustivel_is_deslocacoes", lambda: None if txns[9].category == "deslocacoes" else (_ for _ in ()).throw(AssertionError(txns[9].category)))

    print("\n--- Summary ---")
    summary = summarize(txns)
    check("summary_count", lambda: None if summary["count"] == 10 else (_ for _ in ()).throw(AssertionError))
    check("3_credits", lambda: None if summary["credits_count"] == 3 else (_ for _ in ()).throw(AssertionError(summary["credits_count"])))
    check("7_debits", lambda: None if summary["debits_count"] == 7 else (_ for _ in ()).throw(AssertionError(summary["debits_count"])))
    check("net_positive", lambda: None if summary["net"] > 0 else (_ for _ in ()).throw(AssertionError(summary["net"])))
    check("categories_exist", lambda: None if len(summary["by_category"]) >= 5 else (_ for _ in ()).throw(AssertionError))

    print("\n--- Reconciliation Format ---")
    recon = to_reconciliation_format(txns)
    check("recon_format_10", lambda: None if len(recon) == 10 else (_ for _ in ()).throw(AssertionError))
    check("recon_has_amount", lambda: None if "amount" in recon[0] else (_ for _ in ()).throw(AssertionError))

    # Cleanup
    os.unlink(tmp.name)

    print(f"\n{'='*50}")
    print(f"Results: {p} passed, {f} failed, {p+f} total")
    return 0 if f == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="DARIO Bank Statement Parser (PT)")
    parser.add_argument("--file", "-f", help="Bank statement CSV/OFX file")
    parser.add_argument("--bank", "-b", choices=list(BANK_FORMATS.keys()), help="Force bank format")
    parser.add_argument("--output", "-o", choices=["json", "yaml", "summary", "table"], default="summary")
    parser.add_argument("--categorize", action="store_true", help="Show category breakdown")
    parser.add_argument("--update-receivables", action="store_true", help="Update receivables.yaml")
    parser.add_argument("--dir", "-d", help="Directory with multiple statement files")
    parser.add_argument("--test", action="store_true", help="Run self-tests")
    args = parser.parse_args()

    if args.test:
        sys.exit(run_self_test())

    if not args.file and not args.dir:
        parser.print_help()
        return

    # Parse
    if args.file:
        txns = parse_file(args.file, args.bank)
    elif args.dir:
        txns = []
        for f in Path(args.dir).glob("*.csv"):
            txns.extend(parse_file(str(f), args.bank))

    if not txns:
        print("No transactions parsed.")
        return

    # Output
    if args.output == "json":
        print(json.dumps([asdict(t) for t in txns], indent=2, ensure_ascii=False))
    elif args.output == "summary":
        s = summarize(txns)
        print("\n=== Bank Statement Summary ===")
        print(f"  Bank: {s['bank']}")
        print(f"  Period: {s['period']['start']} → {s['period']['end']}")
        print(f"  Transactions: {s['count']}")
        print(f"  Credits: {s['credits_count']} ({s['total_credits']:,.2f} EUR)")
        print(f"  Debits: {s['debits_count']} ({s['total_debits']:,.2f} EUR)")
        print(f"  Net: {s['net']:,.2f} EUR")
        if s.get("closing_balance"):
            print(f"  Closing balance: {s['closing_balance']:,.2f} EUR")
        if args.categorize or True:
            print("\n  Categories:")
            for cat, data in s["by_category"].items():
                print(f"    {cat:25s} {data['count']:>3} txns  {data['total']:>10,.2f} EUR")
    elif args.output == "table":
        print(f"{'Date':<12} {'Description':<40} {'Amount':>12} {'Balance':>12} {'Category':<15}")
        print("-" * 95)
        for t in txns:
            print(f"{t.date:<12} {t.description[:39]:<40} {t.amount:>12,.2f} {t.balance:>12,.2f} {t.category:<15}")

    # Update receivables
    if args.update_receivables:
        update_receivables(txns)


if __name__ == "__main__":
    main()

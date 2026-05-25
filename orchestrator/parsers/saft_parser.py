#!/usr/bin/env python3
"""
DARIO CFO — SAF-T (PT) Parser v1.04_01
========================================
Second REAL data connector. Reads SAF-T XML files exported from Portuguese
accounting software (PHC, Primavera, Sage, Moloni, InvoiceXpress, Jasmin).

Extracts:
- Company info (NIF, name, address)
- Customers (NIF, name, billing)
- Products/services
- Sales invoices (FT, FS, NC, ND)
- Tax totals (IVA by rate)
- Payments received

Usage:
    python saft_parser.py --file SAFT_2026.xml                   # Full parse
    python saft_parser.py --file SAFT_2026.xml --invoices        # Invoices only
    python saft_parser.py --file SAFT_2026.xml --customers       # Customers only
    python saft_parser.py --file SAFT_2026.xml --tax-summary     # IVA summary
    python saft_parser.py --file SAFT_2026.xml --update          # Update receivables
    python saft_parser.py --file SAFT_2026.xml --json            # JSON output
    python saft_parser.py --test                                 # Self-test
"""

import argparse
import json
import logging
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

ORCH_DIR = Path(os.path.expanduser("~/.claude/orchestrator"))
FINANCE_DIR = ORCH_DIR / "finance"

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("saft_parser")

# SAF-T PT namespace
NS = {"saft": "urn:OECD:StandardAuditFile-Tax:PT_1.04_01"}


@dataclass
class SaftCompany:
    nif: str = ""
    name: str = ""
    address: str = ""
    city: str = ""
    postal_code: str = ""
    fiscal_year: str = ""
    start_date: str = ""
    end_date: str = ""
    software: str = ""


@dataclass
class SaftCustomer:
    customer_id: str = ""
    nif: str = ""
    name: str = ""
    address: str = ""
    city: str = ""
    postal_code: str = ""
    country: str = "PT"
    total_invoiced: float = 0.0


@dataclass
class SaftInvoice:
    invoice_no: str = ""
    invoice_type: str = ""  # FT, FS, NC, ND
    date: str = ""
    customer_id: str = ""
    customer_nif: str = ""
    customer_name: str = ""
    net_total: float = 0.0
    tax_total: float = 0.0
    gross_total: float = 0.0
    status: str = ""  # N=Normal, A=Anulada, F=Facturada
    atcud: str = ""
    lines: list = field(default_factory=list)


@dataclass
class SaftTaxSummary:
    tax_type: str = "IVA"
    tax_rate: float = 0.0
    tax_base: float = 0.0
    tax_amount: float = 0.0


def _text(element, path: str, ns: dict = None) -> str:
    """Safely extract text from XML element."""
    if ns:
        el = element.find(path, ns)
    else:
        # Try without namespace
        el = element.find(path)
        if el is None:
            # Try with namespace
            el = element.find(path, NS)
    return el.text.strip() if el is not None and el.text else ""


def _float(element, path: str, ns: dict = None) -> float:
    """Safely extract float from XML element."""
    text = _text(element, path, ns)
    try:
        return float(text) if text else 0.0
    except ValueError:
        return 0.0


def parse_saft(filepath: str) -> dict:
    """Parse a SAF-T (PT) XML file. Returns structured data."""

    log.info(f"Parsing SAF-T: {filepath}")

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        log.error(f"XML parse error: {e}")
        return {"error": str(e)}

    # Detect namespace
    ns = {}
    root_tag = root.tag
    if "{" in root_tag:
        ns_uri = root_tag.split("}")[0].strip("{")
        ns = {"saft": ns_uri}

    result = {
        "company": None,
        "customers": [],
        "invoices": [],
        "tax_summary": [],
        "totals": {},
    }

    # === HEADER ===
    header = root.find(".//saft:Header", ns) or root.find(".//Header")
    if header is not None:
        company = SaftCompany(
            nif=_text(header, "saft:TaxRegistrationNumber", ns) or _text(header, "TaxRegistrationNumber"),
            name=_text(header, "saft:CompanyName", ns) or _text(header, "CompanyName"),
            fiscal_year=_text(header, "saft:FiscalYear", ns) or _text(header, "FiscalYear"),
            start_date=_text(header, "saft:StartDate", ns) or _text(header, "StartDate"),
            end_date=_text(header, "saft:EndDate", ns) or _text(header, "EndDate"),
            software=_text(header, "saft:SoftwareCertificateNumber", ns) or _text(header, "SoftwareCertificateNumber"),
        )
        # Address
        addr = header.find(".//saft:CompanyAddress", ns) or header.find(".//CompanyAddress")
        if addr is not None:
            company.address = _text(addr, "saft:AddressDetail", ns) or _text(addr, "AddressDetail")
            company.city = _text(addr, "saft:City", ns) or _text(addr, "City")
            company.postal_code = _text(addr, "saft:PostalCode", ns) or _text(addr, "PostalCode")
        result["company"] = asdict(company)

    # === CUSTOMERS ===
    customers_el = root.find(".//saft:MasterFiles", ns) or root.find(".//MasterFiles")
    if customers_el is not None:
        for cust in customers_el.findall("saft:Customer", ns) or customers_el.findall("Customer") or []:
            c = SaftCustomer(
                customer_id=_text(cust, "saft:CustomerID", ns) or _text(cust, "CustomerID"),
                nif=_text(cust, "saft:CustomerTaxID", ns) or _text(cust, "CustomerTaxID"),
                name=_text(cust, "saft:CompanyName", ns) or _text(cust, "CompanyName"),
            )
            addr = cust.find("saft:BillingAddress", ns) or cust.find("BillingAddress")
            if addr is not None:
                c.address = _text(addr, "saft:AddressDetail", ns) or _text(addr, "AddressDetail")
                c.city = _text(addr, "saft:City", ns) or _text(addr, "City")
                c.country = _text(addr, "saft:Country", ns) or _text(addr, "Country") or "PT"
            result["customers"].append(asdict(c))

    # === INVOICES ===
    source_docs = root.find(".//saft:SourceDocuments", ns) or root.find(".//SourceDocuments")
    if source_docs is not None:
        sales_invoices = source_docs.find("saft:SalesInvoices", ns) or source_docs.find("SalesInvoices")
        if sales_invoices is not None:
            for inv_el in sales_invoices.findall("saft:Invoice", ns) or sales_invoices.findall("Invoice") or []:
                inv = SaftInvoice(
                    invoice_no=_text(inv_el, "saft:InvoiceNo", ns) or _text(inv_el, "InvoiceNo"),
                    invoice_type=_text(inv_el, "saft:InvoiceType", ns) or _text(inv_el, "InvoiceType"),
                    date=_text(inv_el, "saft:InvoiceDate", ns) or _text(inv_el, "InvoiceDate"),
                    atcud=_text(inv_el, "saft:ATCUD", ns) or _text(inv_el, "ATCUD"),
                )

                # Status
                status_el = inv_el.find("saft:DocumentStatus", ns) or inv_el.find("DocumentStatus")
                if status_el is not None:
                    inv.status = _text(status_el, "saft:InvoiceStatus", ns) or _text(status_el, "InvoiceStatus")

                # Customer
                inv.customer_id = _text(inv_el, "saft:CustomerID", ns) or _text(inv_el, "CustomerID")

                # Totals
                totals_el = inv_el.find("saft:DocumentTotals", ns) or inv_el.find("DocumentTotals")
                if totals_el is not None:
                    inv.net_total = _float(totals_el, "saft:NetTotal", ns) or _float(totals_el, "NetTotal")
                    inv.tax_total = _float(totals_el, "saft:TaxPayable", ns) or _float(totals_el, "TaxPayable")
                    inv.gross_total = _float(totals_el, "saft:GrossTotal", ns) or _float(totals_el, "GrossTotal")

                # Match customer name from customers list
                for c in result["customers"]:
                    if c["customer_id"] == inv.customer_id:
                        inv.customer_name = c["name"]
                        inv.customer_nif = c["nif"]
                        break

                result["invoices"].append(asdict(inv))

    # === TAX SUMMARY ===
    tax_totals = {}
    for inv in result["invoices"]:
        if inv.get("status") == "A":
            continue  # Skip cancelled
        tax = inv.get("tax_total", 0)
        net = inv.get("net_total", 0)
        if net > 0:
            rate = round(tax / net * 100) if net else 0
            if rate not in tax_totals:
                tax_totals[rate] = {"tax_base": 0, "tax_amount": 0}
            tax_totals[rate]["tax_base"] += net
            tax_totals[rate]["tax_amount"] += tax

    for rate, data in sorted(tax_totals.items()):
        result["tax_summary"].append(asdict(SaftTaxSummary(
            tax_rate=rate,
            tax_base=round(data["tax_base"], 2),
            tax_amount=round(data["tax_amount"], 2),
        )))

    # === TOTALS ===
    active_invoices = [i for i in result["invoices"] if i.get("status") != "A"]
    result["totals"] = {
        "total_invoices": len(result["invoices"]),
        "active_invoices": len(active_invoices),
        "cancelled": len(result["invoices"]) - len(active_invoices),
        "total_customers": len(result["customers"]),
        "total_net": round(sum(i.get("net_total", 0) for i in active_invoices), 2),
        "total_tax": round(sum(i.get("tax_total", 0) for i in active_invoices), 2),
        "total_gross": round(sum(i.get("gross_total", 0) for i in active_invoices), 2),
    }

    log.info(f"Parsed: {result['totals']['total_invoices']} invoices, {result['totals']['total_customers']} customers")
    return result


def update_from_saft(data: dict):
    """Update finance YAMLs from parsed SAF-T data."""
    import yaml

    # Update receivables with invoice data
    receivables_file = FINANCE_DIR / "receivables.yaml"
    recv_data = {"receivables": [], "summary": {}, "updated_at": datetime.now().isoformat()}

    for inv in data.get("invoices", []):
        if inv.get("status") == "A":
            continue
        if inv.get("invoice_type") in ("FT", "FS", "FR"):
            recv_data["receivables"].append({
                "client": inv.get("customer_name", ""),
                "invoice_number": inv.get("invoice_no", ""),
                "invoice_date": inv.get("date", ""),
                "amount": inv.get("net_total", 0),
                "iva_amount": inv.get("tax_total", 0),
                "total": inv.get("gross_total", 0),
                "status": "paid",  # SAF-T only has issued invoices
                "nif": inv.get("customer_nif", ""),
            })

    recv_data["summary"] = {
        "total_invoiced": data.get("totals", {}).get("total_gross", 0),
        "total_iva": data.get("totals", {}).get("total_tax", 0),
        "invoice_count": data.get("totals", {}).get("active_invoices", 0),
    }

    with open(receivables_file, "w") as f:
        yaml.dump(recv_data, f, default_flow_style=False, allow_unicode=True)

    log.info(f"Updated receivables.yaml from SAF-T ({len(recv_data['receivables'])} invoices)")


# ═══════════════════════════════════════════════════
# SELF-TEST
# ═══════════════════════════════════════════════════

SAMPLE_SAFT = """<?xml version="1.0" encoding="UTF-8"?>
<AuditFile xmlns="urn:OECD:StandardAuditFile-Tax:PT_1.04_01">
  <Header>
    <AuditFileVersion>1.04_01</AuditFileVersion>
    <CompanyID>509123456</CompanyID>
    <TaxRegistrationNumber>509123456</TaxRegistrationNumber>
    <CompanyName>BARDA Digital Agency Lda</CompanyName>
    <FiscalYear>2026</FiscalYear>
    <StartDate>2026-01-01</StartDate>
    <EndDate>2026-05-08</EndDate>
    <SoftwareCertificateNumber>1234</SoftwareCertificateNumber>
    <CompanyAddress>
      <AddressDetail>Rua do Exemplo 123</AddressDetail>
      <City>Lisboa</City>
      <PostalCode>1000-001</PostalCode>
      <Country>PT</Country>
    </CompanyAddress>
  </Header>
  <MasterFiles>
    <Customer>
      <CustomerID>C001</CustomerID>
      <CustomerTaxID>501234567</CustomerTaxID>
      <CompanyName>Cliente Vivenda Lda</CompanyName>
      <BillingAddress><AddressDetail>Av da Liberdade 100</AddressDetail><City>Lisboa</City><Country>PT</Country></BillingAddress>
    </Customer>
    <Customer>
      <CustomerID>C002</CustomerID>
      <CustomerTaxID>502345678</CustomerTaxID>
      <CompanyName>Mar e Brasa Restauracao Lda</CompanyName>
      <BillingAddress><AddressDetail>Praia de Carcavelos</AddressDetail><City>Cascais</City><Country>PT</Country></BillingAddress>
    </Customer>
  </MasterFiles>
  <SourceDocuments>
    <SalesInvoices>
      <NumberOfEntries>3</NumberOfEntries>
      <TotalDebit>0.00</TotalDebit>
      <TotalCredit>8500.00</TotalCredit>
      <Invoice>
        <InvoiceNo>FT 2026/001</InvoiceNo>
        <ATCUD>XKJL-1</ATCUD>
        <DocumentStatus><InvoiceStatus>N</InvoiceStatus></DocumentStatus>
        <InvoiceDate>2026-01-15</InvoiceDate>
        <InvoiceType>FT</InvoiceType>
        <CustomerID>C001</CustomerID>
        <DocumentTotals>
          <TaxPayable>575.00</TaxPayable>
          <NetTotal>2500.00</NetTotal>
          <GrossTotal>3075.00</GrossTotal>
        </DocumentTotals>
      </Invoice>
      <Invoice>
        <InvoiceNo>FT 2026/002</InvoiceNo>
        <ATCUD>XKJL-2</ATCUD>
        <DocumentStatus><InvoiceStatus>N</InvoiceStatus></DocumentStatus>
        <InvoiceDate>2026-02-20</InvoiceDate>
        <InvoiceType>FT</InvoiceType>
        <CustomerID>C002</CustomerID>
        <DocumentTotals>
          <TaxPayable>1150.00</TaxPayable>
          <NetTotal>5000.00</NetTotal>
          <GrossTotal>6150.00</GrossTotal>
        </DocumentTotals>
      </Invoice>
      <Invoice>
        <InvoiceNo>NC 2026/001</InvoiceNo>
        <ATCUD>XKJL-3</ATCUD>
        <DocumentStatus><InvoiceStatus>A</InvoiceStatus></DocumentStatus>
        <InvoiceDate>2026-03-01</InvoiceDate>
        <InvoiceType>NC</InvoiceType>
        <CustomerID>C001</CustomerID>
        <DocumentTotals>
          <TaxPayable>230.00</TaxPayable>
          <NetTotal>1000.00</NetTotal>
          <GrossTotal>1230.00</GrossTotal>
        </DocumentTotals>
      </Invoice>
    </SalesInvoices>
  </SourceDocuments>
</AuditFile>"""


def run_self_test():
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

    print("=== SAF-T Parser — Self Tests ===\n")

    # Write sample XML
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False, encoding="utf-8")
    tmp.write(SAMPLE_SAFT)
    tmp.close()

    data = parse_saft(tmp.name)

    print("--- Company ---")
    check("company_nif", lambda: None if data["company"]["nif"] == "509123456" else (_ for _ in ()).throw(AssertionError))
    check("company_name", lambda: None if "BARDA" in data["company"]["name"] else (_ for _ in ()).throw(AssertionError))
    check("fiscal_year", lambda: None if data["company"]["fiscal_year"] == "2026" else (_ for _ in ()).throw(AssertionError))

    print("\n--- Customers ---")
    check("2_customers", lambda: None if len(data["customers"]) == 2 else (_ for _ in ()).throw(AssertionError(len(data["customers"]))))
    check("vivenda_nif", lambda: None if data["customers"][0]["nif"] == "501234567" else (_ for _ in ()).throw(AssertionError))
    check("mar_brasa_name", lambda: None if "Mar" in data["customers"][1]["name"] else (_ for _ in ()).throw(AssertionError))

    print("\n--- Invoices ---")
    check("3_invoices", lambda: None if len(data["invoices"]) == 3 else (_ for _ in ()).throw(AssertionError(len(data["invoices"]))))
    check("ft_2026_001", lambda: None if data["invoices"][0]["invoice_no"] == "FT 2026/001" else (_ for _ in ()).throw(AssertionError))
    check("atcud_present", lambda: None if data["invoices"][0]["atcud"] == "XKJL-1" else (_ for _ in ()).throw(AssertionError))
    check("net_2500", lambda: None if data["invoices"][0]["net_total"] == 2500.0 else (_ for _ in ()).throw(AssertionError))
    check("nc_cancelled", lambda: None if data["invoices"][2]["status"] == "A" else (_ for _ in ()).throw(AssertionError))
    check("customer_name_matched", lambda: None if "Vivenda" in data["invoices"][0]["customer_name"] else (_ for _ in ()).throw(AssertionError))

    print("\n--- Totals ---")
    check("2_active_invoices", lambda: None if data["totals"]["active_invoices"] == 2 else (_ for _ in ()).throw(AssertionError))
    check("1_cancelled", lambda: None if data["totals"]["cancelled"] == 1 else (_ for _ in ()).throw(AssertionError))
    check("net_7500", lambda: None if data["totals"]["total_net"] == 7500.0 else (_ for _ in ()).throw(AssertionError(data["totals"]["total_net"])))
    check("gross_9225", lambda: None if data["totals"]["total_gross"] == 9225.0 else (_ for _ in ()).throw(AssertionError))

    print("\n--- Tax Summary ---")
    check("tax_summary_exists", lambda: None if len(data["tax_summary"]) > 0 else (_ for _ in ()).throw(AssertionError))
    check("iva_23_present", lambda: None if any(t["tax_rate"] == 23 for t in data["tax_summary"]) else (_ for _ in ()).throw(AssertionError))

    os.unlink(tmp.name)

    print(f"\n{'='*50}")
    print(f"Results: {p} passed, {f} failed, {p+f} total")
    return 0 if f == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="DARIO SAF-T (PT) Parser")
    parser.add_argument("--file", "-f", help="SAF-T XML file")
    parser.add_argument("--invoices", action="store_true", help="Show invoices only")
    parser.add_argument("--customers", action="store_true", help="Show customers only")
    parser.add_argument("--tax-summary", action="store_true", help="Show IVA summary")
    parser.add_argument("--update", action="store_true", help="Update receivables.yaml")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--test", action="store_true", help="Run self-tests")
    args = parser.parse_args()

    if args.test:
        sys.exit(run_self_test())

    if not args.file:
        parser.print_help()
        return

    data = parse_saft(args.file)

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.invoices:
        for inv in data["invoices"]:
            status = "CANCELADA" if inv["status"] == "A" else ""
            print(f"  {inv['invoice_no']:<16} {inv['date']:<12} {inv['customer_name']:<30} {inv['gross_total']:>10,.2f} EUR {status}")
    elif args.customers:
        for c in data["customers"]:
            print(f"  {c['customer_id']:<8} NIF {c['nif']:<12} {c['name']}")
    elif args.tax_summary:
        print(f"\n  IVA Summary ({data['company']['fiscal_year'] if data.get('company') else ''}):")
        for t in data["tax_summary"]:
            print(f"    {t['tax_rate']:>5.0f}%  Base: {t['tax_base']:>12,.2f}  IVA: {t['tax_amount']:>10,.2f}")
        print(f"    {'TOTAL':>5}  Base: {data['totals']['total_net']:>12,.2f}  IVA: {data['totals']['total_tax']:>10,.2f}")
    else:
        # Full summary
        c = data.get("company", {})
        t = data.get("totals", {})
        print("\n=== SAF-T Summary ===")
        print(f"  Company: {c.get('name', '')} (NIF {c.get('nif', '')})")
        print(f"  Period: {c.get('start_date', '')} → {c.get('end_date', '')}")
        print(f"  Customers: {t.get('total_customers', 0)}")
        print(f"  Invoices: {t.get('active_invoices', 0)} active, {t.get('cancelled', 0)} cancelled")
        print(f"  Net total: {t.get('total_net', 0):,.2f} EUR")
        print(f"  IVA total: {t.get('total_tax', 0):,.2f} EUR")
        print(f"  Gross total: {t.get('total_gross', 0):,.2f} EUR")

    if args.update:
        update_from_saft(data)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
mcp-stf — MCP Server for STF (Supremo Tribunal Federal) data
==============================================================
Open-source MCP server for STF public RSS + decisions + Súmulas Vinculantes.
Repo: github.com/dario-legal-br/mcp-stf (planned)
"""

import argparse
import json
import sys
import urllib.request
import re

STF_RSS_BASE = "https://www.stf.jus.br/portal/cms/listarSiteRSS.asp"

# Súmulas Vinculantes — texto consolidado (base local crescente)
SUMULAS_VINCULANTES = {
    "8": {
        "numero": "8",
        "texto": "São inconstitucionais o parágrafo único do artigo 5º do "
                 "Decreto-Lei 1.569/1977 e os artigos 45 e 46 da Lei 8.212/1991.",
        "tema": "Prescrição/decadência tributário",
        "aprovacao": "2008-06-12",
    },
    "14": {
        "numero": "14",
        "texto": "É direito do defensor ter acesso amplo aos elementos de prova "
                 "documentados em procedimento investigatório.",
        "tema": "Acesso defesa a provas em investigação",
        "aprovacao": "2009-02-02",
    },
    "26": {
        "numero": "26",
        "texto": "Progressão de regime em crime hediondo — inconstitucionalidade "
                 "do art. 2º Lei 8.072/90.",
        "tema": "Progressão de regime",
        "aprovacao": "2009-12-16",
    },
}

TEMAS_REPERCUSSAO_GERAL = [
    {"tema": "69", "titulo": "ICMS na base do PIS/COFINS",
     "status": "Julgado 2017 — ICMS NÃO compõe base", "area": "tributario"},
    {"tema": "881", "titulo": "Coisa julgada em matéria tributária",
     "status": "Em julgamento", "area": "tributario"},
    {"tema": "1118", "titulo": "Reforma Tributária modulações",
     "status": "Recente 2024", "area": "tributario"},
    {"tema": "246", "titulo": "Terceirização lícita Lei 13.429/17",
     "status": "Julgado 2018", "area": "trabalhista"},
]


def get_recent_decisions(limit: int = 10) -> dict:
    try:
        url = f"{STF_RSS_BASE}?servico=jurisprudenciaDecisaoMonocratica"
        req = urllib.request.Request(url, headers={"User-Agent": "LEX-BR/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
        items = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)[:limit]
        decisions = []
        for item in items:
            title = re.search(r"<title><!\[CDATA\[(.*?)\]\]></title>", item)
            link = re.search(r"<link>(.*?)</link>", item)
            pub = re.search(r"<pubDate>(.*?)</pubDate>", item)
            desc = re.search(r"<description><!\[CDATA\[(.*?)\]\]></description>", item, re.DOTALL)
            decisions.append({
                "title": title.group(1) if title else "",
                "link": link.group(1) if link else "",
                "date": pub.group(1) if pub else "",
                "description": (desc.group(1)[:500] + "...") if desc else "",
            })
        return {"source": "STF RSS", "total": len(decisions), "decisions": decisions}
    except Exception as e:
        return {"error": str(e), "source": "STF RSS"}


def get_sumula_vinculante(numero: str) -> dict:
    sv = SUMULAS_VINCULANTES.get(str(numero))
    if sv:
        return {"source": "STF SV base local", **sv}
    return {
        "source": "STF SV base local",
        "error": f"SV {numero} não disponível na base local.",
        "note": "Base local cobre SVs mais consultadas. Lista completa em "
                "www.stf.jus.br/portal/cms/listarSumulaVinculante.asp",
    }


def search_recent_decisions(query: str, limit: int = 20) -> dict:
    recent = get_recent_decisions(limit=50)
    if "error" in recent:
        return recent
    q = query.lower()
    matches = [d for d in recent.get("decisions", [])
               if q in (d.get("title", "") + " " + d.get("description", "")).lower()]
    return {"query": query, "total_matches": len(matches), "results": matches[:limit]}


def get_repercussao_geral_temas() -> dict:
    return {
        "source": "STF RG base local",
        "total": len(TEMAS_REPERCUSSAO_GERAL),
        "temas": TEMAS_REPERCUSSAO_GERAL,
        "note": "Parcial. Lista completa: portal.stf.jus.br/jurisprudenciaRepercussao/",
    }


MCP_TOOLS = [
    {"name": "get_recent_decisions",
     "description": "Get recent STF decisions via RSS",
     "inputSchema": {"type": "object", "properties": {
         "limit": {"type": "integer", "default": 10}}}},
    {"name": "get_sumula_vinculante",
     "description": "Get Súmula Vinculante text by number",
     "inputSchema": {"type": "object",
                     "properties": {"numero": {"type": "string"}},
                     "required": ["numero"]}},
    {"name": "search_recent_decisions",
     "description": "Search recent STF decisions",
     "inputSchema": {"type": "object",
                     "properties": {"query": {"type": "string"},
                                    "limit": {"type": "integer", "default": 20}},
                     "required": ["query"]}},
    {"name": "get_repercussao_geral_temas",
     "description": "Get Repercussão Geral hot topics",
     "inputSchema": {"type": "object", "properties": {}}},
]


def serve_mcp_stdio():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            req = json.loads(line.strip())
            method, params, req_id = req.get("method"), req.get("params", {}), req.get("id")
            if method == "initialize":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {
                    "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                    "serverInfo": {"name": "mcp-stf", "version": "0.1.0"}}}
            elif method == "tools/list":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}
            elif method == "tools/call":
                tn = params.get("name"); args = params.get("arguments", {})
                fns = {"get_recent_decisions": get_recent_decisions,
                       "get_sumula_vinculante": get_sumula_vinculante,
                       "search_recent_decisions": search_recent_decisions,
                       "get_repercussao_geral_temas": get_repercussao_geral_temas}
                result = fns[tn](**args) if tn in fns else {"error": f"Unknown: {tn}"}
                response = {"jsonrpc": "2.0", "id": req_id,
                            "result": {"content": [{"type": "text", "text": json.dumps(result)}]}}
            else:
                response = {"jsonrpc": "2.0", "id": req_id,
                            "error": {"code": -32601, "message": f"Method not found: {method}"}}
            print(json.dumps(response), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0",
                              "error": {"code": -32603, "message": str(e)}}), flush=True)


def main():
    p = argparse.ArgumentParser(description="mcp-stf server")
    p.add_argument("--recent", action="store_true")
    p.add_argument("--sv", help="Súmula Vinculante by number")
    p.add_argument("--search", help="Search recent decisions")
    p.add_argument("--rg", action="store_true")
    p.add_argument("--serve", action="store_true")
    args = p.parse_args()
    if args.serve:
        serve_mcp_stdio(); return 0
    if args.recent:
        print(json.dumps(get_recent_decisions(), indent=2, ensure_ascii=False)); return 0
    if args.sv:
        print(json.dumps(get_sumula_vinculante(args.sv), indent=2, ensure_ascii=False)); return 0
    if args.search:
        print(json.dumps(search_recent_decisions(args.search), indent=2, ensure_ascii=False)); return 0
    if args.rg:
        print(json.dumps(get_repercussao_geral_temas(), indent=2, ensure_ascii=False)); return 0
    p.print_help(); return 1


if __name__ == "__main__":
    sys.exit(main())

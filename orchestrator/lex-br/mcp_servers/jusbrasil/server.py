#!/usr/bin/env python3
"""
mcp-jusbrasil — MCP Server for JusBrasil API
============================================
Open-source MCP server for JusBrasil jurisprudence API.
Repo: github.com/dario-legal-br/mcp-jusbrasil (planned)

JusBrasil API: api.jusbrasil.com.br/docs
Provides: jurisprudência STF/STJ/TJs, súmulas, legislação consolidada

Status: STUB v0.1 — structure ready, real API integration pending API key
from JusBrasil. Returns mock data with realistic structure until live.

Tools exposed:
  - search_jurisprudence(query, court, limit) — buscar acórdãos
  - get_sumula(tribunal, numero) — texto de súmula
  - search_legislation(query, lei_numero) — buscar legislação

CLI:
    python server.py --search "rescisão indireta"
    python server.py --sumula STJ 145
    python server.py --serve  # MCP server mode (stdio)
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

JUSBRASIL_API_BASE = "https://api.jusbrasil.com.br/v1"
API_KEY = os.environ.get("JUSBRASIL_API_KEY")  # set in environment


# Mock data for stub mode (when no API key)
MOCK_JURISPRUDENCE = {
    "rescisão indireta": [
        {
            "id": "stj-9876543",
            "tribunal": "STJ",
            "processo": "1234567-89.2023.5.02.0001",
            "relator": "Min. Maria José Silva",
            "data": "2023-08-15",
            "ementa": "RESCISÃO INDIRETA. ASSÉDIO MORAL. CONFIGURADO. "
                     "Comprovado o tratamento humilhante reiterado por superior...",
            "url": "https://www.jusbrasil.com.br/processos/stj-9876543",
        },
    ],
    "estabilidade gestante": [
        {
            "id": "tst-8765432",
            "tribunal": "TST",
            "processo": "8765432-10.2023.5.02.0002",
            "relator": "Min. João Carlos Pereira",
            "data": "2023-09-20",
            "ementa": "ESTABILIDADE GESTANTE. ART. 10, II, ADCT. "
                     "Reintegração devida. Súmula 244 TST...",
            "url": "https://www.jusbrasil.com.br/processos/tst-8765432",
        },
    ],
}

SUMULAS = {
    ("STJ", "145"): {
        "tribunal": "STJ",
        "numero": "145",
        "texto": "No transporte desinteressado, de simples cortesia, o "
                 "transportador só será civilmente responsável por danos "
                 "causados ao transportado quando incorrer em dolo ou culpa "
                 "grave.",
        "data_aprovacao": "1995-04-27",
    },
    ("TST", "244"): {
        "tribunal": "TST",
        "numero": "244",
        "texto": "Gestante. Estabilidade Provisória. I - O desconhecimento "
                 "do estado gravídico pelo empregador não afasta o direito ao "
                 "pagamento da indenização decorrente da estabilidade...",
        "data_aprovacao": "2012-12-14",
    },
}


def search_jurisprudence(query: str, court: str | None = None,
                         limit: int = 10) -> dict:
    """Search jurisprudência on JusBrasil API.

    In stub mode (no API key): returns mock data matching query keywords.
    In live mode: calls real JusBrasil API.
    """
    if not API_KEY:
        # STUB MODE — return mock data
        query_lower = query.lower()
        for keyword, results in MOCK_JURISPRUDENCE.items():
            if keyword.lower() in query_lower or query_lower in keyword.lower():
                if court:
                    results = [r for r in results if r["tribunal"] == court.upper()]
                return {
                    "mode": "STUB",
                    "query": query,
                    "results": results[:limit],
                    "total": len(results),
                    "note": "Live API key not configured (JUSBRASIL_API_KEY env var). "
                            "Returning mock data for development.",
                }
        return {
            "mode": "STUB",
            "query": query,
            "results": [],
            "total": 0,
            "note": "No mock data for this query. Configure JUSBRASIL_API_KEY for live data.",
        }

    # LIVE MODE — real API call
    params = {"q": query, "limit": limit}
    if court:
        params["tribunal"] = court
    url = f"{JUSBRASIL_API_BASE}/jurisprudence/search?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        return {
            "mode": "LIVE",
            "query": query,
            "results": data.get("results", []),
            "total": data.get("total", 0),
        }
    except Exception as e:
        return {"mode": "ERROR", "error": str(e), "query": query}


def get_sumula(tribunal: str, numero: str) -> dict:
    """Get súmula text by tribunal + numero."""
    if not API_KEY:
        # STUB MODE
        key = (tribunal.upper(), str(numero))
        if key in SUMULAS:
            return {"mode": "STUB", **SUMULAS[key]}
        return {
            "mode": "STUB",
            "tribunal": tribunal,
            "numero": numero,
            "error": "Súmula não encontrada no mock data.",
        }
    # LIVE MODE
    url = f"{JUSBRASIL_API_BASE}/sumulas/{tribunal}/{numero}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return {"mode": "LIVE", **json.loads(resp.read())}
    except Exception as e:
        return {"mode": "ERROR", "error": str(e)}


def search_legislation(query: str, lei_numero: str | None = None) -> dict:
    """Search legislação consolidada."""
    if not API_KEY:
        return {
            "mode": "STUB",
            "query": query,
            "results": [],
            "note": "Legislation search requires live API key (JUSBRASIL_API_KEY).",
        }
    # LIVE MODE
    params = {"q": query}
    if lei_numero:
        params["lei"] = lei_numero
    url = f"{JUSBRASIL_API_BASE}/legislation/search?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return {"mode": "LIVE", **json.loads(resp.read())}
    except Exception as e:
        return {"mode": "ERROR", "error": str(e)}


# MCP Protocol implementation (stdio JSON-RPC)
MCP_TOOLS = [
    {
        "name": "search_jurisprudence",
        "description": "Search Brazilian jurisprudence (STF, STJ, TJs, TST) by keyword",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "court": {"type": "string", "description": "Tribunal (STF/STJ/TST/etc.)",
                          "enum": ["STF", "STJ", "TST", "TSE", "STM"]},
                "limit": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_sumula",
        "description": "Get text of a súmula by tribunal and number",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tribunal": {"type": "string", "enum": ["STF", "STJ", "TST", "TSE"]},
                "numero": {"type": "string"},
            },
            "required": ["tribunal", "numero"],
        },
    },
    {
        "name": "search_legislation",
        "description": "Search Brazilian consolidated legislation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "lei_numero": {"type": "string"},
            },
            "required": ["query"],
        },
    },
]


def serve_mcp_stdio():
    """MCP server mode — reads JSON-RPC from stdin, writes to stdout."""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            req = json.loads(line.strip())
            method = req.get("method")
            params = req.get("params", {})
            req_id = req.get("id")

            if method == "initialize":
                response = {
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "mcp-jusbrasil", "version": "0.1.0"},
                    },
                }
            elif method == "tools/list":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}
            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})
                if tool_name == "search_jurisprudence":
                    result = search_jurisprudence(**args)
                elif tool_name == "get_sumula":
                    result = get_sumula(**args)
                elif tool_name == "search_legislation":
                    result = search_legislation(**args)
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}
                response = {
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
                }
            else:
                response = {
                    "jsonrpc": "2.0", "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"},
                }
            print(json.dumps(response), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0",
                              "error": {"code": -32603, "message": str(e)}}),
                  flush=True)


def main():
    p = argparse.ArgumentParser(description="mcp-jusbrasil server")
    p.add_argument("--search", help="Search jurisprudence")
    p.add_argument("--court", help="Filter by court")
    p.add_argument("--sumula", nargs=2, metavar=("TRIBUNAL", "NUMERO"))
    p.add_argument("--legislation", help="Search legislation")
    p.add_argument("--serve", action="store_true", help="Run as MCP server (stdio)")
    args = p.parse_args()

    if args.serve:
        serve_mcp_stdio()
        return 0

    if args.search:
        result = search_jurisprudence(args.search, court=args.court)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    if args.sumula:
        result = get_sumula(*args.sumula)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    if args.legislation:
        result = search_legislation(args.legislation)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

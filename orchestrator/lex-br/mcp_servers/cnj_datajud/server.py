#!/usr/bin/env python3
"""
mcp-cnj-datajud — MCP Server for CNJ DataJud API (oficial)
============================================================
Open-source MCP server for CNJ DataJud public API.
Repo: github.com/dario-legal-br/mcp-cnj-datajud (planned)

CNJ DataJud: https://datajud-wiki.cnj.jus.br/api-publica/
ENDPOINT: https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search

Provides: metadados processuais oficiais de todos os tribunais brasileiros
(STJ, STF, TRFs, TJs, TRTs, TSE). API gratuita, sem necessidade de API key.

Authentication: Bearer token público compartilhado (do CNJ).

Tools exposed:
  - search_process(numero_processo, tribunal) — buscar metadados de processo
  - search_by_class(classe, tribunal, date_range) — pesquisar por classe
  - get_movements(numero_processo, tribunal) — andamentos
"""

import argparse
import json
import os
import sys
import urllib.request

DATAJUD_BASE = "https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"
# Token público compartilhado (vide datajud-wiki.cnj.jus.br)
DATAJUD_TOKEN = os.environ.get(
    "DATAJUD_TOKEN",
    "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
)

TRIBUNAIS_VALIDOS = {
    "stj", "stf", "tst", "tse",
    "trf1", "trf2", "trf3", "trf4", "trf5", "trf6",
    # TJs estaduais (todos)
    "tjac", "tjal", "tjam", "tjap", "tjba", "tjce", "tjdft", "tjes",
    "tjgo", "tjma", "tjmg", "tjms", "tjmt", "tjpa", "tjpb", "tjpe",
    "tjpi", "tjpr", "tjrj", "tjrn", "tjro", "tjrr", "tjrs", "tjsc",
    "tjse", "tjsp", "tjto",
    # TRTs (24 regiões)
    *(f"trt{i}" for i in range(1, 25)),
}


def _datajud_request(tribunal: str, query_body: dict) -> dict:
    """POST query to DataJud API."""
    tribunal = tribunal.lower()
    if tribunal not in TRIBUNAIS_VALIDOS:
        return {"error": f"Tribunal inválido: {tribunal}. Use sigla CNJ (ex: tjsp, trt2)"}

    url = DATAJUD_BASE.format(tribunal=tribunal)
    data = json.dumps(query_body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"APIKey {DATAJUD_TOKEN}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e), "tribunal": tribunal}


def search_process(numero_processo: str, tribunal: str) -> dict:
    """Busca metadados de um processo pelo número CNJ.

    Numero formato: NNNNNNN-DD.AAAA.J.TR.OOOO
    Ex: 1234567-89.2023.5.02.0001
    """
    query = {
        "query": {
            "match": {"numeroProcesso": numero_processo}
        },
        "size": 1,
    }
    result = _datajud_request(tribunal, query)
    if "error" in result:
        return result

    hits = result.get("hits", {}).get("hits", [])
    if not hits:
        return {
            "found": False,
            "numero_processo": numero_processo,
            "tribunal": tribunal,
            "message": "Processo não encontrado no DataJud.",
        }

    source = hits[0].get("_source", {})
    return {
        "found": True,
        "numero_processo": numero_processo,
        "tribunal": tribunal,
        "data": {
            "classe": source.get("classe", {}),
            "assuntos": source.get("assuntos", []),
            "orgao_julgador": source.get("orgaoJulgador", {}),
            "movimentos_count": len(source.get("movimentos", [])),
            "data_ajuizamento": source.get("dataAjuizamento"),
            "grau": source.get("grau"),
            "ultima_atualizacao": source.get("dataHoraUltimaAtualizacao"),
        },
    }


def search_by_class(classe_codigo: int, tribunal: str,
                    size: int = 20) -> dict:
    """Pesquisa processos por código de classe (CNJ).

    Códigos de classe: vide tabelas TPU CNJ.
    Ex: 436 = Ação Trabalhista, 1107 = Procedimento Comum Cível
    """
    query = {
        "query": {
            "match": {"classe.codigo": classe_codigo}
        },
        "size": min(size, 100),
        "sort": [{"dataAjuizamento": "desc"}],
    }
    result = _datajud_request(tribunal, query)
    if "error" in result:
        return result

    hits = result.get("hits", {}).get("hits", [])
    return {
        "found": len(hits),
        "tribunal": tribunal,
        "classe_codigo": classe_codigo,
        "results": [
            {
                "numero_processo": h.get("_source", {}).get("numeroProcesso"),
                "data_ajuizamento": h.get("_source", {}).get("dataAjuizamento"),
                "orgao": h.get("_source", {}).get("orgaoJulgador", {}).get("nome"),
            }
            for h in hits
        ],
    }


def get_movements(numero_processo: str, tribunal: str) -> dict:
    """Retorna lista de andamentos do processo."""
    query = {
        "query": {"match": {"numeroProcesso": numero_processo}},
        "size": 1,
    }
    result = _datajud_request(tribunal, query)
    if "error" in result:
        return result

    hits = result.get("hits", {}).get("hits", [])
    if not hits:
        return {"found": False, "numero_processo": numero_processo}

    movimentos = hits[0].get("_source", {}).get("movimentos", [])
    return {
        "found": True,
        "numero_processo": numero_processo,
        "tribunal": tribunal,
        "movimentos_count": len(movimentos),
        "movimentos": [
            {
                "data_hora": m.get("dataHora"),
                "codigo": m.get("codigo"),
                "nome": m.get("nome"),
                "complementos": m.get("complementosTabelados", []),
            }
            for m in sorted(movimentos, key=lambda x: x.get("dataHora", ""), reverse=True)[:50]
        ],
    }


MCP_TOOLS = [
    {
        "name": "search_process",
        "description": "Search Brazilian court process metadata via CNJ DataJud (official)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "numero_processo": {"type": "string",
                                    "description": "CNJ format: NNNNNNN-DD.AAAA.J.TR.OOOO"},
                "tribunal": {"type": "string",
                             "description": "CNJ tribunal slug: stj, stf, tjsp, trt2, etc."},
            },
            "required": ["numero_processo", "tribunal"],
        },
    },
    {
        "name": "search_by_class",
        "description": "Search processes by CNJ class code",
        "inputSchema": {
            "type": "object",
            "properties": {
                "classe_codigo": {"type": "integer",
                                  "description": "CNJ class code (ex: 436 = Ação Trabalhista)"},
                "tribunal": {"type": "string"},
                "size": {"type": "integer", "default": 20, "maximum": 100},
            },
            "required": ["classe_codigo", "tribunal"],
        },
    },
    {
        "name": "get_movements",
        "description": "Get process movements (andamentos)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "numero_processo": {"type": "string"},
                "tribunal": {"type": "string"},
            },
            "required": ["numero_processo", "tribunal"],
        },
    },
]


def serve_mcp_stdio():
    """MCP server stdio mode."""
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
                        "serverInfo": {"name": "mcp-cnj-datajud", "version": "0.1.0"},
                    },
                }
            elif method == "tools/list":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}
            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})
                if tool_name == "search_process":
                    result = search_process(**args)
                elif tool_name == "search_by_class":
                    result = search_by_class(**args)
                elif tool_name == "get_movements":
                    result = get_movements(**args)
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}
                response = {
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
                }
            else:
                response = {"jsonrpc": "2.0", "id": req_id,
                            "error": {"code": -32601, "message": f"Method not found: {method}"}}
            print(json.dumps(response), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0",
                              "error": {"code": -32603, "message": str(e)}}),
                  flush=True)


def main():
    p = argparse.ArgumentParser(description="mcp-cnj-datajud server")
    p.add_argument("--process", help="Search process by number")
    p.add_argument("--tribunal", help="Tribunal slug (lowercase)")
    p.add_argument("--movements", help="Get movements of a process")
    p.add_argument("--class-search", type=int, help="Search by class code")
    p.add_argument("--serve", action="store_true")
    args = p.parse_args()

    if args.serve:
        serve_mcp_stdio()
        return 0

    if args.process and args.tribunal:
        r = search_process(args.process, args.tribunal)
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0

    if args.movements and args.tribunal:
        r = get_movements(args.movements, args.tribunal)
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0

    if args.class_search and args.tribunal:
        r = search_by_class(args.class_search, args.tribunal)
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

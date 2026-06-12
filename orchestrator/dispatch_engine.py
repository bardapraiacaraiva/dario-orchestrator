#!/usr/bin/env python3
"""Shim de compatibilidade — delega para dispatch.dispatch_engine (código real em dispatch/).
Criado 2026-06-03: o skill lucas-heartbeat referencia o caminho na raiz, mas o código
vive em packages. NÃO duplica lógica — corre o módulo real preservando os argumentos."""
import os
import runpy
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
runpy.run_module("dispatch.dispatch_engine", run_name="__main__", alter_sys=True)

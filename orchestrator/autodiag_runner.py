#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shim de compatibilidade — delega para core.autodiag_runner (código real em core/).
Criado 2026-06-03: o skill lucas-heartbeat referencia o caminho na raiz, mas o código
vive em packages. NÃO duplica lógica — corre o módulo real preservando os argumentos."""
import os, sys, runpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
runpy.run_module("core.autodiag_runner", run_name="__main__", alter_sys=True)

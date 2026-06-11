#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shim de compatibilidade — delega para finance.budget_tracker (código real em finance/).
Criado 2026-06-03: o skill lucas-heartbeat referencia scripts/budget_tracker.py, mas o
código vive em finance/. NÃO duplica lógica — corre o módulo real preservando os argumentos."""
import os, sys, runpy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
runpy.run_module("finance.budget_tracker", run_name="__main__", alter_sys=True)

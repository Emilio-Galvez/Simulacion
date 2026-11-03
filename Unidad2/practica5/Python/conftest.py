r"""Pruebas unitarias y de integracion del proyecto LCG en Python.

Ejecucion:

    cd "Practica 5/Python"
    python -m pytest pruebas -v
"""

from __future__ import annotations

import os
import sys

RAIZ_PYTHON = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ_PYTHON not in sys.path:
    sys.path.insert(0, RAIZ_PYTHON)

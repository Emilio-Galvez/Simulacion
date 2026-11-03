"""Pruebas automatizadas de la implementacion Python del LCG."""

from __future__ import annotations

import os
import sys

RAIZ_PYTHON = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ_PYTHON not in sys.path:
    sys.path.insert(0, RAIZ_PYTHON)

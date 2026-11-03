"""Estrategias de generacion de numeros pseudoaleatorios (patron Strategy)."""

from estrategias.estrategia_lcg import EstrategiaLCG
from estrategias.interfaz_generador import Generador, ParametrosInvalidosError

__all__ = ["EstrategiaLCG", "Generador", "ParametrosInvalidosError"]

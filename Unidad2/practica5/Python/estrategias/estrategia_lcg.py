"""Estrategia concreta del Generador Congruencial Lineal (LCG).

Implementa la recurrencia clasica:

    X(n+1) = (a * X(n) + c) mod m

y la normalizacion U(n) = X(n) / m.

Pertenece a la CAPA DE LOGICA DE NEGOCIO.
"""

from __future__ import annotations

from estrategias.interfaz_generador import Generador, ParametrosInvalidosError

MULTIPLICADOR_POR_DEFECTO = 1664525
INCREMENTO_POR_DEFECTO = 1013904223
MODULO_POR_DEFECTO = 2**32
SEMILLA_POR_DEFECTO = 12345
CANTIDAD_POR_DEFECTO = 10000


class EstrategiaLCG(Generador):
    """Generador Congruencial Lineal con parametros configurables."""

    def __init__(
        self,
        multiplicador: int = MULTIPLICADOR_POR_DEFECTO,
        incremento: int = INCREMENTO_POR_DEFECTO,
        modulo: int = MODULO_POR_DEFECTO,
        semilla: int = SEMILLA_POR_DEFECTO,
    ) -> None:
        self._validar_parametros(multiplicador, incremento, modulo, semilla)
        self._multiplicador = multiplicador
        self._incremento = incremento
        self._modulo = modulo
        self._semilla = semilla

    @staticmethod
    def _validar_parametros(multiplicador: int, incremento: int, modulo: int, semilla: int) -> None:
        """Valida los parametros matematicos del generador."""
        if not isinstance(multiplicador, int) or not isinstance(incremento, int):
            raise ParametrosInvalidosError("a y c deben ser valores enteros.")
        if not isinstance(modulo, int) or not isinstance(semilla, int):
            raise ParametrosInvalidosError("m y la semilla deben ser valores enteros.")
        if multiplicador <= 0:
            raise ParametrosInvalidosError("El multiplicador a debe ser mayor que cero.")
        if modulo <= 1:
            raise ParametrosInvalidosError("El modulo m debe ser mayor que uno.")
        if not 0 <= incremento < modulo:
            raise ParametrosInvalidosError("El incremento c debe cumplir 0 <= c < m.")
        if not 0 <= semilla < modulo:
            raise ParametrosInvalidosError("La semilla debe cumplir 0 <= X(0) < m.")

    def generar(self, cantidad: int) -> list[int]:
        """Devuelve los estados crudos X(1), X(2), ... X(cantidad)."""
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ParametrosInvalidosError("La cantidad generada debe ser un entero no negativo.")

        estados: list[int] = []
        estado = self._semilla
        for _ in range(cantidad):
            estado = (self._multiplicador * estado + self._incremento) % self._modulo
            estados.append(estado)
        return estados

    def normalizar(self, estado: int) -> float:
        """Normaliza un estado crudo: U(n) = X(n) / m."""
        if not 0 <= estado < self._modulo:
            raise ParametrosInvalidosError("El estado a normalizar esta fuera del rango [0, m).")
        return estado / self._modulo

    @property
    def multiplicador(self) -> int:
        return self._multiplicador

    @property
    def incremento(self) -> int:
        return self._incremento

    @property
    def modulo(self) -> int:
        return self._modulo

    @property
    def semilla(self) -> int:
        return self._semilla

    @property
    def nombre(self) -> str:
        return "LCG"

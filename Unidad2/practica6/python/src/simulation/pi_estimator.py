"""Estimacion determinista de pi para completar la tabla de la guia.

La guia solicita una columna "pi estimado", pero no define el procedimiento.
Para no introducir Monte Carlo ni inventar datos, se usa la serie alterna de
Leibniz con la misma cantidad N de terminos que de numeros procesados:

    pi = 4 * sum_{k=0}^{N-1} (-1)^k / (2k + 1)

Es un calculo determinista, equivalente en Python y Java, y permite comparar
el error absoluto para los cuatro tamanos solicitados. No se deriva de la
secuencia LCG; esta decision se documenta en el README.
"""

from __future__ import annotations

import math

REAL_PI = 3.141592653589793


class PiEstimator:
    """Estimador determinista basado en la serie de Leibniz."""

    @staticmethod
    def estimate(terms: int) -> float:
        if terms <= 0:
            raise ValueError("La cantidad de terminos debe ser positiva.")

        total = 0.0
        sign = 1.0
        for k in range(terms):
            total += sign / (2 * k + 1)
            sign = -sign
        return 4.0 * total

    @staticmethod
    def absolute_error(estimate: float) -> float:
        return abs(REAL_PI - estimate)

    @staticmethod
    def reference_value() -> float:
        return REAL_PI

    @staticmethod
    def is_valid_estimate(value: float) -> bool:
        return math.isfinite(value) and value > 0.0

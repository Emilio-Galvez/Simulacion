"""Funciones numericas compartidas por las pruebas estadisticas.

Se implementan en Python puro para que Java pueda usar exactamente los mismos
algoritmos y no dependender de SciPy.
"""

from __future__ import annotations

import math

_EPS = 3.0e-14
_FPMIN = 1.0e-300
_ITMAX = 1000
_LANCZOS = (
    0.99999999999980993,
    676.5203681218851,
    -1259.1392167224028,
    771.32342877765313,
    -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
    9.9843695780195716e-6,
    1.5056327351493116e-7,
)


def log_gamma(z: float) -> float:
    """Logaritmo de la funcion gamma mediante la aproximacion de Lanczos."""

    if z < 0.5:
        return math.log(math.pi) - math.log(math.sin(math.pi * z)) - log_gamma(1.0 - z)

    z -= 1.0
    x = _LANCZOS[0]
    for i in range(1, 9):
        x += _LANCZOS[i] / (z + i)
    t = z + 7.5
    return 0.5 * math.log(2.0 * math.pi) + (z + 0.5) * math.log(t) - t + math.log(x)


def _gamma_series(a: float, x: float) -> float:
    ap = a
    summation = 1.0 / a
    delta = summation
    for _ in range(_ITMAX):
        ap += 1.0
        delta *= x / ap
        summation += delta
        if abs(delta) < abs(summation) * _EPS:
            break
    return summation * math.exp(-x + a * math.log(x) - log_gamma(a))


def _gamma_continued_fraction(a: float, x: float) -> float:
    b = x + 1.0 - a
    c = 1.0 / _FPMIN
    d = 1.0 / b
    h = d
    for i in range(1, _ITMAX + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < _FPMIN:
            d = _FPMIN
        c = b + an / c
        if abs(c) < _FPMIN:
            c = _FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < _EPS:
            break
    return math.exp(-x + a * math.log(x) - log_gamma(a)) * h


def regularized_gamma_q(a: float, x: float) -> float:
    """Funcion gamma incompleta regularizada superior Q(a, x)."""

    if a <= 0.0:
        raise ValueError("a debe ser positiva.")
    if x < 0.0:
        raise ValueError("x no puede ser negativo.")
    if x == 0.0:
        return 1.0
    if x < a + 1.0:
        return 1.0 - _gamma_series(a, x)
    return _gamma_continued_fraction(a, x)


def chi_square_survival(statistic: float, degrees_of_freedom: int) -> float:
    """Valor p de una prueba Chi-cuadrado."""

    if degrees_of_freedom <= 0:
        raise ValueError("Los grados de libertad deben ser positivos.")
    if statistic <= 0.0:
        return 1.0
    return regularized_gamma_q(degrees_of_freedom / 2.0, statistic / 2.0)


def kolmogorov_survival(lam: float) -> float:
    """Funcion de supervivencia asintotica de Kolmogorov-Smirnov."""

    if lam <= 0.0:
        return 1.0
    if lam < 0.1:
        return 1.0

    a2 = -2.0 * lam * lam
    fac = 2.0
    total = 0.0
    term = 1.0
    previous = 0.0

    for _ in range(1, 1001):
        term *= math.exp(a2)
        total += fac * term
        fac = -fac
        if abs(term) <= 1.0e-6 * previous or abs(term) <= 1.0e-16 * abs(total):
            break
        previous = abs(term)

    return min(1.0, max(0.0, total))


def kolmogorov_smirnov_p_value(statistic: float, sample_size: int) -> float:
    """Valor p con la correccion de muestra finita de Stephens."""

    if sample_size <= 0:
        raise ValueError("El tamano de muestra debe ser positivo.")
    root_n = math.sqrt(sample_size)
    lam = (root_n + 0.12 + 0.11 / root_n) * statistic
    return kolmogorov_survival(lam)

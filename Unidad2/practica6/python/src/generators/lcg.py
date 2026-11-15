"""Generador congruencial lineal (LCG).

Implementa exactamente:

    X(n+1) = (a * X(n) + c) mod m
    U(n)   = X(n+1) / m

Los estados se conservan como enteros de Python, por lo que no hay
desbordamiento. Los valores U se obtienen con la misma division IEEE-754 que
en Java.
"""

from __future__ import annotations

from models.results import GenerationResult


class LCGError(ValueError):
    """Parametros invalidos del generador."""


class LCG:
    """Generador congruencial lineal configurable."""

    def __init__(self, seed: int, multiplier: int, increment: int, modulus: int) -> None:
        if modulus <= 1:
            raise LCGError("El modulo debe ser mayor que 1.")
        if not 0 <= seed < modulus:
            raise LCGError("La semilla debe cumplir 0 <= semilla < modulo.")
        if not 0 < multiplier < modulus:
            raise LCGError("El multiplicador debe cumplir 0 < a < modulo.")
        if not 0 <= increment < modulus:
            raise LCGError("El incremento debe cumplir 0 <= c < modulo.")

        self._seed = seed
        self._multiplier = multiplier
        self._increment = increment
        self._modulus = modulus
        self._state = seed

    @property
    def seed(self) -> int:
        return self._seed

    @property
    def multiplier(self) -> int:
        return self._multiplier

    @property
    def increment(self) -> int:
        return self._increment

    @property
    def modulus(self) -> int:
        return self._modulus

    @property
    def state(self) -> int:
        return self._state

    def next_state(self) -> int:
        """Avanza un paso y devuelve X(n+1)."""

        self._state = (self._multiplier * self._state + self._increment) % self._modulus
        return self._state

    def next_uniform(self) -> float:
        """Avanza un paso y devuelve U(n) = X(n+1) / m."""

        return self.next_state() / self._modulus

    def generate(self, count: int) -> GenerationResult:
        """Genera ``count`` estados y sus valores uniformes asociados."""

        if count < 0:
            raise LCGError("La cantidad de numeros no puede ser negativa.")

        states: list[int] = []
        uniforms: list[float] = []
        state = self._state
        modulus = self._modulus
        multiplier = self._multiplier
        increment = self._increment

        for _ in range(count):
            state = (multiplier * state + increment) % modulus
            states.append(state)
            uniforms.append(state / modulus)

        self._state = state
        return GenerationResult(states=states, uniforms=uniforms)

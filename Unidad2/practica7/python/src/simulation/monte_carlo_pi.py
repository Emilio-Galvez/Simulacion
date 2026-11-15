"""Estimacion de pi mediante el metodo Monte Carlo.

Se generan N puntos uniformes en el cuadrado [0, 1) x [0, 1) y se cuentan los
que caen dentro del circulo unitario x^2 + y^2 <= 1. Como el area del cuarto de
circulo es pi/4, la estimacion es:

    pi_estimado = 4 * (Nc / N)

donde Nc es la cantidad de puntos dentro del circulo. El generador utilizado es
el RNG nativo de cada lenguaje con la misma semilla; por tanto, el procedimiento
es comparable, aunque las secuencias no son identicas entre Python y Java.
"""

from __future__ import annotations

import random
import time

from models.results import Measurement, Summary

REAL_PI = 3.141592653589793


class MonteCarloPi:
    """Ejecuta el experimento Monte Carlo con un RNG nativo reproducible."""

    def __init__(self, seed: int, real_pi: float = REAL_PI) -> None:
        self._seed = seed
        self._real_pi = real_pi

    def run_once(self, n: int, repetition: int = 1) -> Measurement:
        if n <= 0:
            raise ValueError("La cantidad de puntos debe ser positiva.")

        rng = random.Random(self._seed)
        inside = 0
        start = time.perf_counter_ns()
        for _ in range(n):
            x = rng.random()
            y = rng.random()
            if x * x + y * y <= 1.0:
                inside += 1
        elapsed_s = (time.perf_counter_ns() - start) / 1_000_000_000

        estimate = 4.0 * inside / n
        return Measurement(
            n=n,
            repetition=repetition,
            inside=inside,
            pi_estimate=estimate,
            error=abs(self._real_pi - estimate),
            time_s=elapsed_s,
        )

    def run(self, n: int, repetitions: int) -> Summary:
        if repetitions <= 0:
            raise ValueError("El numero de repeticiones debe ser positivo.")

        measurements = tuple(
            self.run_once(n=n, repetition=repetition)
            for repetition in range(1, repetitions + 1)
        )
        first = measurements[0]
        return Summary(
            n=n,
            inside=first.inside,
            pi_estimate=first.pi_estimate,
            error=first.error,
            measurements=measurements,
        )

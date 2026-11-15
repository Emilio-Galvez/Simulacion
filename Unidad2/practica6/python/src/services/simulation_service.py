"""Orquestacion de generacion, pruebas estadisticas y medicion de tiempos."""

from __future__ import annotations

import time

from config import SimulationConfig
from generators.lcg import LCG
from models.results import SimulationResult, TimingResult
from simulation.pi_estimator import PiEstimator
from statistics.chi_square import ChiSquareTest
from statistics.kolmogorov_smirnov import KolmogorovSmirnovTest
from statistics.statistical_test import StatisticalTest


class SimulationService:
    """Ejecuta una simulacion completa para cada tamano de muestra."""

    def __init__(self, config: SimulationConfig, tests: list[StatisticalTest] | None = None) -> None:
        self._config = config
        self._tests = tests if tests is not None else [
            ChiSquareTest(config.bins),
            KolmogorovSmirnovTest(),
        ]

    def _new_lcg(self) -> LCG:
        return LCG(
            seed=self._config.seed,
            multiplier=self._config.multiplier,
            increment=self._config.increment,
            modulus=self._config.modulus,
        )

    def warm_up(self) -> None:
        """Ejecuta un ciclo pequeno para excluir el arranque del interprete."""

        self.run(1000)

    def run(self, n: int) -> SimulationResult:
        if n <= 0:
            raise ValueError("n debe ser positivo.")

        start_generation = time.perf_counter_ns()
        generation = self._new_lcg().generate(n)
        end_generation = time.perf_counter_ns()

        chi_square = None
        kolmogorov_smirnov = None
        chi_square_ns = 0
        kolmogorov_smirnov_ns = 0

        for test in self._tests:
            start = time.perf_counter_ns()
            result = test.run(generation.uniforms, self._config.alpha)
            elapsed = time.perf_counter_ns() - start
            if isinstance(test, ChiSquareTest):
                chi_square = result
                chi_square_ns = elapsed
            elif isinstance(test, KolmogorovSmirnovTest):
                kolmogorov_smirnov = result
                kolmogorov_smirnov_ns = elapsed

        if chi_square is None or kolmogorov_smirnov is None:
            raise RuntimeError("Se requieren las estrategias Chi-cuadrado y Kolmogorov-Smirnov.")

        start_pi = time.perf_counter_ns()
        pi_estimate = PiEstimator.estimate(n)
        pi_ns = time.perf_counter_ns() - start_pi

        timings = TimingResult(
            generation_ns=end_generation - start_generation,
            chi_square_ns=chi_square_ns,
            kolmogorov_smirnov_ns=kolmogorov_smirnov_ns,
            pi_ns=pi_ns,
        )
        return SimulationResult(
            n=n,
            generation=generation,
            chi_square=chi_square,
            kolmogorov_smirnov=kolmogorov_smirnov,
            pi_estimate=pi_estimate,
            pi_error=PiEstimator.absolute_error(pi_estimate),
            timings=timings,
        )

    def run_all(self, sizes: tuple[int, ...] | None = None) -> list[SimulationResult]:
        selected = sizes if sizes is not None else self._config.sample_sizes
        return [self.run(n) for n in selected]

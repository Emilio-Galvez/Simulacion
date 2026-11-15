"""Orquestacion del experimento Monte Carlo y medicion de tiempos."""

from __future__ import annotations

from config import SimulationConfig
from models.results import Summary
from simulation.monte_carlo_pi import MonteCarloPi


class SimulationService:
    """Ejecuta el experimento para cada tamano de muestra configurado."""

    def __init__(self, config: SimulationConfig) -> None:
        self._config = config

    def _new_experiment(self) -> MonteCarloPi:
        return MonteCarloPi(seed=self._config.seed, real_pi=self._config.real_pi)

    def warm_up(self) -> None:
        """Ejecuta una muestra grande para calentar el interprete y la JVM."""

        self._new_experiment().run_once(self._config.warmup_size)

    def run(self, n: int) -> Summary:
        return self._new_experiment().run(n=n, repetitions=self._config.repetitions)

    def run_all(self, sizes: tuple[int, ...] | None = None) -> list[Summary]:
        selected = sizes if sizes is not None else self._config.sample_sizes
        return [self.run(n) for n in selected]

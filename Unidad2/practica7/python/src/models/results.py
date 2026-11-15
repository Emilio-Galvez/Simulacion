"""Modelos de datos de la Practica 7."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median


@dataclass(frozen=True)
class Measurement:
    """Una ejecucion individual del experimento Monte Carlo."""

    n: int
    repetition: int
    inside: int
    pi_estimate: float
    error: float
    time_s: float


@dataclass(frozen=True)
class Summary:
    """Resumen de las repeticiones para un tamano de muestra N."""

    n: int
    inside: int
    pi_estimate: float
    error: float
    measurements: tuple[Measurement, ...]

    @property
    def times_s(self) -> tuple[float, ...]:
        return tuple(measurement.time_s for measurement in self.measurements)

    @property
    def median_time_s(self) -> float:
        return median(self.times_s)

    @property
    def mean_time_s(self) -> float:
        return mean(self.times_s)

    @property
    def min_time_s(self) -> float:
        return min(self.times_s)

    @property
    def max_time_s(self) -> float:
        return max(self.times_s)

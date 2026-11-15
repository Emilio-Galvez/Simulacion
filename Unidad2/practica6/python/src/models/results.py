"""Modelos de datos de la Practica 6."""

from __future__ import annotations

from dataclasses import dataclass, field

from statistics.statistical_test import StatisticalTestResult


@dataclass(frozen=True)
class GenerationResult:
    """Estados enteros y valores uniformes generados por el LCG."""

    states: list[int]
    uniforms: list[float]

    @property
    def count(self) -> int:
        return len(self.states)


@dataclass(frozen=True)
class TimingResult:
    """Tiempos en nanosegundos de cada etapa medida."""

    generation_ns: int
    chi_square_ns: int
    kolmogorov_smirnov_ns: int
    pi_ns: int

    @property
    def total_ns(self) -> int:
        return (
            self.generation_ns
            + self.chi_square_ns
            + self.kolmogorov_smirnov_ns
            + self.pi_ns
        )

    def as_seconds(self) -> dict[str, float]:
        return {
            "generation_s": self.generation_ns / 1_000_000_000,
            "chi_square_s": self.chi_square_ns / 1_000_000_000,
            "kolmogorov_smirnov_s": self.kolmogorov_smirnov_ns / 1_000_000_000,
            "pi_s": self.pi_ns / 1_000_000_000,
            "total_s": self.total_ns / 1_000_000_000,
        }


@dataclass(frozen=True)
class SimulationResult:
    """Resultado completo de una ejecucion para un tamano N."""

    n: int
    generation: GenerationResult
    chi_square: StatisticalTestResult
    kolmogorov_smirnov: StatisticalTestResult
    pi_estimate: float
    pi_error: float
    timings: TimingResult


@dataclass(frozen=True)
class ComparisonRow:
    """Fila de comparacion entre Python y Java."""

    n: int
    pi_python: float
    pi_java: float
    error_python: float
    error_java: float
    time_python_s: float
    time_java_s: float
    chi2_stat_python: float
    chi2_stat_java: float
    chi2_p_python: float
    chi2_p_java: float
    ks_d_python: float
    ks_d_java: float
    ks_p_python: float
    ks_p_java: float
    states_equal: bool
    max_uniform_diff: float
    details: dict[str, float] = field(default_factory=dict)

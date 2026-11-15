"""Prueba Kolmogorov-Smirnov de una muestra contra U(0, 1)."""

from __future__ import annotations

from collections.abc import Sequence

from statistics.special_functions import kolmogorov_smirnov_p_value
from statistics.statistical_test import StatisticalTest, StatisticalTestResult


class KolmogorovSmirnovTest(StatisticalTest):
    """Estrategia Kolmogorov-Smirnov para una distribucion uniforme."""

    @property
    def name(self) -> str:
        return "Kolmogorov-Smirnov"

    def run(self, sample: Sequence[float], alpha: float) -> StatisticalTestResult:
        self.validate_input(sample, alpha)
        n = len(sample)
        ordered = sorted(sample)

        d_plus = 0.0
        d_minus = 0.0
        for position, value in enumerate(ordered, start=1):
            empirical_upper = position / n
            empirical_lower = (position - 1) / n
            d_plus = max(d_plus, empirical_upper - value)
            d_minus = max(d_minus, value - empirical_lower)

        statistic = max(d_plus, d_minus)
        p_value = min(1.0, max(0.0, kolmogorov_smirnov_p_value(statistic, n)))
        reject_null = p_value < alpha

        return StatisticalTestResult(
            name=self.name,
            statistic=statistic,
            p_value=p_value,
            alpha=alpha,
            reject_null=reject_null,
            details={
                "d_plus": d_plus,
                "d_minus": d_minus,
                "sample_size": n,
            },
        )

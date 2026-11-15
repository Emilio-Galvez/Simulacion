"""Prueba de bondad de ajuste Chi-cuadrado."""

from __future__ import annotations

from collections.abc import Sequence

from statistics.special_functions import chi_square_survival
from statistics.statistical_test import StatisticalTest, StatisticalTestResult


class ChiSquareTest(StatisticalTest):
    """Estrategia Chi-cuadrado para una distribucion uniforme en [0, 1)."""

    def __init__(self, bins: int = 10) -> None:
        if bins <= 1:
            raise ValueError("El numero de intervalos debe ser mayor que 1.")
        self._bins = bins

    @property
    def name(self) -> str:
        return "Chi-cuadrado"

    @property
    def bins(self) -> int:
        return self._bins

    def run(self, sample: Sequence[float], alpha: float) -> StatisticalTestResult:
        self.validate_input(sample, alpha)
        n = len(sample)
        k = self._bins
        observed = [0] * k

        for value in sample:
            index = int(value * k)
            if index >= k:
                index = k - 1
            observed[index] += 1

        expected_value = n / k
        expected = [expected_value] * k
        statistic = 0.0
        for observed_i, expected_i in zip(observed, expected):
            difference = observed_i - expected_i
            statistic += (difference * difference) / expected_i

        degrees_of_freedom = k - 1
        p_value = min(1.0, max(0.0, chi_square_survival(statistic, degrees_of_freedom)))
        reject_null = p_value < alpha

        return StatisticalTestResult(
            name=self.name,
            statistic=statistic,
            p_value=p_value,
            alpha=alpha,
            reject_null=reject_null,
            details={
                "observed": observed,
                "expected": expected,
                "degrees_of_freedom": degrees_of_freedom,
                "bins": k,
                "sample_size": n,
            },
        )

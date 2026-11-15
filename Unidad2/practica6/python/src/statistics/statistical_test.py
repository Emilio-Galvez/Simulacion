"""Contrato comun para las pruebas estadisticas (patron Strategy)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class StatisticalTestResult:
    """Resultado generico de una prueba de bondad de ajuste."""

    name: str
    statistic: float
    p_value: float
    alpha: float
    reject_null: bool
    details: dict[str, object] = field(default_factory=dict)

    @property
    def decision(self) -> str:
        return "Se rechaza H0" if self.reject_null else "No se rechaza H0"


class StatisticalTest(ABC):
    """Estrategia de validacion estadistica."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre legible de la prueba."""

    @abstractmethod
    def run(self, sample: Sequence[float], alpha: float) -> StatisticalTestResult:
        """Ejecuta la prueba sobre una muestra en [0, 1)."""

    @staticmethod
    def validate_input(sample: Sequence[float], alpha: float) -> None:
        if not 0.0 < alpha < 1.0:
            raise ValueError("alpha debe estar en (0, 1).")
        if len(sample) == 0:
            raise ValueError("La muestra no puede estar vacia.")
        for value in sample:
            if not 0.0 <= value < 1.0:
                raise ValueError(f"Valor fuera del intervalo [0, 1): {value!r}")

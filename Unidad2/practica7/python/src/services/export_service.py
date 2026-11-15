"""Exportacion de resultados Monte Carlo a CSV."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from models.results import Summary


class ExportService:
    """Escribe las mediciones individuales y el resumen por tamano de muestra."""

    def __init__(self, results_dir: Path) -> None:
        self._results_dir = results_dir

    def export_all(self, summaries: list[Summary]) -> None:
        self._results_dir.mkdir(parents=True, exist_ok=True)
        self._export_measurements(summaries)
        self._export_summary(summaries)

    def _export_measurements(self, summaries: list[Summary]) -> None:
        rows = []
        for summary in summaries:
            for measurement in summary.measurements:
                rows.append(
                    {
                        "N": measurement.n,
                        "repeticion": measurement.repetition,
                        "dentro": measurement.inside,
                        "pi_estimado": measurement.pi_estimate,
                        "error": measurement.error,
                        "tiempo_s": measurement.time_s,
                    }
                )
        pd.DataFrame(rows).to_csv(
            self._results_dir / "mediciones.csv", index=False
        )

    def _export_summary(self, summaries: list[Summary]) -> None:
        rows = []
        for summary in summaries:
            rows.append(
                {
                    "N": summary.n,
                    "dentro": summary.inside,
                    "pi_estimado": summary.pi_estimate,
                    "error": summary.error,
                    "tiempo_mediana_s": summary.median_time_s,
                    "tiempo_media_s": summary.mean_time_s,
                    "tiempo_min_s": summary.min_time_s,
                    "tiempo_max_s": summary.max_time_s,
                }
            )
        pd.DataFrame(rows).to_csv(self._results_dir / "resumen.csv", index=False)

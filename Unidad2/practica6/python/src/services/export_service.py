"""Exportacion de resultados a CSV."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

from models.results import SimulationResult


class ExportService:
    """Escribe secuencias, estadisticas, rendimiento y tabla resumen."""

    def __init__(self, results_dir: Path) -> None:
        self._results_dir = results_dir
        self._sequences_dir = results_dir / "sequences"
        self._statistics_dir = results_dir / "statistics"
        self._performance_dir = results_dir / "performance"
        self._summary_dir = results_dir / "summary"

    def export_all(self, results: list[SimulationResult]) -> None:
        for directory in (
            self._sequences_dir,
            self._statistics_dir,
            self._performance_dir,
            self._summary_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)

        for result in results:
            self._export_sequence(result)
        self._export_statistics(results)
        self._export_performance(results)
        self._export_summary(results)

    def _export_sequence(self, result: SimulationResult) -> None:
        path = self._sequences_dir / f"sequence_{result.n}.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(["index", "state", "uniform"])
            for index, (state, uniform) in enumerate(
                zip(result.generation.states, result.generation.uniforms),
                start=1,
            ):
                writer.writerow([index, state, uniform])

    def _export_statistics(self, results: list[SimulationResult]) -> None:
        chi_rows = []
        ks_rows = []
        for result in results:
            chi = result.chi_square
            observed = chi.details["observed"]
            expected = chi.details["expected"]
            row = {
                "N": result.n,
                "statistic": chi.statistic,
                "degrees_of_freedom": chi.details["degrees_of_freedom"],
                "p_value": chi.p_value,
                "alpha": chi.alpha,
                "decision": chi.decision,
            }
            for index, value in enumerate(observed):
                row[f"observed_{index}"] = value
            for index, value in enumerate(expected):
                row[f"expected_{index}"] = value
            chi_rows.append(row)

            ks = result.kolmogorov_smirnov
            ks_rows.append(
                {
                    "N": result.n,
                    "statistic": ks.statistic,
                    "d_plus": ks.details["d_plus"],
                    "d_minus": ks.details["d_minus"],
                    "p_value": ks.p_value,
                    "alpha": ks.alpha,
                    "decision": ks.decision,
                }
            )

        pd.DataFrame(chi_rows).to_csv(self._statistics_dir / "chi_square.csv", index=False)
        pd.DataFrame(ks_rows).to_csv(
            self._statistics_dir / "kolmogorov_smirnov.csv", index=False
        )

    def _export_performance(self, results: list[SimulationResult]) -> None:
        rows = []
        for result in results:
            seconds = result.timings.as_seconds()
            rows.append(
                {
                    "N": result.n,
                    "generation_s": seconds["generation_s"],
                    "chi_square_s": seconds["chi_square_s"],
                    "kolmogorov_smirnov_s": seconds["kolmogorov_smirnov_s"],
                    "pi_s": seconds["pi_s"],
                    "total_s": seconds["total_s"],
                }
            )
        pd.DataFrame(rows).to_csv(self._performance_dir / "timings.csv", index=False)

    def _export_summary(self, results: list[SimulationResult]) -> None:
        rows = []
        for result in results:
            rows.append(
                {
                    "N": result.n,
                    "pi_estimado": result.pi_estimate,
                    "error": result.pi_error,
                    "tiempo_s": result.timings.total_ns / 1_000_000_000,
                }
            )
        pd.DataFrame(rows).to_csv(self._summary_dir / "pi_table.csv", index=False)

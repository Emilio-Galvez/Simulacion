"""Comparacion de los resultados obtenidos en Python y Java."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import SimulationConfig


class ComparisonService:
    """Construye la tabla comparativa a partir de los resumenes de cada lenguaje."""

    def __init__(self, config: SimulationConfig) -> None:
        self._config = config

    def _read_summary(self, base: Path) -> pd.DataFrame:
        path = base / "resumen.csv"
        if not path.exists():
            raise FileNotFoundError(
                f"No existe {path}. Ejecute primero la implementacion correspondiente."
            )
        return pd.read_csv(path)

    def build(self) -> pd.DataFrame:
        python = self._read_summary(self._config.python_results_dir)
        java = self._read_summary(self._config.java_results_dir)

        frame = python[
            ["N", "pi_estimado", "error", "tiempo_mediana_s"]
        ].merge(
            java[["N", "pi_estimado", "error", "tiempo_mediana_s"]],
            on="N",
            suffixes=("_python", "_java"),
        )
        frame = frame.rename(
            columns={
                "tiempo_mediana_s_python": "tiempo_python_s",
                "tiempo_mediana_s_java": "tiempo_java_s",
            }
        )
        frame["diferencia_pi"] = (
            frame["pi_estimado_python"] - frame["pi_estimado_java"]
        ).abs()
        frame["diferencia_error"] = (
            frame["error_python"] - frame["error_java"]
        ).abs()
        frame["razon_tiempo_java_python"] = (
            frame["tiempo_java_s"] / frame["tiempo_python_s"]
        )
        frame["mejor_error"] = frame[["error_python", "error_java"]].min(axis=1)
        frame["mejor_lenguaje"] = frame.apply(
            lambda row: (
                "Empate"
                if abs(row["error_python"] - row["error_java"]) < 1e-15
                else ("Python" if row["error_python"] < row["error_java"] else "Java")
            ),
            axis=1,
        )
        return frame.sort_values("N").reset_index(drop=True)

    def export(self, frame: pd.DataFrame) -> None:
        directory = self._config.comparison_dir
        directory.mkdir(parents=True, exist_ok=True)

        frame.to_csv(directory / "tabla_comparativa.csv", index=False)

        requested = pd.DataFrame(
            {
                "N": frame["N"],
                "pi_estimado": frame["pi_estimado_python"],
                "error": frame["error_python"],
                "tiempo_python_s": frame["tiempo_python_s"],
                "tiempo_java_s": frame["tiempo_java_s"],
            }
        )
        requested.to_csv(directory / "tabla_solicitada.csv", index=False)

        lines = [
            "| N | pi Python | Error Python | Tiempo Python (s) | "
            "pi Java | Error Java | Tiempo Java (s) |",
            "|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for _, row in frame.iterrows():
            lines.append(
                f"| {int(row['N']):,} "
                f"| {row['pi_estimado_python']:.12f} "
                f"| {row['error_python']:.6e} "
                f"| {row['tiempo_python_s']:.6f} "
                f"| {row['pi_estimado_java']:.12f} "
                f"| {row['error_java']:.6e} "
                f"| {row['tiempo_java_s']:.6f} |"
            )
        (directory / "tabla_comparativa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    @staticmethod
    def print_table(frame: pd.DataFrame) -> None:
        print("\nTabla comparativa Python-Java (tiempos: mediana de las repeticiones)")
        print(
            f"{'N':>10} {'pi Python':>14} {'error Python':>14} "
            f"{'tiempo Python':>14} {'pi Java':>14} {'error Java':>14} "
            f"{'tiempo Java':>14}"
        )
        for _, row in frame.iterrows():
            print(
                f"{int(row['N']):>10,} "
                f"{row['pi_estimado_python']:>14.12f} "
                f"{row['error_python']:>14.6e} "
                f"{row['tiempo_python_s']:>14.6f} "
                f"{row['pi_estimado_java']:>14.12f} "
                f"{row['error_java']:>14.6e} "
                f"{row['tiempo_java_s']:>14.6f}"
            )
        print("\nTiempos y diferencias")
        for _, row in frame.iterrows():
            print(
                f"N={int(row['N']):,}: "
                f"Java/Python={row['razon_tiempo_java_python']:.3f}x, "
                f"|pi_py-pi_java|={row['diferencia_pi']:.3e}, "
                f"mejor error={row['mejor_error']:.6e} ({row['mejor_lenguaje']})"
            )

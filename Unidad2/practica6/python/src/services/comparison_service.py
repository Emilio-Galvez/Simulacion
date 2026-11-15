"""Comparacion automatica de los resultados Python y Java."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from config import SimulationConfig


class ComparisonService:
    """Lee los CSV de ambos lenguajes y construye la tabla comparativa."""

    def __init__(self, config: SimulationConfig) -> None:
        self._config = config
        self._python_dir = config.python_results_dir
        self._java_dir = config.java_results_dir

    def _read_summary(self, base: Path) -> dict[int, dict[str, float]]:
        path = base / "summary" / "pi_table.csv"
        if not path.exists():
            raise FileNotFoundError(
                f"No existe {path}. Ejecute primero la implementacion correspondiente."
            )
        frame = pd.read_csv(path)
        return {int(row["N"]): row.to_dict() for _, row in frame.iterrows()}

    def _read_statistics(self, base: Path) -> tuple[dict[int, dict], dict[int, dict]]:
        chi_path = base / "statistics" / "chi_square.csv"
        ks_path = base / "statistics" / "kolmogorov_smirnov.csv"
        if not chi_path.exists() or not ks_path.exists():
            raise FileNotFoundError(
                f"Faltan los CSV estadisticos en {base / 'statistics'}."
            )
        chi_frame = pd.read_csv(chi_path)
        ks_frame = pd.read_csv(ks_path)
        chi = {int(row["N"]): row.to_dict() for _, row in chi_frame.iterrows()}
        ks = {int(row["N"]): row.to_dict() for _, row in ks_frame.iterrows()}
        return chi, ks

    def _compare_sequences(self, n: int) -> tuple[bool, float]:
        python_path = self._python_dir / "sequences" / f"sequence_{n}.csv"
        java_path = self._java_dir / "sequences" / f"sequence_{n}.csv"
        if not python_path.exists() or not java_path.exists():
            raise FileNotFoundError(f"Faltan las secuencias para N={n}.")

        python_states = pd.read_csv(
            python_path, usecols=["state"], dtype={"state": "int64"}
        )["state"].to_numpy()
        java_states = pd.read_csv(
            java_path, usecols=["state"], dtype={"state": "int64"}
        )["state"].to_numpy()
        states_equal = (
            python_states.shape == java_states.shape
            and bool(np.array_equal(python_states, java_states))
        )

        python_uniforms = pd.read_csv(
            python_path, usecols=["uniform"], dtype={"uniform": "float64"}
        )["uniform"].to_numpy()
        java_uniforms = pd.read_csv(
            java_path, usecols=["uniform"], dtype={"uniform": "float64"}
        )["uniform"].to_numpy()
        if python_uniforms.shape != java_uniforms.shape:
            max_uniform_diff = float("inf")
        else:
            max_uniform_diff = float(np.max(np.abs(python_uniforms - java_uniforms)))

        return states_equal, max_uniform_diff

    def build(self) -> pd.DataFrame:
        python_summary = self._read_summary(self._python_dir)
        java_summary = self._read_summary(self._java_dir)
        python_chi, python_ks = self._read_statistics(self._python_dir)
        java_chi, java_ks = self._read_statistics(self._java_dir)

        rows: list[dict[str, object]] = []
        for n in self._config.sample_sizes:
            if n not in python_summary or n not in java_summary:
                continue
            states_equal, max_uniform_diff = self._compare_sequences(n)
            py_summary = python_summary[n]
            jv_summary = java_summary[n]
            py_chi = python_chi[n]
            jv_chi = java_chi[n]
            py_ks = python_ks[n]
            jv_ks = java_ks[n]

            rows.append(
                {
                    "N": n,
                    "pi_python": float(py_summary["pi_estimado"]),
                    "pi_java": float(jv_summary["pi_estimado"]),
                    "error_python": float(py_summary["error"]),
                    "error_java": float(jv_summary["error"]),
                    "time_python_s": float(py_summary["tiempo_s"]),
                    "time_java_s": float(jv_summary["tiempo_s"]),
                    "chi2_stat_python": float(py_chi["statistic"]),
                    "chi2_stat_java": float(jv_chi["statistic"]),
                    "chi2_p_python": float(py_chi["p_value"]),
                    "chi2_p_java": float(jv_chi["p_value"]),
                    "ks_d_python": float(py_ks["statistic"]),
                    "ks_d_java": float(jv_ks["statistic"]),
                    "ks_p_python": float(py_ks["p_value"]),
                    "ks_p_java": float(jv_ks["p_value"]),
                    "states_equal": states_equal,
                    "max_uniform_diff": max_uniform_diff,
                }
            )

        if not rows:
            raise RuntimeError("No hay resultados comparables para los tamanos configurados.")

        frame = pd.DataFrame(rows)
        frame["chi2_p_diff"] = (frame["chi2_p_python"] - frame["chi2_p_java"]).abs()
        frame["ks_p_diff"] = (frame["ks_p_python"] - frame["ks_p_java"]).abs()
        frame["chi2_stat_diff"] = (
            frame["chi2_stat_python"] - frame["chi2_stat_java"]
        ).abs()
        frame["ks_d_diff"] = (frame["ks_d_python"] - frame["ks_d_java"]).abs()
        return frame

    def export(self, frame: pd.DataFrame) -> None:
        directory = self._config.comparison_dir
        directory.mkdir(parents=True, exist_ok=True)
        frame.to_csv(directory / "comparison.csv", index=False)

        table = pd.DataFrame(
            {
                "N": frame["N"],
                "pi_estimado": frame["pi_python"],
                "error": frame["error_python"],
                "tiempo_python_s": frame["time_python_s"],
                "tiempo_java_s": frame["time_java_s"],
            }
        )
        table.to_csv(directory / "pi_table.csv", index=False)

    @staticmethod
    def print_table(frame: pd.DataFrame) -> None:
        table = pd.DataFrame(
            {
                "N": frame["N"],
                "pi_estimado": frame["pi_python"],
                "error": frame["error_python"],
                "tiempo_python_s": frame["time_python_s"],
                "tiempo_java_s": frame["time_java_s"],
            }
        )
        print("\nTabla comparativa Python-Java")
        print(table.to_string(index=False, float_format=lambda value: f"{value:.10f}"))
        print("\nVerificacion de equivalencia")
        for _, row in frame.iterrows():
            print(
                f"N={int(row['N'])}: estados iguales={bool(row['states_equal'])}, "
                f"max|U_py-U_java|={row['max_uniform_diff']:.3e}, "
                f"|p_chi_py-p_chi_java|={row['chi2_p_diff']:.3e}, "
                f"|p_ks_py-p_ks_java|={row['ks_p_diff']:.3e}"
            )

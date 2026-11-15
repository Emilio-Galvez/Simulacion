"""Graficas de resultados con Matplotlib."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import SimulationConfig


def _load_uniforms(config: SimulationConfig, n: int) -> np.ndarray:
    path = config.python_results_dir / "sequences" / f"sequence_{n}.csv"
    if not path.exists():
        raise FileNotFoundError(f"No existe la secuencia {path}.")
    return pd.read_csv(path, usecols=["uniform"], dtype={"uniform": "float64"})[
        "uniform"
    ].to_numpy()


def plot_histogram(uniforms: np.ndarray, n: int, bins: int, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    counts, edges, _ = ax.hist(
        uniforms,
        bins=np.linspace(0.0, 1.0, bins + 1),
        edgecolor="black",
        alpha=0.75,
        label="Frecuencia observada",
    )
    expected = n / bins
    centers = (edges[:-1] + edges[1:]) / 2.0
    ax.step(
        edges,
        np.append(counts, counts[-1]),
        where="post",
        color="tab:red",
        linewidth=1.2,
        label="Frecuencia esperada por intervalo",
    )
    ax.axhline(expected, color="tab:red", linestyle="--", linewidth=1.2)
    ax.set_title(f"Histograma de frecuencias de numeros pseudoaleatorios (N={n:,})")
    ax.set_xlabel("Intervalo")
    ax.set_ylabel("Frecuencia")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def plot_ecdf(uniforms: np.ndarray, n: int, output: Path) -> None:
    ordered = np.sort(uniforms)
    if n > 100_000:
        positions = np.linspace(0, n - 1, 100_000, dtype=np.int64)
        x_values = ordered[positions]
        y_values = (positions + 1) / n
    else:
        x_values = ordered
        y_values = np.arange(1, n + 1) / n

    theoretical = np.linspace(0.0, 1.0, 500)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        x_values,
        y_values,
        drawstyle="steps-post",
        linewidth=1.2,
        label="Distribucion empirica Fn(x)",
    )
    ax.plot(
        theoretical,
        theoretical,
        linestyle="--",
        linewidth=1.5,
        color="tab:red",
        label="Distribucion teorica F(x)=x",
    )
    ax.set_title(f"Distribucion acumulada empirica vs. teorica (N={n:,})")
    ax.set_xlabel("x")
    ax.set_ylabel("F(x)")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def plot_times(frame: pd.DataFrame, output: Path) -> None:
    labels = [f"{int(value):,}" for value in frame["N"]]
    positions = np.arange(len(labels))
    width = 0.36

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(
        positions - width / 2,
        frame["time_python_s"],
        width,
        label="Python",
        color="tab:blue",
    )
    ax.bar(
        positions + width / 2,
        frame["time_java_s"],
        width,
        label="Java",
        color="tab:orange",
    )
    ax.set_yscale("log")
    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.set_title("Comparacion de tiempos de ejecucion Python vs. Java")
    ax.set_xlabel("Cantidad de numeros N")
    ax.set_ylabel("Tiempo total (s, escala logaritmica)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def plot_pi_error(frame: pd.DataFrame, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(
        frame["N"],
        frame["error_python"],
        marker="o",
        linewidth=1.8,
        label="Python",
    )
    ax.plot(
        frame["N"],
        frame["error_java"],
        marker="s",
        linewidth=1.2,
        linestyle="--",
        label="Java",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Error absoluto de la estimacion de pi")
    ax.set_xlabel("Cantidad de numeros N")
    ax.set_ylabel("Error absoluto |pi_real - pi_estimado|")
    ax.legend()
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def generate_all_plots(
    config: SimulationConfig,
    frame: pd.DataFrame,
    sizes: tuple[int, ...] | None = None,
) -> list[Path]:
    """Genera todas las graficas y devuelve sus rutas."""

    output_dir = config.plots_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    selected_sizes = sizes if sizes is not None else config.sample_sizes
    paths: list[Path] = []

    for n in selected_sizes:
        uniforms = _load_uniforms(config, n)
        histogram_path = output_dir / f"histograma_{n}.png"
        ecdf_path = output_dir / f"ecdf_{n}.png"
        plot_histogram(uniforms, n, config.bins, histogram_path)
        plot_ecdf(uniforms, n, ecdf_path)
        paths.extend([histogram_path, ecdf_path])

    times_path = output_dir / "comparacion_tiempos.png"
    pi_error_path = output_dir / "error_pi.png"
    plot_times(frame, times_path)
    plot_pi_error(frame, pi_error_path)
    paths.extend([times_path, pi_error_path])
    return paths

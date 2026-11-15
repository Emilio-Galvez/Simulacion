"""Graficas de resultados con Matplotlib."""

from __future__ import annotations

import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import SimulationConfig


def plot_error(frame: pd.DataFrame, output: Path) -> None:
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
        linewidth=1.4,
        linestyle="--",
        label="Java",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Error absoluto de la estimacion de pi")
    ax.set_xlabel("Cantidad de puntos N")
    ax.set_ylabel("Error absoluto |pi_real - pi_estimado|")
    ax.legend()
    ax.grid(alpha=0.3, which="both")
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
        frame["tiempo_python_s"],
        width,
        label="Python",
        color="tab:blue",
    )
    ax.bar(
        positions + width / 2,
        frame["tiempo_java_s"],
        width,
        label="Java",
        color="tab:orange",
    )
    ax.set_yscale("log")
    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.set_title("Tiempo de ejecucion del experimento Monte Carlo")
    ax.set_xlabel("Cantidad de puntos N")
    ax.set_ylabel("Tiempo mediano (s, escala logaritmica)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def plot_points(seed: int, n: int, output: Path) -> None:
    rng = random.Random(seed)
    inside_x: list[float] = []
    inside_y: list[float] = []
    outside_x: list[float] = []
    outside_y: list[float] = []
    inside = 0

    for _ in range(n):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1.0:
            inside += 1
            inside_x.append(x)
            inside_y.append(y)
        else:
            outside_x.append(x)
            outside_y.append(y)

    estimate = 4.0 * inside / n
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(inside_x, inside_y, s=6, color="tab:green", label="Dentro del circulo")
    ax.scatter(outside_x, outside_y, s=6, color="tab:red", label="Fuera del circulo")
    circle = plt.Circle((0.0, 0.0), 1.0, fill=False, color="black", linewidth=1.5)
    ax.add_patch(circle)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_aspect("equal")
    ax.set_title(f"Monte Carlo con N={n:,}; pi estimado={estimate:.6f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def generate_all_plots(config: SimulationConfig, frame: pd.DataFrame) -> list[Path]:
    """Genera las graficas del informe y devuelve sus rutas."""

    output_dir = config.plots_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    error_path = output_dir / "error_vs_n.png"
    times_path = output_dir / "tiempos_vs_n.png"
    points_path = output_dir / "monte_carlo_1000.png"

    plot_error(frame, error_path)
    plot_times(frame, times_path)
    plot_points(config.seed, 1000, points_path)
    return [error_path, times_path, points_path]

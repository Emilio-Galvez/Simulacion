"""Punto de entrada de la implementacion Python de la Practica 6."""

from __future__ import annotations

import argparse
from pathlib import Path

from config import SimulationConfig, load_config
from models.results import SimulationResult
from services.comparison_service import ComparisonService
from services.export_service import ExportService
from services.simulation_service import SimulationService
from visualization.plots import generate_all_plots


def _parse_sizes(raw: str | None, config: SimulationConfig) -> tuple[int, ...]:
    if raw is None:
        return config.sample_sizes
    sizes = tuple(int(item.strip()) for item in raw.split(",") if item.strip())
    if not sizes or any(size <= 0 for size in sizes):
        raise argparse.ArgumentTypeError("Los tamanos deben ser enteros positivos.")
    return sizes


def _print_python_results(results: list[SimulationResult]) -> None:
    print("\nResultados Python")
    print(
        f"{'N':>10} {'pi estimado':>16} {'error':>14} {'tiempo (s)':>14} "
        f"{'p Chi2':>12} {'p KS':>12}"
    )
    for result in results:
        print(
            f"{result.n:>10,} {result.pi_estimate:>16.12f} {result.pi_error:>14.6e} "
            f"{result.timings.total_ns / 1_000_000_000:>14.6f} "
            f"{result.chi_square.p_value:>12.6f} {result.kolmogorov_smirnov.p_value:>12.6f}"
        )


def _run_comparison(config: SimulationConfig, with_plots: bool) -> None:
    comparison = ComparisonService(config)
    try:
        frame = comparison.build()
    except FileNotFoundError as exc:
        print(f"\nNo se puede comparar todavia: {exc}")
        return

    comparison.export(frame)
    comparison.print_table(frame)
    print(f"\nComparacion exportada en: {config.comparison_dir}")

    if with_plots:
        try:
            paths = generate_all_plots(config, frame)
        except ImportError as exc:
            print(f"No se generaron las graficas: {exc}")
            return
        print("\nGraficas generadas:")
        for path in paths:
            print(f"  {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Practica 6 - Simulacion")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument(
        "--sizes",
        type=str,
        default=None,
        help="Lista de tamanos separados por coma, por ejemplo: 1000,10000",
    )
    parser.add_argument("--compare-only", action="store_true")
    parser.add_argument("--no-compare", action="store_true")
    parser.add_argument("--no-plots", action="store_true")
    parser.add_argument("--no-warmup", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    sizes = _parse_sizes(args.sizes, config)

    if not args.compare_only:
        service = SimulationService(config)
        if not args.no_warmup:
            service.warm_up()
        results = service.run_all(sizes)
        ExportService(config.python_results_dir).export_all(results)
        _print_python_results(results)
        print(f"\nResultados Python exportados en: {config.python_results_dir}")

    if not args.no_compare:
        _run_comparison(config, with_plots=not args.no_plots)


if __name__ == "__main__":
    main()

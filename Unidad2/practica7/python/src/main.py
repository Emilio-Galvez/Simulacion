"""Punto de entrada de la implementacion Python de la Practica 7."""

from __future__ import annotations

import argparse
from pathlib import Path

from config import SimulationConfig, load_config
from models.results import Summary
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


def _print_python_results(summaries: list[Summary]) -> None:
    print("\nResultados Python")
    print(
        f"{'N':>10} {'dentro':>12} {'pi estimado':>16} {'error':>14} "
        f"{'tiempo mediano (s)':>20}"
    )
    for summary in summaries:
        print(
            f"{summary.n:>10,} {summary.inside:>12,} "
            f"{summary.pi_estimate:>16.12f} {summary.error:>14.6e} "
            f"{summary.median_time_s:>20.6f}"
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
    parser = argparse.ArgumentParser(description="Practica 7 - Monte Carlo")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument(
        "--sizes",
        type=str,
        default=None,
        help="Lista de tamanos separados por coma, por ejemplo: 1000,10000",
    )
    parser.add_argument(
        "--repetitions",
        type=int,
        default=None,
        help="Numero de repeticiones para el tiempo mediano",
    )
    parser.add_argument("--compare-only", action="store_true")
    parser.add_argument("--no-compare", action="store_true")
    parser.add_argument("--no-plots", action="store_true")
    parser.add_argument("--no-warmup", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    sizes = _parse_sizes(args.sizes, config)

    if args.repetitions is not None:
        if args.repetitions <= 0:
            raise SystemExit("El numero de repeticiones debe ser positivo.")
        config = config.__class__(
            seed=config.seed,
            sample_sizes=config.sample_sizes,
            repetitions=args.repetitions,
            warmup_size=config.warmup_size,
            real_pi=config.real_pi,
            project_root=config.project_root,
            config_path=config.config_path,
        )

    if not args.compare_only:
        service = SimulationService(config)
        if not args.no_warmup:
            service.warm_up()
        summaries = service.run_all(sizes)
        ExportService(config.python_results_dir).export_all(summaries)
        _print_python_results(summaries)
        print(f"\nResultados Python exportados en: {config.python_results_dir}")

    if not args.no_compare:
        _run_comparison(config, with_plots=not args.no_plots)


if __name__ == "__main__":
    main()

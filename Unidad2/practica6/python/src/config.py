"""Configuracion compartida de la Practica 6."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "simulation.properties"


class ConfigError(ValueError):
    """Error de configuracion."""


def _read_properties(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


@dataclass(frozen=True)
class SimulationConfig:
    """Parametros del LCG, de las pruebas y de la experimentacion."""

    seed: int
    multiplier: int
    increment: int
    modulus: int
    alpha: float
    bins: int
    sample_sizes: tuple[int, ...]
    project_root: Path
    config_path: Path

    @property
    def python_results_dir(self) -> Path:
        return self.project_root / "python" / "results"

    @property
    def java_results_dir(self) -> Path:
        return self.project_root / "java" / "results"

    @property
    def comparison_dir(self) -> Path:
        return self.project_root / "results" / "comparison"

    @property
    def plots_dir(self) -> Path:
        return self.project_root / "results" / "plots"

    def validate(self) -> None:
        if self.modulus <= 1:
            raise ConfigError("El modulo debe ser mayor que 1.")
        if not 0 <= self.seed < self.modulus:
            raise ConfigError("La semilla debe cumplir 0 <= semilla < modulo.")
        if not 0 < self.multiplier < self.modulus:
            raise ConfigError("El multiplicador debe cumplir 0 < a < modulo.")
        if not 0 <= self.increment < self.modulus:
            raise ConfigError("El incremento debe cumplir 0 <= c < modulo.")
        if not 0.0 < self.alpha < 1.0:
            raise ConfigError("El nivel de significancia debe estar en (0, 1).")
        if self.bins <= 1:
            raise ConfigError("El numero de intervalos debe ser mayor que 1.")
        if not self.sample_sizes or any(n <= 0 for n in self.sample_sizes):
            raise ConfigError("Los tamanos de muestra deben ser enteros positivos.")


def load_config(path: str | Path | None = None) -> SimulationConfig:
    """Carga y valida el archivo de propiedades compartido."""

    config_path = Path(path).resolve() if path is not None else DEFAULT_CONFIG_PATH
    if not config_path.exists():
        raise ConfigError(f"No existe el archivo de configuracion: {config_path}")

    values = _read_properties(config_path)
    try:
        sample_sizes = tuple(
            int(item.strip()) for item in values["sample.sizes"].split(",") if item.strip()
        )
        config = SimulationConfig(
            seed=int(values["seed"]),
            multiplier=int(values["multiplier"]),
            increment=int(values["increment"]),
            modulus=int(values["modulus"]),
            alpha=float(values["alpha"]),
            bins=int(values["bins"]),
            sample_sizes=sample_sizes,
            project_root=config_path.parent.parent,
            config_path=config_path,
        )
    except KeyError as exc:
        raise ConfigError(f"Falta la propiedad {exc.args[0]!r} en {config_path}") from exc
    except ValueError as exc:
        raise ConfigError(f"Valor invalido en {config_path}: {exc}") from exc

    config.validate()
    return config

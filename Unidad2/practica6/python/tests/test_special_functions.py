import math

import pytest

from statistics.special_functions import (
    chi_square_survival,
    kolmogorov_survival,
    log_gamma,
)


def test_log_gamma_valores_conocidos() -> None:
    assert log_gamma(1.0) == pytest.approx(0.0, abs=1e-12)
    assert log_gamma(5.0) == pytest.approx(math.log(24.0), abs=1e-12)
    assert log_gamma(0.5) == pytest.approx(math.log(math.sqrt(math.pi)), abs=1e-12)


def test_chi_cuadrado_valor_critico() -> None:
    assert chi_square_survival(16.919, 9) == pytest.approx(0.05, abs=1e-4)
    assert chi_square_survival(0.0, 9) == 1.0


def test_kolmogorov_valor_critico() -> None:
    assert kolmogorov_survival(1.36) == pytest.approx(0.05, abs=0.005)
    assert kolmogorov_survival(0.0) == 1.0

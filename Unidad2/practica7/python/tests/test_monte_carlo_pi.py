import math

import pytest

from simulation.monte_carlo_pi import MonteCarloPi


def test_estimacion_es_cuatro_veces_la_proporcion() -> None:
    result = MonteCarloPi(seed=12345).run_once(1000)
    assert result.pi_estimate == pytest.approx(4.0 * result.inside / result.n)


def test_error_absoluto() -> None:
    result = MonteCarloPi(seed=12345).run_once(1000)
    assert result.error == pytest.approx(abs(math.pi - result.pi_estimate))


def test_misma_semilla_produce_misma_estimacion() -> None:
    first = MonteCarloPi(seed=2026).run_once(10_000)
    second = MonteCarloPi(seed=2026).run_once(10_000)
    assert first.pi_estimate == second.pi_estimate
    assert first.inside == second.inside


def test_estimacion_en_rango_razonable() -> None:
    result = MonteCarloPi(seed=12345).run_once(10_000)
    assert 3.0 < result.pi_estimate < 3.3


def test_puntos_invalidos() -> None:
    with pytest.raises(ValueError):
        MonteCarloPi(seed=12345).run_once(0)


def test_repeticiones_invalidas() -> None:
    with pytest.raises(ValueError):
        MonteCarloPi(seed=12345).run(1000, 0)

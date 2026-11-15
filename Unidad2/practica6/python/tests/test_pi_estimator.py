import pytest

from simulation.pi_estimator import PiEstimator


def test_error_absoluto() -> None:
    assert PiEstimator.absolute_error(3.0) == pytest.approx(0.141592653589793, abs=1e-15)


def test_serie_de_leibniz_converge_lentamente() -> None:
    estimate = PiEstimator.estimate(1_000_000)
    assert PiEstimator.absolute_error(estimate) < 1e-5


def test_estimacion_en_rango() -> None:
    estimate = PiEstimator.estimate(1_000)
    assert 3.14 < estimate < 3.142


def test_terminos_invalidos() -> None:
    with pytest.raises(ValueError):
        PiEstimator.estimate(0)

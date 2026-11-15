import pytest

from generators.lcg import LCG
from statistics.chi_square import ChiSquareTest


def test_muestra_perfectamente_uniforme() -> None:
    n = 10_000
    sample = [index / n for index in range(n)]
    result = ChiSquareTest(10).run(sample, 0.05)

    assert result.details["degrees_of_freedom"] == 9
    assert result.details["observed"] == [n // 10] * 10
    assert result.statistic == pytest.approx(0.0, abs=1e-12)
    assert result.p_value == pytest.approx(1.0, abs=1e-12)
    assert not result.reject_null


def test_muestra_constante_rechaza_uniformidad() -> None:
    result = ChiSquareTest(10).run([0.05] * 10_000, 0.05)
    assert result.statistic > 1000
    assert result.p_value < 0.05
    assert result.reject_null


def test_frecuencias_suman_el_total_y_grados_de_libertad() -> None:
    lcg = LCG(12345, 1664525, 1013904223, 4294967296)
    sample = lcg.generate(10_000).uniforms
    result = ChiSquareTest(10).run(sample, 0.05)

    observed = result.details["observed"]
    expected = result.details["expected"]
    assert sum(observed) == 10_000
    assert len(observed) == len(expected) == 10
    assert result.details["degrees_of_freedom"] == 9
    assert 0.0 <= result.p_value <= 1.0


def test_valores_esperados() -> None:
    result = ChiSquareTest(10).run([0.05] * 100, 0.05)
    assert result.details["expected"] == [10.0] * 10

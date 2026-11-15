import pytest

from generators.lcg import LCG
from statistics.kolmogorov_smirnov import KolmogorovSmirnovTest


def test_muestra_en_rejilla_uniforme() -> None:
    n = 10_000
    sample = [index / n for index in range(n)]
    result = KolmogorovSmirnovTest().run(sample, 0.05)

    assert result.statistic == pytest.approx(1.0 / n, abs=1e-12)
    assert result.details["d_minus"] == pytest.approx(0.0, abs=1e-12)
    assert result.p_value > 0.05
    assert not result.reject_null


def test_muestra_constante_rechaza_uniformidad() -> None:
    result = KolmogorovSmirnovTest().run([0.5] * 1_000, 0.05)
    assert result.statistic == pytest.approx(0.5, abs=1e-3)
    assert result.p_value < 0.05
    assert result.reject_null


def test_estadistico_es_el_maximo_de_las_diferencias() -> None:
    lcg = LCG(12345, 1664525, 1013904223, 4294967296)
    sample = lcg.generate(1_000).uniforms
    result = KolmogorovSmirnovTest().run(sample, 0.05)
    d_plus = result.details["d_plus"]
    d_minus = result.details["d_minus"]
    assert d_plus >= 0.0
    assert d_minus >= 0.0
    assert result.statistic == pytest.approx(max(d_plus, d_minus), abs=1e-15)
    assert 0.0 <= result.p_value <= 1.0


def test_muestra_vacia() -> None:
    with pytest.raises(ValueError):
        KolmogorovSmirnovTest().run([], 0.05)

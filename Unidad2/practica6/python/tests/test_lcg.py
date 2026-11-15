import pytest

from generators.lcg import LCG, LCGError

EXPECTED_STATES = [
    87628868,
    71072467,
    2332836374,
    2726892157,
    3908547000,
    483019191,
    2129828778,
    2355140353,
    2560230508,
    3364893915,
]


def make_lcg() -> LCG:
    return LCG(
        seed=12345,
        multiplier=1664525,
        increment=1013904223,
        modulus=4294967296,
    )


def test_primeros_estados_conocidos() -> None:
    result = make_lcg().generate(10)
    assert result.states == EXPECTED_STATES


def test_valores_en_intervalo_unitario() -> None:
    result = make_lcg().generate(10_000)
    assert len(result.uniforms) == 10_000
    assert all(0.0 <= value < 1.0 for value in result.uniforms)
    assert all(value == state / 4294967296 for state, value in zip(result.states, result.uniforms))


def test_reproducibilidad() -> None:
    first = make_lcg().generate(1_000)
    second = make_lcg().generate(1_000)
    assert first.states == second.states
    assert first.uniforms == second.uniforms


def test_el_generador_avanza_su_estado() -> None:
    lcg = make_lcg()
    assert lcg.state == 12345
    lcg.next_state()
    assert lcg.state == EXPECTED_STATES[0]


@pytest.mark.parametrize(
    "seed,multiplier,increment,modulus",
    [
        (-1, 1664525, 1013904223, 4294967296),
        (12345, 0, 1013904223, 4294967296),
        (12345, 1664525, -1, 4294967296),
        (12345, 1664525, 1013904223, 1),
        (4294967296, 1664525, 1013904223, 4294967296),
    ],
)
def test_parametros_invalidos(seed: int, multiplier: int, increment: int, modulus: int) -> None:
    with pytest.raises(LCGError):
        LCG(seed, multiplier, increment, modulus)


def test_cantidad_negativa() -> None:
    with pytest.raises(LCGError):
        make_lcg().generate(-1)

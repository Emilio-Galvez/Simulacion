import csv
from pathlib import Path

import pytest

from generators.lcg import LCG

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

JAVA_SEQUENCE = (
    Path(__file__).resolve().parents[2]
    / "java"
    / "results"
    / "sequences"
    / "sequence_1000.csv"
)


def python_states(count: int) -> list[int]:
    lcg = LCG(12345, 1664525, 1013904223, 4294967296)
    return lcg.generate(count).states


def test_primeros_estados_coinciden_con_la_referencia() -> None:
    assert python_states(10) == EXPECTED_STATES


@pytest.mark.skipif(not JAVA_SEQUENCE.exists(), reason="Ejecute primero la implementacion Java")
def test_secuencia_python_y_java_son_identicas() -> None:
    java_states: list[int] = []
    with JAVA_SEQUENCE.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            java_states.append(int(row["state"]))
    assert python_states(len(java_states)) == java_states

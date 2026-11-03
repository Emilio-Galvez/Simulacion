"""Prueba de integracion: el CSV de Python debe coincidir con el de Java.

La prueba se omite (skip) cuando todavia no existe el archivo generado por
Java. Tras ejecutar ambos programas, el comando siguiente verifica la
identidad completa de las dos secuencias:

    cd Practica\\ 5/Python
    python -m pytest pruebas/test_integracion_java.py -v
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

from datos.exportador_csv import ExportadorCSV
from datos.rutas import directorio_resultados, encontrar_raiz_proyecto
from servicios.comparador import Comparador

RAIZ = encontrar_raiz_proyecto()
DIRECTORIO_RESULTADOS = directorio_resultados(RAIZ)
RUTA_PYTHON = os.path.join(DIRECTORIO_RESULTADOS, "resultados_python.csv")
RUTA_JAVA = os.path.join(DIRECTORIO_RESULTADOS, "resultados_java.csv")


@pytest.mark.skipif(
    not os.path.isfile(RUTA_JAVA),
    reason="No existe resultados_java.csv: ejecuta primero la simulacion en Java.",
)
class TestIntegracionPythonJava:
    """Verifica que Python y Java produzcan exactamente la misma secuencia."""

    def test_los_archivos_csv_existen(self):
        assert os.path.isfile(RUTA_PYTHON)
        assert os.path.isfile(RUTA_JAVA)

    def test_las_secuencias_completas_son_identicas(self):
        estados_python = ExportadorCSV.leer_estados(RUTA_PYTHON)
        estados_java = ExportadorCSV.leer_estados(RUTA_JAVA)
        assert len(estados_python) == 10000
        assert len(estados_java) == 10000
        resultado = Comparador.comparar_secuencias(estados_python, estados_java)
        assert resultado.identicas, resultado.mensaje

    def test_las_primeras_20_observaciones_coinciden(self):
        filas_python = ExportadorCSV.leer_resultados(RUTA_PYTHON)[:20]
        filas_java = ExportadorCSV.leer_resultados(RUTA_JAVA)[:20]
        for fila_python, fila_java in zip(filas_python, filas_java, strict=False):
            assert fila_python["x"] == fila_java["x"]
            assert fila_python["normalizado"] == fila_java["normalizado"]

    def test_los_archivos_csv_son_identicos_byte_a_byte(self):
        with open(RUTA_PYTHON, "rb") as archivo_python, open(RUTA_JAVA, "rb") as archivo_java:
            assert archivo_python.read() == archivo_java.read()


def test_el_programa_python_ejecuta_el_flujo_automatico(tmp_path):
    """El flujo automatico debe generar el CSV de resultados de Python."""
    raiz_python = os.path.join(RAIZ, "Python")
    proceso = subprocess.run(
        [
            sys.executable,
            "main.py",
            "--automatica",
            "--sin-graficas",
            "--salida",
            str(tmp_path),
        ],
        cwd=raiz_python,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proceso.returncode == 0, proceso.stderr
    assert os.path.isfile(tmp_path / "resultados_python.csv")
    estados = ExportadorCSV.leer_estados(str(tmp_path / "resultados_python.csv"))
    assert len(estados) == 10000

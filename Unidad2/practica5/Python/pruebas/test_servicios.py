"""Pruebas de los servicios de analisis, comparacion y de la capa de datos."""

from __future__ import annotations

import os
from decimal import Decimal

from datos.exportador_csv import ExportadorCSV, formatear_normalizado_exacto
from generador_lcg import ServicioLCG
from servicios.analisis import Analisis
from servicios.comparador import Comparador

CANTIDAD_ESPERADA = 10000
MODULO = 2**32


class TestAnalisisDelPeriodo:
    """Verifica el analisis del periodo y las condiciones de Hull-Dobell."""

    def test_los_parametros_cumplen_hull_dobell(self):
        verificacion = Analisis.verificar_hull_dobell(1664525, 1013904223, MODULO)
        assert verificacion.cumple_periodo_completo
        assert verificacion.periodo_teorico == MODULO

    def test_se_verifican_las_tres_condiciones(self):
        verificacion = Analisis.verificar_hull_dobell(1664525, 1013904223, MODULO)
        assert len(verificacion.condiciones) == 3
        assert all(condicion.cumple for condicion in verificacion.condiciones)

    def test_un_incremento_par_no_alcanza_el_periodo_completo(self):
        verificacion = Analisis.verificar_hull_dobell(1664525, 1013904222, MODULO)
        assert not verificacion.cumple_periodo_completo
        assert verificacion.periodo_teorico == 0

    def test_los_factores_primos_de_2_32_son_correctos(self):
        assert Analisis.factores_primos(MODULO) == [2]

    def test_el_periodo_empirico_no_se_detecta_en_10000_muestras(self):
        generador = ServicioLCG().crear_generador()
        assert Analisis.periodo_empirico(generador, limite=CANTIDAD_ESPERADA) is None


class TestAnalisisEstadistico:
    """Verifica las estadisticas y la prueba de uniformidad."""

    def test_las_estadisticas_de_la_simulacion_son_razonables(self):
        resultado = ServicioLCG().simular()
        estadisticas = resultado.estadisticas
        assert estadisticas["cantidad"] == CANTIDAD_ESPERADA
        assert abs(estadisticas["media"] - 0.5) < 0.02
        assert abs(estadisticas["varianza"] - 1.0 / 12.0) < 0.01
        assert 0.0 <= estadisticas["minimo"] < estadisticas["maximo"] < 1.0

    def test_la_prueba_chi_cuadrado_no_rechaza_la_uniformidad(self):
        resultado = ServicioLCG().simular()
        prueba = Analisis.prueba_chi_cuadrado(resultado.normalizados, bins=20)
        assert prueba.grados_libertad == 19
        assert not prueba.rechaza_hipotesis
        assert sum(prueba.frecuencias_observadas) == CANTIDAD_ESPERADA


class TestComparador:
    """Verifica la comparacion entre secuencias."""

    def test_dos_secuencias_identicas_son_reportadas_como_identicas(self):
        estados = ServicioLCG().simular().estados
        resultado = Comparador.comparar_secuencias(estados, list(estados))
        assert resultado.identicas
        assert resultado.total_comparadas == CANTIDAD_ESPERADA
        assert resultado.primera_diferencia is None

    def test_dos_semillas_distintas_producen_secuencias_distintas(self):
        original = ServicioLCG().simular(12345).estados
        alternativa = ServicioLCG().simular(54321).estados
        resultado = Comparador.comparar_semillas(original, alternativa)
        assert not resultado.identicas
        assert resultado.primera_diferencia is not None
        assert resultado.primera_diferencia.indice == 0

    def test_la_tabla_comparativa_incluye_las_primeras_20_observaciones(self):
        estados = ServicioLCG().simular().estados
        tabla = Comparador.tabla_primeras_observaciones(estados, list(estados), MODULO, 20)
        assert len(tabla) == 20
        assert all(fila["coincide"] for fila in tabla)


class TestCapaDeDatos:
    """Verifica la exportacion y lectura de archivos CSV."""

    def test_el_formato_normalizado_es_exacto_y_truncado(self):
        texto = formatear_normalizado_exacto(87628868, MODULO)
        esperado = Decimal(87628868) / Decimal(MODULO)
        assert texto == f"{esperado:.12f}"
        assert Decimal(texto) <= esperado

    def test_el_formato_normalizado_coincide_con_otros_lenguajes(self):
        assert formatear_normalizado_exacto(2097152, MODULO) == "0.000488281250"
        assert formatear_normalizado_exacto(0, MODULO) == "0.000000000000"
        assert formatear_normalizado_exacto(MODULO - 1, MODULO) == "0.999999999767"

    def test_el_csv_se_genera_correctamente(self, tmp_path):
        estados = ServicioLCG().simular().estados
        ruta = str(tmp_path / "resultados.csv")
        ExportadorCSV.exportar_resultados(ruta, estados, MODULO)
        assert os.path.isfile(ruta)
        with open(ruta, encoding="utf-8") as archivo:
            lineas = archivo.read().strip().split("\n")
        assert lineas[0] == "indice,x,normalizado"
        assert len(lineas) == CANTIDAD_ESPERADA + 1
        assert lineas[1] == f"1,{estados[0]},{formatear_normalizado_exacto(estados[0], MODULO)}"

    def test_el_csv_se_puede_leer_desde_disco(self, tmp_path):
        estados = ServicioLCG().simular().estados
        ruta = str(tmp_path / "resultados.csv")
        ExportadorCSV.exportar_resultados(ruta, estados, MODULO)
        assert ExportadorCSV.leer_estados(ruta) == estados

    def test_el_csv_de_comparacion_se_genera_correctamente(self, tmp_path):
        estados = ServicioLCG().simular().estados
        filas = Comparador.tabla_primeras_observaciones(estados, list(estados), MODULO, 20)
        ruta = str(tmp_path / "comparacion.csv")
        ExportadorCSV.exportar_comparacion(ruta, filas)
        with open(ruta, encoding="utf-8") as archivo:
            lineas = archivo.read().strip().split("\n")
        assert lineas[0] == "indice,x_python,x_java,u_python,u_java,coincide"
        assert len(lineas) == 21
        assert lineas[1].endswith(",si")

    def test_comparar_archivos_csv_detecta_identidad(self, tmp_path):
        estados = ServicioLCG().simular().estados
        ruta_1 = str(tmp_path / "resultados_1.csv")
        ruta_2 = str(tmp_path / "resultados_2.csv")
        ExportadorCSV.exportar_resultados(ruta_1, estados, MODULO)
        ExportadorCSV.exportar_resultados(ruta_2, estados, MODULO)
        assert Comparador.comparar_archivos_csv(ruta_1, ruta_2).identicas

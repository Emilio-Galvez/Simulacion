"""Pruebas de la estrategia LCG, la fabrica y el servicio de dominio."""

from __future__ import annotations

import pytest

from datos.configuracion import Configuracion
from estrategias.estrategia_lcg import EstrategiaLCG
from estrategias.interfaz_generador import Generador, ParametrosInvalidosError
from fabricas.fabrica_generador import FabricaGenerador, TipoGeneradorDesconocidoError
from generador_lcg import ServicioLCG

CANTIDAD_ESPERADA = 10000
PRIMEROS_ESTADOS_ESPERADOS = [87628868, 71072467, 2332836374, 2726892157, 3908547000]


class TestValidacionDeParametros:
    """Verifica la validacion de los parametros matematicos."""

    def test_parametros_por_defecto_son_validos(self):
        generador = EstrategiaLCG()
        assert generador.multiplicador == 1664525
        assert generador.incremento == 1013904223
        assert generador.modulo == 2**32
        assert generador.semilla == 12345

    def test_multiplicador_no_positivo_es_invalido(self):
        with pytest.raises(ParametrosInvalidosError):
            EstrategiaLCG(multiplicador=0)

    def test_modulo_invalido_es_rechazado(self):
        with pytest.raises(ParametrosInvalidosError):
            EstrategiaLCG(modulo=1)

    def test_incremento_fuera_de_rango_es_rechazado(self):
        with pytest.raises(ParametrosInvalidosError):
            EstrategiaLCG(incremento=2**32)

    def test_semilla_fuera_de_rango_es_rechazada(self):
        with pytest.raises(ParametrosInvalidosError):
            EstrategiaLCG(semilla=2**32)

    def test_cantidad_negativa_es_rechazada(self):
        with pytest.raises(ParametrosInvalidosError):
            EstrategiaLCG().generar(-1)

    def test_configuracion_invalida_es_rechazada(self):
        with pytest.raises(ParametrosInvalidosError):
            Configuracion(semilla=-1).validar()


class TestGeneracion:
    """Verifica la generacion de la secuencia pseudoaleatoria."""

    def test_se_generan_exactamente_10000_valores(self):
        generador = EstrategiaLCG()
        assert len(generador.generar(CANTIDAD_ESPERADA)) == CANTIDAD_ESPERADA

    def test_primeros_estados_coinciden_con_el_referencia_calculada(self):
        generador = EstrategiaLCG()
        estados = generador.generar(5)
        assert estados == PRIMEROS_ESTADOS_ESPERADOS

    def test_todos_los_valores_normalizados_estan_en_el_intervalo_unitario(self):
        generador = EstrategiaLCG()
        normalizados = generador.generar_normalizados(CANTIDAD_ESPERADA)
        assert len(normalizados) == CANTIDAD_ESPERADA
        assert all(0.0 <= valor < 1.0 for valor in normalizados)

    def test_normalizacion_usa_la_relacion_indicada(self):
        generador = EstrategiaLCG()
        estados = generador.generar(10)
        for estado, normalizado in zip(estados, generador.generar_normalizados(10), strict=True):
            assert normalizado == estado / generador.modulo

    def test_estados_se_mantienen_en_el_rango_del_modulo(self):
        generador = EstrategiaLCG()
        assert all(0 <= estado < generador.modulo for estado in generador.generar(1000))

    def test_generacion_es_determinista(self):
        primera = EstrategiaLCG().generar(100)
        segunda = EstrategiaLCG().generar(100)
        assert primera == segunda

    def test_cambiar_la_semilla_produce_una_secuencia_distinta(self):
        original = EstrategiaLCG(semilla=12345).generar(CANTIDAD_ESPERADA)
        alternativa = EstrategiaLCG(semilla=54321).generar(CANTIDAD_ESPERADA)
        assert original != alternativa
        assert original[0] != alternativa[0]

    def test_el_servicio_de_dominio_reutiliza_los_parametros_configurados(self):
        servicio = ServicioLCG(Configuracion.por_defecto())
        resultado = servicio.simular()
        assert resultado.cantidad == CANTIDAD_ESPERADA
        assert resultado.semilla == 12345
        assert len(resultado.normalizados) == CANTIDAD_ESPERADA


class TestFabricaGenerador:
    """Verifica el patron Factory Method."""

    def test_la_fabrica_crea_un_generador_lcg(self):
        generador = FabricaGenerador.crear("LCG")
        assert isinstance(generador, EstrategiaLCG)
        assert isinstance(generador, Generador)

    def test_el_tipo_es_indiferente_a_mayusculas(self):
        assert isinstance(FabricaGenerador.crear("lCg"), EstrategiaLCG)

    def test_la_fabrica_aplica_los_parametros_recibidos(self):
        generador = FabricaGenerador.crear(
            "LCG", multiplicador=1664525, incremento=1013904223, modulo=2**32, semilla=777
        )
        assert generador.semilla == 777
        assert generador.modulo == 2**32

    def test_un_tipo_desconocido_produce_un_error_de_negocio(self):
        with pytest.raises(TipoGeneradorDesconocidoError):
            FabricaGenerador.crear("MERSENNE")

    def test_se_puede_registrar_una_nueva_estrategia(self):
        class GeneradorNulo(Generador):
            def generar(self, cantidad: int):
                return [0] * cantidad

            def normalizar(self, estado: int) -> float:
                return 0.0

            @property
            def multiplicador(self) -> int:
                return 1

            @property
            def incremento(self) -> int:
                return 0

            @property
            def modulo(self) -> int:
                return 2**32

            @property
            def semilla(self) -> int:
                return 0

        FabricaGenerador.registrar("NULO", GeneradorNulo)
        try:
            assert isinstance(FabricaGenerador.crear("NULO"), GeneradorNulo)
        finally:
            FabricaGenerador._registro.pop("NULO", None)

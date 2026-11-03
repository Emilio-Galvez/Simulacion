"""Servicios de analisis matematico y estadistico de las simulaciones.

Capa de LOGICA DE NEGOCIO: aqui viven el analisis del periodo (teorema de
Hull-Dobell), las estadisticas descriptivas y las pruebas de uniformidad.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field

from estrategias.interfaz_generador import Generador


@dataclass(frozen=True)
class CondicionHullDobell:
    """Resultado de evaluar una condicion del teorema de Hull-Dobell."""

    descripcion: str
    cumple: bool
    detalle: str = ""


@dataclass(frozen=True)
class ResultadoHullDobell:
    """Verificacion completa de las condiciones de Hull-Dobell."""

    multiplicador: int
    incremento: int
    modulo: int
    condiciones: list[CondicionHullDobell] = field(default_factory=list)
    periodo_teorico: int = 0

    @property
    def cumple_periodo_completo(self) -> bool:
        """Indica si se alcanza el periodo completo m."""
        return all(condicion.cumple for condicion in self.condiciones)

    @property
    def resumen(self) -> str:
        """Resumen legible del analisis."""
        estado = "CUMPLE" if self.cumple_periodo_completo else "NO CUMPLE"
        return f"Condiciones de Hull-Dobell: {estado} | Periodo teorico = {self.periodo_teorico:,}"


@dataclass(frozen=True)
class ResultadoChiCuadrado:
    """Resultado de la prueba de bondad de ajuste chi-cuadrado."""

    intervalo_confianza: float
    bins: int
    frecuencias_observadas: list[int]
    frecuencias_esperadas: list[float]
    estadistico: float
    valor_critico: float
    grados_libertad: int
    rechaza_hipotesis: bool


class Analisis:
    """Servicio de analisis para generadores y secuencias pseudoaleatorias."""

    VALOR_CRITICO_CHI_CUADRADO_20 = 31.410
    VALOR_CRITICO_CHI_CUADRADO_19 = 30.144
    VALOR_CRITICO_CHI_CUADRADO_10 = 18.307
    VALOR_CRITICO_CHI_CUADRADO_05 = 11.070
    VALOR_CRITICO_CHI_CUADRADO_01 = 7.779

    @staticmethod
    def factores_primos(n: int) -> list[int]:
        """Devuelve los factores primos distintos de n."""
        if n < 2:
            return []
        factores: list[int] = []
        divisor = 2
        restante = n
        while divisor * divisor <= restante:
            if restante % divisor == 0:
                factores.append(divisor)
                while restante % divisor == 0:
                    restante //= divisor
            divisor += 1 if divisor == 2 else 2
        if restante > 1:
            factores.append(restante)
        return factores

    @classmethod
    def verificar_hull_dobell(
        cls, multiplicador: int, incremento: int, modulo: int
    ) -> ResultadoHullDobell:
        """Verifica las tres condiciones de Hull-Dobell para el periodo completo."""
        factores = cls.factores_primos(modulo)
        condiciones: list[CondicionHullDobell] = []

        condicion_c = all(incremento % factor == 1 for factor in factores)
        condiciones.append(
            CondicionHullDobell(
                descripcion="c - 1 debe ser divisible por cada factor primo de m",
                cumple=condicion_c,
                detalle=(
                    f"c = {incremento}, factores primos de m = {factores}, "
                    f"c mod p = {[incremento % factor for factor in factores]}"
                ),
            )
        )

        condicion_a = all(multiplicador % factor == 1 for factor in factores)
        condiciones.append(
            CondicionHullDobell(
                descripcion="a - 1 debe ser divisible por cada factor primo de m",
                cumple=condicion_a,
                detalle=(
                    f"a = {multiplicador}, a mod p = "
                    f"{[multiplicador % factor for factor in factores]}"
                ),
            )
        )

        if modulo % 4 == 0:
            condicion_cuatro = multiplicador % 4 == 1
            condiciones.append(
                CondicionHullDobell(
                    descripcion="a debe ser congruente con 1 modulo 4 (m divisible por 4)",
                    cumple=condicion_cuatro,
                    detalle=f"a mod 4 = {multiplicador % 4}",
                )
            )

        periodo = modulo if all(c.cumple for c in condiciones) else 0
        return ResultadoHullDobell(
            multiplicador=multiplicador,
            incremento=incremento,
            modulo=modulo,
            condiciones=condiciones,
            periodo_teorico=periodo,
        )

    @classmethod
    def periodo_teorico(cls, multiplicador: int, increment0: int, modulo: int) -> int:
        """Periodo teorico del generador segun Hull-Dobell (0 si no se cumple)."""
        return cls.verificar_hull_dobell(multiplicador, increment0, modulo).periodo_teorico

    @classmethod
    def periodo_empirico(cls, generador: Generador, limite: int | None = None) -> int | None:
        """Detecta empiricamente el ciclo del generador.

        Devuelve la longitud del ciclo si se encuentra una repeticion dentro
        del limite evaluado; en caso contrario devuelve None, lo que significa
        que el ciclo es mas largo que las muestras generadas.
        """
        total = limite if limite is not None else 100000
        vistos: dict[int, int] = {}
        estado = generador.semilla
        for indice in range(total):
            if estado in vistos:
                return indice - vistos[estado]
            vistos[estado] = indice
            estado = (generador.multiplicador * estado + generador.incremento) % generador.modulo
        return None

    @staticmethod
    def estadisticas(valores: Sequence[float]) -> dict[str, float]:
        """Calcula estadisticas descriptivas de los valores normalizados."""
        if not valores:
            return {
                "cantidad": 0,
                "minimo": float("nan"),
                "maximo": float("nan"),
                "media": float("nan"),
                "varianza": float("nan"),
                "desviacion_estandar": float("nan"),
                "suma": 0.0,
            }
        cantidad = len(valores)
        suma = float(sum(valores))
        media = suma / cantidad
        varianza = sum((valor - media) ** 2 for valor in valores) / cantidad
        return {
            "cantidad": cantidad,
            "minimo": min(valores),
            "maximo": max(valores),
            "media": media,
            "varianza": varianza,
            "desviacion_estandar": math.sqrt(varianza),
            "suma": suma,
        }

    @classmethod
    def prueba_chi_cuadrado(
        cls, valores: Sequence[float], bins: int = 20, intervalo_confianza: float = 0.95
    ) -> ResultadoChiCuadrado:
        """Prueba de uniformidad chi-cuadrado sobre el intervalo [0, 1)."""
        if bins < 2:
            raise ValueError("El numero de intervalos debe ser mayor o igual a 2.")
        if not valores:
            raise ValueError("La secuencia debe contener al menos un valor.")

        frecuencia_esperada = len(valores) / bins
        frecuencias = [0] * bins
        for valor in valores:
            indice = min(int(valor * bins), bins - 1)
            frecuencias[indice] += 1

        estadistico = sum(
            (observado - frecuencia_esperada) ** 2 / frecuencia_esperada
            for observado in frecuencias
        )
        grados_libertad = bins - 1
        valor_critico = cls._valor_critico(grados_libertad, intervalo_confianza)
        return ResultadoChiCuadrado(
            intervalo_confianza=intervalo_confianza,
            bins=bins,
            frecuencias_observadas=frecuencias,
            frecuencias_esperadas=[frecuencia_esperada] * bins,
            estadistico=estadistico,
            valor_critico=valor_critico,
            grados_libertad=grados_libertad,
            rechaza_hipotesis=estadistico > valor_critico,
        )

    @staticmethod
    def _valor_critico(grados_libertad: int, intervalo_confianza: float) -> float:
        """Valor critico tabulado de chi-cuadrado para los casos usados en el curso."""
        tabla = {
            (19, 0.95): Analisis.VALOR_CRITICO_CHI_CUADRADO_19,
            (19, 0.99): Analisis.VALOR_CRITICO_CHI_CUADRADO_20,
            (9, 0.95): Analisis.VALOR_CRITICO_CHI_CUADRADO_10,
            (4, 0.95): Analisis.VALOR_CRITICO_CHI_CUADRADO_05,
            (3, 0.99): Analisis.VALOR_CRITICO_CHI_CUADRADO_01,
        }
        clave = (grados_libertad, intervalo_confianza)
        if clave in tabla:
            return tabla[clave]
        if grados_libertad == 19:
            return Analisis.VALOR_CRITICO_CHI_CUADRADO_19
        if grados_libertad == 9:
            return Analisis.VALOR_CRITICO_CHI_CUADRADO_10
        if grados_libertad == 4:
            return Analisis.VALOR_CRITICO_CHI_CUADRADO_05
        return Analisis.VALOR_CRITICO_CHI_CUADRADO_01

    @staticmethod
    def analisis_de_uniformidad(valores: Sequence[float], bins: int = 10) -> dict[str, float]:
        """Verifica que la media sea cercana a 0.5 y la varianza a 1/12."""
        estadisticas = Analisis.estadisticas(valores)
        if not valores:
            return estadisticas
        return {
            **estadisticas,
            "error_medio": abs(estadisticas["media"] - 0.5),
            "error_varianza": abs(estadisticas["varianza"] - 1.0 / 12.0),
        }

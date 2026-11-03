"""Servicio de comparacion entre secuencias pseudoaleatorias.

Capa de LOGICA DE NEGOCIO: centraliza la comparacion de secuencias generadas
por distintas implementaciones (por ejemplo Python frente a Java) y de archivos
CSV con el mismo formato de intercambio.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Diferencia:
    """Diferencia detectada entre dos secuencias en un indice dado."""

    indice: int
    valor_izquierdo: int | None
    valor_derecho: int | None

    def __str__(self) -> str:
        return f"indice {self.indice}: {self.valor_izquierdo} != {self.valor_derecho}"


@dataclass(frozen=True)
class ResultadoComparacion:
    """Resultado de comparar dos secuencias de estados crudos X(n)."""

    identicas: bool
    total_comparadas: int
    longitud_izquierda: int
    longitud_derecha: int
    diferencias: list[Diferencia] = field(default_factory=list)
    primera_diferencia: Diferencia | None = None
    total_diferencias: int = 0

    @property
    def mensaje(self) -> str:
        """Mensaje resumen de la comparacion."""
        if self.identicas:
            return (
                f"SECUENCIAS IDENTICAS: las {self.total_comparadas} observaciones "
                "comparadas coinciden exactamente."
            )
        detalle = str(self.primera_diferencia) if self.primera_diferencia else "sin detalle"
        return (
            f"SECUENCIAS DIFERENTES: {self.total_diferencias} diferencia(s) "
            f"detectada(s). Primera: {detalle}."
        )


class Comparador:
    """Servicio de comparacion de secuencias y de archivos CSV."""

    @staticmethod
    def comparar_secuencias(
        izquierda: Sequence[int], derecha: Sequence[int], maximo_diferencias: int = 20
    ) -> ResultadoComparacion:
        """Compara dos secuencias de estados crudos elemento a elemento."""
        total = min(len(izquierda), len(derecha))
        diferencias: list[Diferencia] = []
        total_diferencias = 0
        for indice in range(total):
            if izquierda[indice] != derecha[indice]:
                total_diferencias += 1
                if len(diferencias) < maximo_diferencias:
                    diferencias.append(Diferencia(indice, izquierda[indice], derecha[indice]))
        identicas = len(izquierda) == len(derecha) and total_diferencias == 0
        return ResultadoComparacion(
            identicas=identicas,
            total_comparadas=total,
            longitud_izquierda=len(izquierda),
            longitud_derecha=len(derecha),
            diferencias=diferencias,
            primera_diferencia=diferencias[0] if diferencias else None,
            total_diferencias=total_diferencias,
        )

    @staticmethod
    def comparar_archivos_csv(
        ruta_izquierda: str, ruta_derecha: str, maximo_diferencias: int = 20
    ) -> ResultadoComparacion:
        """Compara dos archivos CSV de resultados con la misma estructura."""
        from datos.exportador_csv import ExportadorCSV

        estados_izquierda = ExportadorCSV.leer_estados(ruta_izquierda)
        estados_derecha = ExportadorCSV.leer_estados(ruta_derecha)
        return Comparador.comparar_secuencias(
            estados_izquierda, estados_derecha, maximo_diferencias
        )

    @staticmethod
    def tabla_primeras_observaciones(
        izquierda: Sequence[int], derecha: Sequence[int], modulo: int, cantidad: int = 20
    ) -> list[dict[str, object]]:
        """Construye la tabla comparativa de las primeras observaciones."""
        from datos.exportador_csv import formatear_normalizado_exacto

        filas: list[dict[str, object]] = []
        for indice in range(min(cantidad, len(izquierda), len(derecha))):
            estado_izq = izquierda[indice]
            estado_der = derecha[indice]
            filas.append(
                {
                    "indice": indice + 1,
                    "x_python": estado_izq,
                    "x_java": estado_der,
                    "u_python": formatear_normalizado_exacto(estado_izq, modulo),
                    "u_java": formatear_normalizado_exacto(estado_der, modulo),
                    "coincide": estado_izq == estado_der,
                }
            )
        return filas

    @staticmethod
    def comparar_semillas(primera: Sequence[int], segunda: Sequence[int]) -> ResultadoComparacion:
        """Compara las secuencias generadas con dos semillas distintas."""
        return Comparador.comparar_secuencias(primera, segunda)

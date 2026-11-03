"""Generacion de graficas de la simulacion (CAPA DE PRESENTACION).

Utiliza Matplotlib con el motor `Agg`, que permite generar las imagenes sin
interfaz grafica y guardarlas directamente en disco.
"""

from __future__ import annotations

import os
from collections.abc import Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

COLORES = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd"]


class GeneradorGraficas:
    """Servicio de presentacion que produce las graficas de la simulacion."""

    def __init__(self, directorio: str, resolucion: int = 150) -> None:
        self._directorio = directorio
        self._resolucion = resolucion
        os.makedirs(self._directorio, exist_ok=True)

    @property
    def directorio(self) -> str:
        """Carpeta donde se guardan las graficas."""
        return self._directorio

    def grafica_secuencia(
        self,
        valores: Sequence[float],
        nombre_archivo: str = "secuencia_normalizada.png",
        titulo: str = "Generador Congruencial Lineal (a=1664525, c=1013904223, m=2^32)",
        etiqueta_semilla: int = 12345,
    ) -> str:
        """Grafica los valores normalizados U(n) generados por el LCG."""
        figura, eje = plt.subplots(figsize=(12, 5.5))
        ejes_x = list(range(1, len(valores) + 1))
        eje.plot(ejes_x, valores, color=COLORES[0], linewidth=0.8, alpha=0.85)
        eje.set_title(titulo, fontsize=13, pad=12)
        eje.set_xlabel("Número de prueba n", fontsize=11)
        eje.set_ylabel("Valor pseudoaleatorio U(n) = X(n)/m", fontsize=11)
        eje.set_xlim(1, max(len(valores), 2))
        eje.set_ylim(0, 1)
        eje.grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
        eje.legend(
            handles=[
                plt.Line2D([], [], color=COLORES[0], label=f"Semilla X(0) = {etiqueta_semilla}")
            ],
            loc="upper right",
        )
        figura.tight_layout()
        return self._guardar(figura, nombre_archivo)

    def grafica_comparativa_semillas(
        self,
        secuencias: dict[int, Sequence[float]],
        nombre_archivo: str = "comparativa_semillas.png",
        titulo: str = "Comparación de dos semillas iniciales del LCG",
        muestras: int = 500,
    ) -> str:
        """Grafica comparativa de las secuencias generadas con semillas distintas."""
        figura, ejes = plt.subplots(1, 2, figsize=(14, 5.5))
        colores = sorted(secuencias.keys())
        for indice, semilla in enumerate(colores):
            valores = secuencias[semilla]
            color = COLORES[indice % len(COLORES)]
            ejes_x = list(range(1, min(muestras, len(valores)) + 1))
            ejes[0].plot(
                ejes_x,
                valores[: len(ejes_x)],
                color=color,
                linewidth=0.9,
                alpha=0.85,
                label=f"Semilla {semilla}",
            )
        ejes[0].set_title(f"Serie temporal (primeras {muestras} observaciones)", fontsize=12)
        ejes[0].set_xlabel("Número de prueba n", fontsize=11)
        ejes[0].set_ylabel("Valor pseudoaleatorio U(n) = X(n)/m", fontsize=11)
        ejes[0].set_ylim(0, 1)
        ejes[0].grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
        ejes[0].legend(title="Semillas comparadas", loc="upper right")

        if len(colores) >= 2:
            primera = list(secuencias[colores[0]])
            segunda = list(secuencias[colores[1]])
            total = min(len(primera), len(segunda))
            ejes[1].scatter(
                primera[:total],
                segunda[:total],
                s=6,
                alpha=0.35,
                color=COLORES[2 % len(COLORES)],
                edgecolors="none",
            )
            ejes[1].set_title(
                f"Dispersión U(n) con semilla {colores[0]} frente a U(n) con semilla {colores[1]}",
                fontsize=12,
            )
            ejes[1].set_xlabel(f"U(n) - semilla {colores[0]}", fontsize=11)
            ejes[1].set_ylabel(f"U(n) - semilla {colores[1]}", fontsize=11)
            ejes[1].set_xlim(0, 1)
            ejes[1].set_ylim(0, 1)
            ejes[1].grid(True, linestyle="--", linewidth=0.6, alpha=0.6)

        figura.suptitle(titulo, fontsize=13)
        figura.tight_layout()
        return self._guardar(figura, nombre_archivo)

    def histograma(
        self,
        valores: Sequence[float],
        nombre_archivo: str = "histograma_frecuencias.png",
        bins: int = 50,
        titulo: str = "Histograma de frecuencias de los valores pseudoaleatorios",
    ) -> str:
        """Histograma de frecuencias de los valores normalizados."""
        figura, eje = plt.subplots(figsize=(10, 5.5))
        eje.hist(
            valores, bins=bins, range=(0.0, 1.0), color=COLORES[0], edgecolor="white", alpha=0.85
        )
        eje.axhline(
            len(valores) / bins,
            color=COLORES[1],
            linestyle="--",
            linewidth=1.5,
            label=f"Frecuencia esperada = {len(valores) / bins:.0f}",
        )
        eje.set_title(titulo, fontsize=13, pad=12)
        eje.set_xlabel("Intervalo del valor pseudoaleatorio U(n)", fontsize=11)
        eje.set_ylabel("Frecuencia absoluta", fontsize=11)
        eje.grid(True, linestyle="--", linewidth=0.6, alpha=0.6, axis="y")
        eje.legend(loc="upper right")
        figura.tight_layout()
        return self._guardar(figura, nombre_archivo)

    def grafica_comparativa_python_java(
        self,
        valores_python: Sequence[float],
        valores_java: Sequence[float],
        nombre_archivo: str = "comparativa_python_java.png",
        titulo: str = "Verificación de la igualdad entre las secuencias de Python y Java",
    ) -> str:
        """Grafica que superpone las secuencias de Python y Java para verificar su igualdad."""
        total = min(len(valores_python), len(valores_java))
        figura, ejes = plt.subplots(1, 2, figsize=(14, 5.5))

        ejes[0].scatter(
            valores_python[:total],
            valores_java[:total],
            s=6,
            alpha=0.35,
            color=COLORES[0],
            edgecolors="none",
            label="Observaciones (U Python, U Java)",
        )
        ejes[0].plot(
            [0, 1],
            [0, 1],
            color=COLORES[1],
            linestyle="--",
            linewidth=1.6,
            label="U Python = U Java",
        )
        ejes[0].set_title("Dispersión de los valores normalizados", fontsize=12)
        ejes[0].set_xlabel("U(n) generado por Python", fontsize=11)
        ejes[0].set_ylabel("U(n) generado por Java", fontsize=11)
        ejes[0].set_xlim(0, 1)
        ejes[0].set_ylim(0, 1)
        ejes[0].grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
        ejes[0].legend(loc="upper left", fontsize=9)

        diferencias = [
            abs(a - b) for a, b in zip(valores_python[:total], valores_java[:total], strict=False)
        ]
        ejes[1].plot(
            list(range(1, total + 1)),
            diferencias,
            color=COLORES[2 % len(COLORES)],
            linewidth=0.9,
            alpha=0.9,
            label="|U(n) Python - U(n) Java|",
        )
        ejes[1].set_title("Diferencia absoluta entre ambos lenguajes", fontsize=12)
        ejes[1].set_xlabel("Número de prueba n", fontsize=11)
        ejes[1].set_ylabel("Diferencia absoluta", fontsize=11)
        ejes[1].set_xlim(1, max(total, 2))
        ejes[1].grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
        ejes[1].legend(loc="upper right", fontsize=9)

        figura.suptitle(titulo, fontsize=13)
        figura.tight_layout()
        return self._guardar(figura, nombre_archivo)

    def _guardar(self, figura, nombre_archivo: str) -> str:
        """Guarda la figura en disco y libera los recursos."""
        ruta = os.path.join(self._directorio, nombre_archivo)
        figura.savefig(ruta, dpi=self._resolucion, bbox_inches="tight")
        plt.close(figura)
        return ruta

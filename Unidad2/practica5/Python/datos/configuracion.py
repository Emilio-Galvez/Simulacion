"""Capa de DATOS: lectura de la configuracion de la simulacion.

La configuracion se guarda en un archivo INI (`configuracion.ini`) legible
tanto por Python (`configparser`) como por Java, de modo que ambos programas
compartan exactamente los mismos parametros matematicos.
"""

from __future__ import annotations

import configparser
import os
from dataclasses import dataclass, replace

from estrategias.estrategia_lcg import (
    CANTIDAD_POR_DEFECTO,
    INCREMENTO_POR_DEFECTO,
    MODULO_POR_DEFECTO,
    MULTIPLICADOR_POR_DEFECTO,
    SEMILLA_POR_DEFECTO,
)
from estrategias.interfaz_generador import ParametrosInvalidosError

SECCION = "lcg"


@dataclass(frozen=True)
class Configuracion:
    """Parametros de una simulacion LCG."""

    multiplicador: int = MULTIPLICADOR_POR_DEFECTO
    incremento: int = INCREMENTO_POR_DEFECTO
    modulo: int = MODULO_POR_DEFECTO
    semilla: int = SEMILLA_POR_DEFECTO
    cantidad: int = CANTIDAD_POR_DEFECTO

    def validar(self) -> None:
        """Valida los parametros de la simulacion."""
        if self.multiplicador <= 0:
            raise ParametrosInvalidosError("El multiplicador a debe ser mayor que cero.")
        if self.modulo <= 1:
            raise ParametrosInvalidosError("El modulo m debe ser mayor que uno.")
        if not 0 <= self.incremento < self.modulo:
            raise ParametrosInvalidosError("El incremento c debe cumplir 0 <= c < m.")
        if not 0 <= self.semilla < self.modulo:
            raise ParametrosInvalidosError("La semilla debe cumplir 0 <= X(0) < m.")
        if self.cantidad <= 0:
            raise ParametrosInvalidosError("La cantidad de numeros debe ser mayor que cero.")

    def con_semilla(self, semilla: int) -> Configuracion:
        """Devuelve una copia de la configuracion con otra semilla inicial."""
        nueva = replace(self, semilla=semilla)
        nueva.validar()
        return nueva

    @classmethod
    def por_defecto(cls) -> Configuracion:
        """Configuracion con los parametros obligatorios de la practica."""
        configuracion = cls()
        configuracion.validar()
        return configuracion

    @classmethod
    def desde_archivo(cls, ruta: str | None = None) -> Configuracion:
        """Lee la configuracion desde un archivo INI; si no existe, usa los valores por defecto."""
        if ruta is None or not os.path.isfile(ruta):
            configuracion = cls()
            configuracion.validar()
            return configuracion

        parser = configparser.ConfigParser()
        parser.read(ruta, encoding="utf-8")
        if not parser.has_section(SECCION):
            raise ParametrosInvalidosError(
                f"El archivo '{ruta}' no contiene la seccion [{SECCION}]."
            )

        configuracion = cls(
            multiplicador=parser.getint(
                SECCION, "multiplicador", fallback=MULTIPLICADOR_POR_DEFECTO
            ),
            incremento=parser.getint(SECCION, "incremento", fallback=INCREMENTO_POR_DEFECTO),
            modulo=parser.getint(SECCION, "modulo", fallback=MODULO_POR_DEFECTO),
            semilla=parser.getint(SECCION, "semilla", fallback=SEMILLA_POR_DEFECTO),
            cantidad=parser.getint(SECCION, "cantidad", fallback=CANTIDAD_POR_DEFECTO),
        )
        configuracion.validar()
        return configuracion

    def escribir_archivo(self, ruta: str) -> str:
        """Escribe la configuracion actual en un archivo INI."""
        parser = configparser.ConfigParser()
        parser[SECCION] = {
            "multiplicador": str(self.multiplicador),
            "incremento": str(self.incremento),
            "modulo": str(self.modulo),
            "semilla": str(self.semilla),
            "cantidad": str(self.cantidad),
        }
        os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            parser.write(archivo)
        return os.path.abspath(ruta)

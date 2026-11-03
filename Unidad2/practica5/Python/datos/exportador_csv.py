"""Capa de DATOS: persistencia de resultados en archivos CSV.

Define el formato de intercambio entre las implementaciones de Python y Java:

    indice,x,normalizado

El campo `x` contiene el estado crudo X(n) y `normalizado` la magnitud U(n)
con 12 decimales calculados mediante division entera exacta, de modo que el
texto generado por Python y por Java sea byte a byte identico.
"""

from __future__ import annotations

import csv
import os
from collections.abc import Iterable, Mapping, Sequence

ENCABEZADO_RESULTADOS = ["indice", "x", "normalizado"]
ENCABEZADO_COMPARACION = [
    "indice",
    "x_python",
    "x_java",
    "u_python",
    "u_java",
    "coincide",
]
DECIMALES_NORMALIZADO = 12


def formatear_normalizado_exacto(
    estado: int, modulo: int, decimales: int = DECIMALES_NORMALIZADO
) -> str:
    """Convierte U(n) = X(n) / m en texto decimal exacto y truncado.

    Se usa aritmetica de enteros (X(n) * 10^d) / m en lugar de redondeo en
    punto flotante: Python redondea al par y Java al alza, por lo que un
    valor con empate (por ejemplo 0.00048828125) podria imprimir distinto en
    cada lenguaje. La division entera garantiza igualdad exacta.
    """
    if modulo <= 0:
        raise ValueError("El modulo debe ser positivo.")
    escala = 10**decimales
    escalado = (estado * escala) // modulo
    parte_entera, parte_decimal = divmod(escalado, escala)
    return f"{parte_entera}.{parte_decimal:0{decimales}d}"


class ExportadorCSV:
    """Servicio de la capa de datos para escribir y leer resultados en CSV."""

    @staticmethod
    def exportar_resultados(
        ruta: str, estados: Sequence[int], modulo: int, decimales: int = DECIMALES_NORMALIZADO
    ) -> str:
        """Exporta una secuencia de estados crudos al formato CSV de resultados."""
        directorio = os.path.dirname(os.path.abspath(ruta))
        os.makedirs(directorio, exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo, lineterminator="\n")
            escritor.writerow(ENCABEZADO_RESULTADOS)
            for indice, estado in enumerate(estados, start=1):
                escritor.writerow(
                    [indice, estado, formatear_normalizado_exacto(estado, modulo, decimales)]
                )
        return os.path.abspath(ruta)

    @staticmethod
    def exportar_comparacion(ruta: str, filas: Iterable[Mapping[str, object]]) -> str:
        """Exporta la tabla comparativa Python vs Java a un archivo CSV."""
        directorio = os.path.dirname(os.path.abspath(ruta))
        os.makedirs(directorio, exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(
                archivo, fieldnames=ENCABEZADO_COMPARACION, lineterminator="\n"
            )
            escritor.writeheader()
            for fila in filas:
                escritor.writerow(
                    {
                        "indice": fila["indice"],
                        "x_python": fila["x_python"],
                        "x_java": fila["x_java"],
                        "u_python": fila["u_python"],
                        "u_java": fila["u_java"],
                        "coincide": "si" if fila["coincide"] else "no",
                    }
                )
        return os.path.abspath(ruta)

    @staticmethod
    def exportar_comparacion_semillas(
        ruta: str, filas: Iterable[Mapping[str, object]], encabezados: Sequence[str]
    ) -> str:
        """Exporta la comparacion entre dos semillas a un archivo CSV."""
        directorio = os.path.dirname(os.path.abspath(ruta))
        os.makedirs(directorio, exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo, lineterminator="\n")
            escritor.writerow(list(encabezados))
            for fila in filas:
                escritor.writerow(list(fila.values()))
        return os.path.abspath(ruta)

    @staticmethod
    def leer_resultados(ruta: str) -> list[dict[str, str]]:
        """Lee un CSV de resultados y devuelve sus filas como diccionarios."""
        with open(ruta, newline="", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo))

    @staticmethod
    def leer_estados(ruta: str) -> list[int]:
        """Lee un CSV de resultados y devuelve la columna de estados crudos."""
        with open(ruta, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            return [int(fila["x"]) for fila in lector]

    @staticmethod
    def archivo_existe(ruta: str) -> bool:
        """Indica si el archivo indicado existe."""
        return os.path.isfile(ruta)

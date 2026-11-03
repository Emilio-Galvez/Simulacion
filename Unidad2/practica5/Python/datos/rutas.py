"""Utilidad de la capa de DATOS para localizar la raiz del proyecto.

Permite que los programas funcionen independientemente del directorio de
trabajo desde el que se ejecuten, localizando la carpeta que contiene los
modulos `Python`, `Java` y `Resultados`.
"""

from __future__ import annotations

import os

NOMBRES_RAIZ = ("Python", "Java")
DIRECTORIO_RESULTADOS = "Resultados"
DIRECTORIO_GRAFICAS = "graficas"
ARCHIVO_CONFIGURACION = "configuracion.ini"


def encontrar_raiz_proyecto(inicio: str | None = None) -> str:
    """Busca la raiz del proyecto subiendo directorios hasta el sistema de archivos."""
    actual = os.path.abspath(inicio or os.getcwd())
    while True:
        if all(os.path.isdir(os.path.join(actual, nombre)) for nombre in NOMBRES_RAIZ):
            return actual
        padre = os.path.dirname(actual)
        if padre == actual:
            break
        actual = padre
    return os.path.abspath(inicio or os.getcwd())


def directorio_resultados(raiz: str | None = None) -> str:
    """Ruta de la carpeta de resultados."""
    raiz_proyecto = raiz or encontrar_raiz_proyecto()
    return os.path.join(raiz_proyecto, DIRECTORIO_RESULTADOS)


def directorio_graficas(raiz: str | None = None) -> str:
    """Ruta de la carpeta de graficas."""
    return os.path.join(directorio_resultados(raiz), DIRECTORIO_GRAFICAS)


def ruta_configuracion(raiz: str | None = None) -> str:
    """Ruta del archivo de configuracion INI del proyecto."""
    raiz_proyecto = raiz or encontrar_raiz_proyecto()
    return os.path.join(raiz_proyecto, ARCHIVO_CONFIGURACION)

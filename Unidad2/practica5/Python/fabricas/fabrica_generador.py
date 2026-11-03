"""Factory Method para crear instancias de generadores pseudoaleatorios.

Permite registrar nuevas estrategias (LCG, Mersenne Twister, Lehmer, ...)
sin modificar el codigo cliente: basta con registrar el constructor asociado
al nuevo tipo. Pertenece a la CAPA DE LOGICA DE NEGOCIO.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import ClassVar

from estrategias.estrategia_lcg import EstrategiaLCG
from estrategias.interfaz_generador import Generador

ConstructorGenerador = Callable[..., Generador]


class TipoGeneradorDesconocidoError(ValueError):
    """Error de negocio lanzado cuando se solicita un generador no registrado."""


class FabricaGenerador:
    """Fachada de creacion de estrategias de generacion."""

    _registro: ClassVar[dict[str, ConstructorGenerador]] = {}

    @classmethod
    def registrar(cls, tipo: str, constructor: ConstructorGenerador) -> None:
        """Registra (o reemplaza) el constructor asociado a un tipo de generador."""
        clave = tipo.strip().upper()
        if not clave:
            raise TipoGeneradorDesconocidoError("El tipo de generador no puede estar vacio.")
        cls._registro[clave] = constructor

    @classmethod
    def crear(cls, tipo: str = "LCG", **parametros) -> Generador:
        """Crea un generador del tipo indicado aplicando sus parametros."""
        clave = (tipo or "").strip().upper()
        constructor = cls._registro.get(clave)
        if constructor is None:
            disponibles = ", ".join(sorted(cls._registro.keys())) or "ninguno"
            raise TipoGeneradorDesconocidoError(
                f"Generador desconocido: '{tipo}'. Disponibles: {disponibles}."
            )
        return constructor(**parametros)

    @classmethod
    def registrar_tipos_disponibles(cls) -> list[str]:
        """Lista los tipos de generador registrados en la fabrica."""
        return sorted(cls._registro.keys())

    @classmethod
    def _registro_inicial(cls) -> None:
        """Registra las estrategias incluidas de serie en el proyecto."""
        cls.registrar("LCG", EstrategiaLCG)


FabricaGenerador._registro_inicial()


def crear_generador(
    multiplicador: int | None = None,
    incremento: int | None = None,
    modulo: int | None = None,
    semilla: int | None = None,
    tipo: str = "LCG",
) -> Generador:
    """Atajo funcional para crear un generador usando los valores por defecto."""
    from estrategias.estrategia_lcg import (
        INCREMENTO_POR_DEFECTO,
        MODULO_POR_DEFECTO,
        MULTIPLICADOR_POR_DEFECTO,
        SEMILLA_POR_DEFECTO,
    )

    return FabricaGenerador.crear(
        tipo,
        multiplicador=MULTIPLICADOR_POR_DEFECTO if multiplicador is None else multiplicador,
        incremento=INCREMENTO_POR_DEFECTO if incremento is None else incremento,
        modulo=MODULO_POR_DEFECTO if modulo is None else modulo,
        semilla=SEMILLA_POR_DEFECTO if semilla is None else semilla,
    )

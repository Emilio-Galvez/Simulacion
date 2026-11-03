"""Fabricas de creacion de generadores (patron Factory Method)."""

from fabricas.fabrica_generador import (
    FabricaGenerador,
    TipoGeneradorDesconocidoError,
    crear_generador,
)

__all__ = ["FabricaGenerador", "TipoGeneradorDesconocidoError", "crear_generador"]

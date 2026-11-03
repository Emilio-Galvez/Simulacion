"""Servicio de dominio del Generador Congruencial Lineal.

Este modulo actua como fachada de la CAPA DE LOGICA DE NEGOCIO: coordina la
validacion de parametros, la obtencion de la estrategia mediante la Fabrica
(Factory Method), la generacion de la secuencia y la normalizacion de los
valores, sin depender de la capa de presentacion ni de la capa de datos.
"""

from __future__ import annotations

from dataclasses import dataclass

from datos.configuracion import Configuracion
from estrategias.interfaz_generador import Generador
from fabricas.fabrica_generador import FabricaGenerador
from servicios.analisis import Analisis


@dataclass(frozen=True)
class ResultadoSimulacion:
    """Resultado completo de una simulacion LCG."""

    semilla: int
    estados: list[int]
    normalizados: list[float]
    estadisticas: dict[str, float]

    @property
    def cantidad(self) -> int:
        """Cantidad de valores generados."""
        return len(self.estados)

    def primeros(self, cantidad: int = 20) -> list[int]:
        """Primeros estados crudos de la simulacion."""
        return self.estados[:cantidad]


class ServicioLCG:
    """Servicio de negocio que ejecuta simulaciones con generadores LCG."""

    TIPO_GENERADOR = "LCG"

    def __init__(self, configuracion: Configuracion | None = None) -> None:
        self._configuracion = configuracion or Configuracion.por_defecto()
        self._configuracion.validar()

    @property
    def configuracion(self) -> Configuracion:
        """Configuracion vigente del servicio."""
        return self._configuracion

    def crear_generador(self, semilla: int | None = None) -> Generador:
        """Crea la estrategia LCG a traves de la Fabrica (patron Factory Method)."""
        configuracion = (
            self._configuracion.con_semilla(semilla) if semilla is not None else self._configuracion
        )
        return FabricaGenerador.crear(
            self.TIPO_GENERADOR,
            multiplicador=configuracion.multiplicador,
            incremento=configuracion.incremento,
            modulo=configuracion.modulo,
            semilla=configuracion.semilla,
        )

    def simular(self, semilla: int | None = None) -> ResultadoSimulacion:
        """Ejecuta la simulacion y devuelve estados, valores normalizados y estadisticas."""
        generador = self.crear_generador(semilla)
        estados = generador.generar(self._configuracion.cantidad)
        normalizados = [generador.normalizar(estado) for estado in estados]
        estadisticas = Analisis.estadisticas(normalizados)
        return ResultadoSimulacion(
            semilla=generador.semilla,
            estados=estados,
            normalizados=normalizados,
            estadisticas=estadisticas,
        )

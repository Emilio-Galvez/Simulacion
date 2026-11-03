"""Contrato Strategy para las estrategias de generacion de numeros pseudoaleatorios.

Este modulo pertenece a la CAPA DE LOGICA DE NEGOCIO y define la interfaz
comun que deben cumplir todos los generadores. Gracias a este contrato la
capa de presentacion puede trabajar con cualquier estrategia sin conocer sus
detalles internos (acoplamiento minimo).
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ParametrosInvalidosError(ValueError):
    """Error de negocio lanzado cuando los parametros del generador son invalidos."""


class Generador(ABC):
    """Estrategia abstracta de generacion de numeros pseudoaleatorios.

    Concrete esta interfaz para incorporar nuevos algoritmos (por ejemplo un
    Mersenne Twister o un Lehmer) sin modificar la logica principal del
    sistema (patron Strategy).
    """

    @abstractmethod
    def generar(self, cantidad: int) -> list[int]:
        """Genera la cantidad indicada de estados crudos X(n)."""

    @abstractmethod
    def normalizar(self, estado: int) -> float:
        """Normaliza un estado crudo mediante U(n) = X(n) / m."""

    def generar_normalizados(self, cantidad: int) -> list[float]:
        """Genera la cantidad indicada de valores normalizados U(n)."""
        return [self.normalizar(estado) for estado in self.generar(cantidad)]

    @property
    @abstractmethod
    def multiplicador(self) -> int:
        """Valor del multiplicador a."""

    @property
    @abstractmethod
    def incremento(self) -> int:
        """Valor del incremento c."""

    @property
    @abstractmethod
    def modulo(self) -> int:
        """Valor del modulo m."""

    @property
    @abstractmethod
    def semilla(self) -> int:
        """Semilla inicial X(0)."""

    @property
    def nombre(self) -> str:
        """Nombre descriptivo de la estrategia."""
        return type(self).__name__

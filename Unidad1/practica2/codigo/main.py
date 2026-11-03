from modelos.deterministico import ModeloDeterministico
from modelos.discreto import ModeloDiscreto
from modelos.estocastico import ModeloEstocastico
from modelos.continuo import ModeloContinuo

from observer.observer import Subject
from observer.tabla import Tabla
from observer.grafica import Grafica


def main():
    subject = Subject()

    tabla = Tabla()
    grafica = Grafica()

    subject.agregar_observador(tabla)
    subject.agregar_observador(grafica)

    modelo = ModeloDeterministico()

    resultados = modelo.simular()

    subject.notificar(resultados)


if __name__ == "__main__":
    main()




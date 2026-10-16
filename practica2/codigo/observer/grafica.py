import matplotlib.pyplot as plt

from observer.observer import Observer


class Grafica(Observer):

    def actualizar(self, resultados):
        tiempos = range(len(resultados))

        plt.plot(tiempos, resultados, marker="o")
        plt.title("Crecimiento de la población")
        plt.xlabel("Tiempo")
        plt.ylabel("Población")
        plt.grid(True)
        plt.show()
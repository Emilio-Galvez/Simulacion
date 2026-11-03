import math
from datos.datos_poblacion import P0, r, tiempo


class ModeloDeterministico:

    def simular(self):
        resultados = []  # Declaramos una lista en donde meteremos cada población

        for t in range(tiempo + 1):  # Recorremos el tiempo
            poblacion = P0 * math.exp(r * t)  # Calculamos la población en el tiempo correspondiente
            resultados.append(poblacion)  # Guardamos cada población en la lista de resultados

        return resultados
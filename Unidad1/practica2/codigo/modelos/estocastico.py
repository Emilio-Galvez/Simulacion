import numpy as np
from datos.datos_poblacion import P0, r, sigma, tiempo

class ModeloEstocastico:
    def simular(self):
        resultados = [] # Creamos una lista para almacenar resultados
        poblacion = P0

        for t in range(tiempo + 1):
            resultados.append(poblacion)

            incremento = r * poblacion
            ruido = np.random.normal(0, sigma) # 0  -> indica la media, es decir los valores aleatorios se distribuyen alrededor de cero
                                   # 20 -> indica la desviacion estandar, cuanto se dispersan los valores respecto a cero

            poblacion = poblacion + incremento + ruido

            if poblacion < 0:
                poblacion = 0 # Esto evitaa que el modelo devuelva una poblacion inferior a cero

        return resultados


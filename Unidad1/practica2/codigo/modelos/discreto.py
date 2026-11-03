from datos.datos_poblacion import P0, r, tiempo

class ModeloDiscreto:
    def simular(self):
        resultados = [] # Declaramos una lista
        poblacion = P0  # y declaramos una poblacion la cual se ira actualizando

        for t in range(tiempo+1):
            resultados.append(poblacion) # Guardamos la poblacion en cada instante de tiempo

            incremento = r * poblacion # Calculamos el incremento de la poblacion
            poblacion = poblacion + incremento # Actualizamos la poblacion

        return resultados
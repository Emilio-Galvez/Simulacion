from datos.factor_temperatura import FactorTemperatura
from simulador.modelo_prediccion import ModeloPrediccion

# Esta clase hereda de ModeloPrediccion, lo que significa que debe implementar el método calcular_indice.

class ModeloInicial(ModeloPrediccion):
    # Al crear un objeto de la clase ModeloInicial, este tendra su propio objeto de la clase FactorTemperatura, que se usara para obtener el factor de temperatura en el metodo calcular_indice.
    # Guardamos  un objeto de FactorTemperatura dentro de ModeloInicial
    def __init__(self):
        self.factor_temperatura = FactorTemperatura()
    
    # Se recibe un objeto de datos cliamticos y lo llamo dato
    # Se ussa el metodo calcular_indice de la clase modelo_prediccion
    # ModeloInicial contiene un objeto de FactorTemperatura y lo utiliza internamente para obtener Tf antes de calcular el índice.
    def calcular_indice(self, dato):
        tf = self.factor_temperatura.obtener_factor(dato.temperatura)

        indice = (
            0.5 * (dato.humedad / 100)
            + 0.3 * (dato.nubosidad / 100)
            + 0.2 * tf
        )

        return indice


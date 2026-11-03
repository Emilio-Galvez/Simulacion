from datos.factor_temperatura import FactorTemperatura
from simulador.modelo_prediccion import ModeloPrediccion


class ModeloAjustado(ModeloPrediccion):

    def __init__(self):
        self.factor_temperatura = FactorTemperatura()

    def calcular_indice(self, dato):
        tf = self.factor_temperatura.obtener_factor(dato.temperatura)

        indice = (
            0.4 * (dato.humedad / 100)
            + 0.5 * (dato.nubosidad / 100)
            + 0.1 * tf
        )

        return indice
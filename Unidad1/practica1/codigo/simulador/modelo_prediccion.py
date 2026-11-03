# Esta clase sirve para que cualquier modelo de predicciòn sepa que operarcion debe realizar
# Sirve como un contrato para que cualquier modelo de predicciòn implemente el metodo calcular_indice
# pass sirve para decir que la clase existe pero aun no tiene comportamiento definido, es como un marcador de posición para que se pueda implementar en el futuro.
class ModeloPrediccion:
    def calcular_indice(self, dato):
        pass
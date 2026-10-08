class Simulador:

    def __init__(self, modelo):
        self.modelo = modelo

    def ejecutar(self, dato):
        return self.modelo.calcular_indice(dato)
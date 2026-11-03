class Observer:

    def actualizar(self, resultados):
        pass

    
class Subject:

    def __init__(self):
        self.observadores = []

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def notificar(self, resultados):
        for observador in self.observadores:
            observador.actualizar(resultados)
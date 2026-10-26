class Resultado:               # Reune lo que pertenece a un escenario: metricas teoricas y simuladas
    def __init__(self, escenario):
        self.escenario = escenario
        self.teoricas = None
        self.simuladas = None
        self.clientes = []
        self.estados = []
        self.fotos = []
        self.mensaje = ""

    def fue_simulado(self):                # Devuelve TRUE cuando ya existen metricas simuladas
        return self.simuladas is not None

# El Controlador arma este paquete y la vista lo consulta para mostrar resultados
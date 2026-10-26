class Metricas:
    def __init__(self, rho, L, Lq, W, Wq):
        self.rho = rho # Utilizacion del servidor
        self.L = L     # Numero promedio de clientes en el sistema
        self.Lq = Lq   # Numero promedio de clientes en la cola
        self.W = W     # Tiempo promedio de espera en el sistema
        self.Wq = Wq   # Tiempo promedio de espera en la cola


# La teoria y las estadisticas simualdas calculan instancias de esta misma clase 
# asi pueden comaprar valroes equivalentes
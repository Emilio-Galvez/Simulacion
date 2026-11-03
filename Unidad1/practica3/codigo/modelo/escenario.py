class Escenario:                                             # Es una configuracion de la simualcion
    def __init__(self, numero, lam, mu, tiempo, condicion):
        self.numero = numero                                 
        self.lam = lam  # tasa de llegada de clientes
        self.mu = mu    # tasa de servicio
        self.tiempo = tiempo  # tiempo total de la simulación
        self.condicion = condicion  #que cumpla lam < mu para que sea estable

    def utilizacion(self): # Proporcion de uso del servidor en promedio
        return self.lam / self.mu   

    def es_estable(self):  # Verifica si el sistema es estable
        if self.lam > 0 and self.lam < self.mu: 
            return True
        return False


# El controlador usa esta comprobacion antes de la simualcion
# y la vista muestra los parametros y la utilizacion
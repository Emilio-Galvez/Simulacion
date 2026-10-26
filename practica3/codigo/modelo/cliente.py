class Cliente:
    def __init__(self, numero, llegada): # Esta clase representa a una persona en la cola
        self.numero = numero             # Guarda su numero
        self.llegada = llegada           # Su tiempo de llegada
        self.inicio_servicio = None      # El inicio del servicio
        self.salida = None               # Su tiempo de salida

    def tiempo_espera(self):                         # Nos sirve para saber cuanto espero
        return self.inicio_servicio - self.llegada 

    def tiempo_en_sistema(self):                     # Cuanto tiempo estuvo aqui
        return self.salida - self.llegada

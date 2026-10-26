class Foto: # Guarda una captura para la simulacion
    def __init__(self, tiempo, en_servicio, cola, espera_promedio):
        self.tiempo = tiempo 
        self.en_servicio = en_servicio # Numero del cliente atendido (0 si el servidor esta libre)
        self.cola = cola # Numeros de los clientes en la cola
        self.espera_promedio = espera_promedio # Tiempo promedio de espera en cola

        # El simulador toma estas capturas de forma periodica y la consola las dibuja, conserva detalles visuales como quien esta 
        # en cada lugar

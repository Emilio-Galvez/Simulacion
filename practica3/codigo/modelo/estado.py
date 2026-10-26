class Estado:                                         # Esta clase registra un instante
    def __init__(self, tiempo, en_cola, en_sistema):  
        self.tiempo = tiempo          # Tiempo del reloj de la simualcion cuuando se registro ese estado
        self.en_cola = en_cola        # Cuantos cleintes haye n cola
        self.en_sistema = en_sistema  # Cuantos clientes hay en el sistema (cola + servicio)


# El simulador guarda guarda estos registros cuando la situacion cambia
# luego las estadisticas los usan para medir promedios a lo largo del tiempo
# como el numero medio de clientes# Numero del cliente atendido (0 si els ervidor esta libre)
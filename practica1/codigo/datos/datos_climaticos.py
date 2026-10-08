class DatosClimaticos:
    def __init__(self, hora, humedad, nubosidad, temperatura):
        self.hora = hora
        self.humedad = humedad
        self.nubosidad = nubosidad
        self.temperatura = temperatura


# Lista con los datos climáticos
datos = [
    DatosClimaticos("06:00", 65, 40, 14),
    DatosClimaticos("08:00", 70, 50, 16),
    DatosClimaticos("10:00", 68, 45, 18),
    DatosClimaticos("12:00", 60, 30, 22),
    DatosClimaticos("14:00", 75, 70, 20),
    DatosClimaticos("16:00", 85, 85, 18),
    DatosClimaticos("18:00", 92, 95, 16),
    DatosClimaticos("20:00", 88, 90, 17),
    DatosClimaticos("22:00", 80, 75, 15)
]
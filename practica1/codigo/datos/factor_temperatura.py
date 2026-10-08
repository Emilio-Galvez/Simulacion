class FactorTemperatura:
    def obtener_factor(self, temperatura):
        if temperatura <= 10:
            return 1.00
        elif temperatura <= 12:
            return 0.90
        elif temperatura <= 14:
            return 0.80
        elif temperatura <= 16:
            return 0.70
        elif temperatura <= 18:
            return 0.60
        elif temperatura <= 20:
            return 0.50
        elif temperatura <= 22:
            return 0.40
        elif temperatura <= 24:
            return 0.30
        elif temperatura <= 26:
            return 0.20
        elif temperatura < 28:
            return 0.15
        else:
            return 0.10
# Aqui creamos un metodo llamado obtener_factor que recibe un parámetro temperatura.
# Se usa <= por si queremos manejar temperaturas que no aparecen en la guia
        



factor = FactorTemperatura()

print(factor.obtener_factor(14))
print(factor.obtener_factor(18))
print(factor.obtener_factor(27))
print(factor.obtener_factor(30)) 


# Hacemos una pequeña prueba de la clase FactorTemperatura creando un objeto factor y llamando al método obtener_factor con diferentes valores de temperatura.